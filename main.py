"""
Wi-Fi Security Analyzer — Phase 1: Basic Scanner

Run against networks you own or are explicitly authorized to test.
"""

from scanner.network import get_network_info
from scanner.devices import get_known_devices, compare_to_approved
from scanner.security import get_current_wifi_security, evaluate_security
from scanner.nearby_networks import scan_nearby_networks, flag_weak_networks, flag_open_networks
from scanner.scorer import compute_overall_score
from scanner.allowlist import get_approved_macs



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
    approved_macs = get_approved_macs()
    comparison = compare_to_approved(devices, approved_macs)

    print(f"\nDevices Found: {len(devices)}")
    print("-" * 40)
    for device in devices:
        status = "✓ known" if device["mac"] in approved_macs else "⚠ UNKNOWN"
        print(f"{device['ip']:<16} {device['mac']:<20} {status}")

    if not devices:
        print("(No devices found in ARP cache yet. Try browsing the web or")
        print(" pinging a few devices on your network, then re-run this.)")

    unknown_count = len(comparison["unknown"])
    if unknown_count > 0:
        print(f"\n⚠ {unknown_count} unrecognized device(s) on your network!")
        print("  If you don't recognize these, someone may be using your Wi-Fi.")
        print("  Add trusted devices with: python -m scanner.allowlist add <MAC> \"<name>\"")

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

    open_nets = flag_open_networks(nearby)
    print(f"\n🔓 Open (No Password) Networks: {len(open_nets)}")
    if open_nets:
        for net in open_nets:
            print(f"  - {net['ssid']}  (Signal: {net['signal']}) — anyone can join, unencrypted!")
    else:
        print("  ✓ No completely open networks detected nearby.")

    weak = flag_weak_networks(nearby)
    print(f"\nWeak/Outdated Networks: {len(weak)}")
    if weak:
        for net in weak:
            print(f"  ⚠ {net['ssid']} ({net['authentication']}) — consider avoiding")
    else:
        print("  ✓ No weak or outdated networks detected nearby.")
        print("\n" + "=" * 40)
    print("      OVERALL SECURITY SCORE")
    print("=" * 40)

    result = compute_overall_score(
        sec_info=sec_info,
        sec_warnings=evaluate_security(sec_info) if "error" not in sec_info else [],
        devices=devices,
        weak_nearby=weak,
        unknown_device_count=unknown_count,
    )

    print(f"Connection Security : {result['connection_score']} / 60")
    print(f"Device Trust         : {result['device_score']} / 20")
    print(f"Nearby Network Risk  : {result['nearby_score']} / 20")
    print("-" * 40)
    print(f"TOTAL SCORE          : {result['total_score']} / 100")
    print(f"GRADE                : {result['grade']}") 


if __name__ == "__main__":
    main()