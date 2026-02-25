# 💀 Void-Deauther: Advanced WiFi Disruption Suite

Void-Deauther is a professional-grade security auditing tool designed for Linux systems. It leverages the power of Python and Scapy to provide a high-performance, multi-threaded environment for WiFi network analysis and targeted deauthentication.

---

## ⚡ Quick Start: Zero to Disrupt
To get started immediately on a Debian-based system (Kali, Ubuntu, Parrot OS):

```bash
# 1. Update and install system dependencies
sudo apt update && sudo apt install python3-pip iw aircrack-ng -y

# 2. Clone and enter
git clone https://github.com/your-repo/void-deauther.git
cd void-deauther

# 3. Install Python requirements
pip install -r requirements.txt

# 4. Launch (Standard Usage)
sudo python3 void_deauther.py -i wlan0
```

---

## 🛠️ Step-by-Step Setup Guide

### 1. Hardware Requirements
- **Wireless Interface**: You MUST have a wireless card that supports **Monitor Mode** and **Packet Injection**. (e.g., Alfa AWUS036ACM, TP-Link TL-WN722N v1).
- **Driver Support**: Ensure your drivers are installed and the interface is visible via `iw dev`.

### 2. Software Dependencies
Void-Deauther relies on two core Python libraries:
- `scapy`: For low-level packet fabrication and sniffing.
- `rich`: For the advanced TUI/Dashboard rendering.

### 3. Environment Configuration
Always run the tool with **root privileges**. The tool will automatically attempt to handle monitor mode transitions, but if your card is stubborn, you can manually prepare it:
```bash
sudo airmon-ng start wlan0
```

---

## 🚀 Advanced Usage Guide

### The Interactive Workflow
1. **Interface Initialization**: Pass your interface name with `-i`. The tool will automatically toggle monitor mode.
2. **Global Scanning**: The tool uses a multi-threaded `ChannelHopper` to scan all available frequencies (1-13).
3. **Target Identification**:
   - **APs Table**: Shows SSIDs, BSSIDs, Channels, and Signal Strength.
   - **Clients Table**: Shows which devices are connected to which Access Points.
4. **Disruption Phase**:
   - Select the index of the AP you wish to audit.
   - The tool will start sending a continuous stream of **Reason 7 (Class 3 frame received from nonassociated STA)** deauth packets.

### Command Reference
| Argument | Description | Required |
| --- | --- | --- |
| `-i`, `--interface` | The name of your wireless interface (e.g., wlan0) | Yes |

### Tips & Tricks
- **Signal Strength**: Look for targets with a signal higher than `-70 dBm` for the most effective disruption.
- **Hidden SSIDs**: The scanner will identify hidden networks as `<Hidden>`. You can still target them via their BSSID.
- **Persistence**: If a client reconnects automatically, leave the deauther running to maintain the disruption state.

---

## ⚠️ Legal Disclaimer
Void-Deauther is created for **Educational and Ethical Testing Purposes only**. 
- **DO NOT** use this tool on networks you do not own or have explicit, written permission to test.
- The developers are not responsible for any misuse or damage caused by this program.
- Unauthorized disruption of wireless networks is a criminal offense in most jurisdictions.

---

## 💎 Features at a Glance
- [x] **Automatic Monitor Mode**: No more `iwconfig` manual setup.
- [x] **Real-time Table Updates**: Watch APs and Clients populate live.
- [x] **Targeted & Broadcast Deauth**: Choose between a scalpel or a sledgehammer.
- [x] **Multi-threaded Core**: Scanning and attacking don't block the UI.
- [x] **Modern Aesthetics**: Sleek red/dark dashboard design.
