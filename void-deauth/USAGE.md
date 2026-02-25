# Void-Deauther Usage Guide

Void-Deauther is an advanced WiFi deauthentication tool designed for network security testing. It automates the process of scanning, targeting, and attacking WiFi networks and their clients.

## ⚠️ Legal Disclaimer
This tool is for educational purposes and authorized penetration testing only. Use it only on networks you own or have explicit permission to test. Unauthorized access is illegal.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- **Operating System**: Linux (Ubuntu, Kali, Parrot, etc.) - Monitor mode is required.
- **Wireless Adapter**: A WiFi adapter that supports **Monitor Mode** and **Packet Injection** (e.g., adapters with Atheros, Ralink, or Realtek chipsets).
- **Python**: Python 3.8 or higher.

### 2. Install Dependencies
Install the required Python libraries using pip:
```bash
sudo pip3 install -r requirements.txt
```
*Note: Scapy requires root privileges to interact with network interfaces.*

### 3. Install System Tools
Ensure you have `iw` and `ip` tools installed (usually pre-installed on Linux):
```bash
sudo apt update && sudo apt install iw iproute2 -y
```

---

## 🚀 How to Use

### 1. Find your Wireless Interface
List your wireless interfaces to identify the one you want to use:
```bash
iw dev
```
Typical names are `wlan0`, `wlan1`, etc.

### 2. Run the Tool
Start the tool by specifying your wireless interface. The tool will automatically set the interface to monitor mode.
```bash
sudo python3 void_deauther.py -i <interface_name>
```
Example:
```bash
sudo python3 void_deauther.py -i wlan1
```

### 3. Scanning Phase
Once started, the tool will:
- Set your interface to **Monitor Mode**.
- Start **Channel Hopping** to find all nearby 2.4GHz Access Points (APs).
- **Discover Clients**: It sniffs data packets to find devices connected to those APs.
- **Display Tables**: Shows a real-time list of APs and their connected clients.

### 4. Selecting a Target
1. Press `Ctrl+C` once you see your target network in the list.
2. A list of available targets will appear with indices (0, 1, 2...).
3. **Enter the index** of the AP you want to attack.

### 5. The Attack
The tool will perform a "Perfect Attack":
1. **Sync Channel**: Switches your adapter to the target AP's channel.
2. **Targeted Bursts**: 
   - Sends **Broadcast Deauth** packets to the AP (affects everyone).
   - Sends **Direct Deauth** packets to every specific client found on that network.
   - Rotates through **Reason Codes** (1, 4, 7, 9) to bypass router protections.

To stop the attack, press `Ctrl+C`. The interface will automatically restore to **Managed Mode**.

---

## 🔍 Troubleshooting

- **No Networks Found**: Ensure your WiFi adapter is plugged in and supports 5GHz if you are looking for 5GHz networks (this tool currently prioritizes 2.4GHz channels 1-13).
- **Interface Error**: If the tool fails to set monitor mode, try manually setting it or killing conflicting processes:
  ```bash
  sudo airmon-ng check kill
  ```
- **Permission Denied**: Always run the tool with `sudo`.
