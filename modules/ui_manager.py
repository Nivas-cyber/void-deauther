from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text

console = Console()

class UIManager:
    def __init__(self):
        self.console = console

    def banner(self):
        banner_text = Text("""
 ██╗   ██╗  ██████╗  ██╗ ██████╗       ██████╗  ███████╗  █████╗  ██╗   ██╗ ████████╗ ██╗  ██╗ ███████╗ ██████╗ 
 ██║   ██║ ██╔═══██╗ ██║ ██╔══██╗      ██╔══██╗ ██╔════╝ ██╔══██╗ ██║   ██║ ╚══██╔══╝ ██║  ██║ ██╔════╝ ██╔══██╗
 ██║   ██║ ██║   ██║ ██║ ██║  ██║      ██║  ██║ █████╗   ███████║ ██║   ██║    ██║    ███████║ █████╗   ██████╔╝
 ╚██╗ ██╔╝ ██║   ██║ ██║ ██║  ██║      ██║  ██║ ██╔══╝   ██╔══██║ ██║   ██║    ██║    ██╔══██║ ██╔══╝   ██╔══██╗
  ╚████╔╝  ╚██████╔╝ ██║ ██████╔╝      ██████╔╝ ███████╗ ██║  ██║ ╚██████╔╝    ██║    ██║  ██║ ███████╗ ██║  ██║
   ╚═══╝    ╚═════╝  ╚═╝ ╚═════╝       ╚═════╝  ╚══════╝ ╚═╝  ╚═╝  ╚═════╝     ╚═╝    ╚═╝  ╚═╝ ╚══════╝ ╚═╝  ╚═╝
        """, style="bold red")
        self.console.print(Panel(banner_text, subtitle="v1.0 - Advanced WiFi Deauthentication Tool", border_style="red"))

    def create_aps_table(self, aps):
        table = Table(title="Available Access Points", expand=True)
        table.add_column("BSSID", style="yellow")
        table.add_column("SSID", style="green")
        table.add_column("CH", style="magenta")
        table.add_column("Sig (dBm)", style="red")

        for bssid, info in aps.items():
            table.add_row(bssid, info['ssid'], str(info['channel']), str(info['signal']))
        return table

    def create_clients_table(self, clients, aps):
        table = Table(title="Connected Clients", expand=True)
        table.add_column("Client MAC", style="yellow")
        table.add_column("AP BSSID", style="cyan")
        table.add_column("SSID", style="green")

        for client_mac, bssid in clients.items():
            ssid = aps.get(bssid, {}).get('ssid', 'Unknown')
            table.add_row(client_mac, bssid, ssid)
        return table

    def display_scanning(self, aps, clients):
        layout = Layout()
        layout.split_row(
            Layout(self.create_aps_table(aps), name="left"),
            Layout(self.create_clients_table(clients, aps), name="right")
        )
        return layout
