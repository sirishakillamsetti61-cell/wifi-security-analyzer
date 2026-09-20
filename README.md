# Wi-Fi Security Analyzer

A Python command-line tool that audits your local Wi-Fi environment — checking your connection's security settings, discovering devices on your network, scanning nearby networks for weak security, and generating an overall security score.

> ⚠️ **Scope & Ethics:** This tool only reads information your own machine already has access to (ARP cache, OS Wi-Fi APIs) or that routers broadcast publicly. It does not attempt to access, crack, or connect to any network you're not authorized to use. Run it only against networks you own or have explicit permission to test.

## Features

- **Network Info** — reports your local IP, gateway, and subnet
- **Device Discovery** — lists devices on your network via the ARP cache, automatically filtering out noise from virtual adapters (VMware, VirtualBox, Hyper-V, Docker)
- **Connection Security Check** — inspects your current Wi-Fi's authentication type and encryption cipher, flagging outdated or weak configurations (Open, WEP, TKIP)
- **Nearby Network Scanner** — scans for other Wi-Fi networks in range and flags any using weak or outdated security
- **Overall Security Score** — combines all checks into a single 0–100 score and letter grade (A–F)

## Sample Output