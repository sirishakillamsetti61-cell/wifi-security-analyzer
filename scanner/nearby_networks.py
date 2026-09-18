"""
Module: Nearby network scanner.

Scans for all Wi-Fi networks currently visible to your adapter (not just
the one you're connected to), using Windows' built-in `netsh` command.
Flags networks using weak or outdated security settings.

This module only passively reads broadcast information that every nearby
router already sends out publicly (SSID, signal strength, security type).
It does not attempt to connect to, access, or crack any network.
"""

import subprocess
import platform
import re

WEAK_AUTH_TYPES = {"Open", "WEP", "WEP40", "WEP104", "Shared"}
LEGACY_AUTH_TYPES = {"WPA-Personal", "WPA-Enterprise", "WPA-None"}


def _run_netsh_networks() -> str:
    try:
        return subprocess.check_output(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def scan_nearby_networks() -> list[dict]:
    """
    Parse `netsh wlan show networks mode=bssid` output into a list of
    dicts, one per SSID, each with authentication type and best signal
    strength seen across its access points.
    """
    if platform.system() != "Windows":
        return []

    output = _run_netsh_networks()
    if not output:
        return []

    networks = []
    current = None

    for line in output.splitlines():
        ssid_match = re.match(r"^SSID\s+\d+\s*:\s*(.*)$", line.strip())
        auth_match = re.match(r"^Authentication\s*:\s*(.*)$", line.strip())
        signal_match = re.match(r"^Signal\s*:\s*(.*)$", line.strip())

        if ssid_match:
            if current:
                networks.append(current)
            current = {
                "ssid": ssid_match.group(1).strip() or "(hidden network)",
                "authentication": "Unknown",
                "signal": "Unknown",
            }
        elif auth_match and current:
            current["authentication"] = auth_match.group(1).strip()
        elif signal_match and current:
            new_signal = signal_match.group(1).strip()
            old_signal = current.get("signal", "0%")
            try:
                if int(new_signal.rstrip("%")) > int(old_signal.rstrip("%")):
                    current["signal"] = new_signal
            except ValueError:
                current["signal"] = new_signal

    if current:
        networks.append(current)

    return networks


def flag_weak_networks(networks: list[dict]) -> list[dict]:
    """Return only the networks using weak/outdated authentication."""
    weak = []
    for net in networks:
        auth = net.get("authentication", "Unknown")
        if auth in WEAK_AUTH_TYPES or auth in LEGACY_AUTH_TYPES:
            weak.append(net)
    return weak


if __name__ == "__main__":
    nets = scan_nearby_networks()
    print(f"Nearby Networks Found: {len(nets)}")
    print("-" * 50)
    for n in nets:
        print(f"{n['ssid']:<25} {n['authentication']:<20} {n['signal']}")

    weak = flag_weak_networks(nets)
    print(f"\n⚠ Weak/Outdated Networks: {len(weak)}")
    for n in weak:
        print(f"  - {n['ssid']} ({n['authentication']})")