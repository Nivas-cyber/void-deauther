import subprocess
import os

class InterfaceManager:
    def __init__(self, interface):
        self.interface = interface

    def run_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    def set_monitor_mode(self, enable=True):
        if enable:
            self.run_command(f"ip link set {self.interface} down")
            self.run_command(f"iw dev {self.interface} set type monitor")
            self.run_command(f"ip link set {self.interface} up")
            return f"Interface {self.interface} set to monitor mode."
        else:
            self.run_command(f"ip link set {self.interface} down")
            self.run_command(f"iw dev {self.interface} set type managed")
            self.run_command(f"ip link set {self.interface} up")
            return f"Interface {self.interface} set to managed mode."

    def set_channel(self, channel):
        self.run_command(f"iw dev {self.interface} set channel {channel}")

    def get_interfaces(self):
        return self.run_command("iw dev | grep Interface | awk '{print $2}'").splitlines()
