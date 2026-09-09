"""
Wi-Fi Security Analyzer — Phase 1: Basic Scanner

Run against networks you own or are explicitly authorized to test.
"""

from scanner.network import get_network_info
from scanner.devices import get_known_devices


def print_banner():
    print("=" * 40)
    print("      WI-FI SECURITY ANALYZER")
    print("=" * 40)


def main():
    print_banner()

    info = get_network_info()
    print(f"\nLocal IP : {info['local_ip']}")
    print(f"Gateway  : {info['gateway']}")
    print(f"Subnet   : {info['subnet']}")

    devices = get_known_devices()
    print(f"\nDevices Found: {len(devices)}")
    print("-" * 40)
    for device in devices:
        print(f"{device['ip']:<16} {device['mac']}")

    if not devices:
        print("(No devices found in ARP cache yet. Try browsing the web or")
        print(" pinging a few devices on your network, then re-run this.)")


if __name__ == "__main__":
    main()
