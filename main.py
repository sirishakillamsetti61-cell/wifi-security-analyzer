"""
Wi-Fi Security Analyzer — Phase 1: Basic Scanner

Run against networks you own or are explicitly authorized to test.
"""

from scanner.network import get_network_info
from scanner.devices import get_known_devices
from scanner.security import get_current_wifi_security, evaluate_security
from scanner.nearby_networks import scan_nearby_networks, flag_weak_networks


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

    print("\n" + "=" * 40)
    print("      WI-FI SECURITY CHECK")
    print("=" * 40)

    sec_info = get_current_wifi_security()

    if "error" in sec_info:
        print(f"[!] {sec_info['error']}")
    else:
        print(f"SSID           : {sec_info.get('ssid', 'Unknown')}")
        print(f"Authentication : {sec_info.get('authentication', 'Unknown')}")
        print(f"Cipher         : {sec_info.get('cipher', 'Unknown')}")
        print(f"Radio type     : {sec_info.get('radio_type', 'Unknown')}")
        print(f"Channel        : {sec_info.get('channel', 'Unknown')}")

        print("\n--- Assessment ---")
        for warning in evaluate_security(sec_info):
            print(f"- {warning}")

    print("\n" + "=" * 40)
    print("      NEARBY NETWORK SCAN")
    print("=" * 40)

    nearby = scan_nearby_networks()
    print(f"Networks Found: {len(nearby)}")
    print("-" * 40)
    for net in nearby:
        print(f"{net['ssid']:<25} {net['authentication']:<20} {net['signal']}")

    weak = flag_weak_networks(nearby)
    print(f"\nWeak/Outdated Networks: {len(weak)}")
    if weak:
        for net in weak:
            print(f"  ⚠ {net['ssid']} ({net['authentication']}) — consider avoiding")
    else:
        print("  ✓ No weak or outdated networks detected nearby.")


if __name__ == "__main__":
    main()