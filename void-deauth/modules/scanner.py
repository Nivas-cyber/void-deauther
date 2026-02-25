from scapy.all import *
import threading
import time

class Scanner:
    def __init__(self, interface):
        self.interface = interface
        self.aps = {}  # {BSSID: {SSID, Channel, Signal}}
        self.clients = {} # {ClientMAC: BSSID}
        self.scanning = False

    def packet_handler(self, pkt):
        try:
            if pkt.haslayer(Dot11Beacon):
                bssid = pkt[Dot11].addr2
                # Robust SSID decoding
                try:
                    ssid = pkt[Dot11Elt].info.decode('utf-8', errors='ignore')
                except:
                    ssid = "Unknown"
                
                if not ssid:
                    ssid = "Hidden"

                stats = pkt[Dot11Beacon].network_stats()
                channel = stats.get("channel")
                signal = pkt.dBm_AntSignal if hasattr(pkt, 'dBm_AntSignal') else "N/A"
                self.aps[bssid] = {"ssid": ssid, "channel": channel, "signal": signal}
            
            elif pkt.haslayer(Dot11) and pkt.type == 2: # Data frame
                sn = pkt[Dot11].addr2
                rc = pkt[Dot11].addr1
                # Filter out broadcast and invalid MACs
                if rc != "ff:ff:ff:ff:ff:ff" and sn != "ff:ff:ff:ff:ff:ff":
                    if sn in self.aps:
                        self.clients[rc] = sn
                    elif rc in self.aps:
                        self.clients[sn] = rc
        except Exception:
            pass # Keep thread alive

    def sniff_packets(self):
        sniff(iface=self.interface, prn=self.packet_handler, store=0, stop_filter=lambda x: not self.scanning)

    def start(self):
        self.scanning = True
        self.sniff_thread = threading.Thread(target=self.sniff_packets, daemon=True)
        self.sniff_thread.start()

    def stop(self):
        self.scanning = False

    def get_results(self):
        return self.aps, self.clients
