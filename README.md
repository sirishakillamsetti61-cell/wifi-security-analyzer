# Wi-Fi Security Analyzer

A Python command-line tool that audits your local Wi-Fi environment — checking your connection's security settings, discovering devices on your network, scanning nearby networks for weak security, and generating an overall security score.

> ⚠️ **Scope & Ethics:** This tool only reads information your own machine already has access to (ARP cache, OS Wi-Fi APIs) or that routers broadcast publicly. It does not attempt to access, crack, or connect to any network you're not authorized to use. Run it only against networks you own or have explicit permission to test.

## Features

- **Network Info** — reports your local IP, gateway, and subnet
- **Device Discovery** — lists devices on your network via the ARP cache, automatically filtering out noise from virtual adapters (VMware, VirtualBox, Hyper-V, Docker)
- **Known Device Allowlist** — flags any device not on your trusted list as "unknown," helping detect unauthorized Wi-Fi use
- **Connection Security Check** — inspects your current Wi-Fi's authentication type and encryption cipher, flagging outdated or weak configurations (Open, WEP, TKIP)
- **Nearby Network Scanner** — scans for other Wi-Fi networks in range, explicitly flagging fully open (no password) networks as well as other weak/outdated security
- **Overall Security Score** — combines all checks into a single 0–100 score and letter grade (A–F)
- **Disconnect Alerts** — runs a background monitor that sends a desktop notification the moment your Wi-Fi disconnects or reconnects

## Sample Output

```
========================================
      WI-FI SECURITY ANALYZER
========================================

Local IP : 10.29.39.196
Gateway  : 10.29.39.74
Subnet   : 10.29.39.0/24

Devices Found: 1
----------------------------------------
10.29.39.74      F2:4C:C0:0C:83:A6

========================================
      WI-FI SECURITY CHECK
========================================
SSID           : Sirisha
Authentication : WPA2-Personal
Cipher         : CCMP
Radio type     : 802.11n
Channel        : 6

--- Assessment ---
- WPA2 is decent but consider upgrading to WPA3 if supported.

========================================
      NEARBY NETWORK SCAN
========================================
Networks Found: 1
----------------------------------------
Sirisha                   WPA2-Personal        100%

Weak/Outdated Networks: 0
  ✓ No weak or outdated networks detected nearby.

========================================
      OVERALL SECURITY SCORE
========================================
Connection Security : 50 / 60
Device Trust         : 20 / 20
Nearby Network Risk  : 20 / 20
----------------------------------------
TOTAL SCORE          : 90 / 100
GRADE                : A — Excellent
```

## Project Structure

```
wifi-security-analyzer/
├── main.py                     # Entry point — runs all checks together
├── requirements.txt
├── README.md
├── .gitignore
└── scanner/
    ├── __init__.py
    ├── network.py               # Local IP / gateway / subnet detection
    ├── devices.py                # ARP-based device discovery + virtual adapter filtering
    ├── security.py               # Current Wi-Fi authentication/cipher check
    ├── nearby_networks.py        # Nearby network scan + weak network flagging
    └── scorer.py                 # Overall scoring system
```

## Requirements

- Windows (uses `netsh` for Wi-Fi data — Wi-Fi checks and nearby scans are Windows-only)
- Python 3.10+
- `winotify` (for desktop notifications — included in requirements.txt)

## Setup

```bash
# Clone the repository
git clone https://github.com/sirishakillamsetti61-cell/wifi-security-analyzer.git
cd wifi-security-analyzer

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the full analyzer:

```bash
python main.py
```

Or run individual modules on their own:

```bash
python -m scanner.devices             # device discovery only
python -m scanner.security            # connection security check only
python -m scanner.nearby_networks     # nearby network scan only
python -m scanner.monitor             # background disconnect/reconnect notifier
python -m scanner.allowlist add <MAC> "<name>"   # add a trusted device
python -m scanner.allowlist list                  # view trusted devices
python -m scanner.allowlist remove <MAC>          # remove a trusted device
```

## How Scoring Works

| Category               | Max Points | Basis                                              |
|-------------------------|-----------|-----------------------------------------------------|
| Connection Security     | 60        | Authentication type (WPA3/WPA2/WPA/WEP) + cipher strength |
| Device Trust             | 20        | Deducted per unknown/unexpected device detected     |
| Nearby Network Risk      | 20        | Deducted per weak/outdated network detected nearby  |

**Grades:** A (90+) · B (75+) · C (60+) · D (40+) · F (below 40)

## Roadmap / Possible Extensions

- WPS status detection
- Export reports to JSON/HTML
- Cross-platform support (macOS/Linux equivalents for `netsh` calls)

## Disclaimer

Built for educational purposes and personal network auditing. Always ensure you have authorization before scanning or analyzing any network you do not own.