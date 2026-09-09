"""
Module: Device discovery.

Phase 1 approach: read the OS's existing ARP cache (the table of devices
your machine has already talked to on the LAN). This requires no special
privileges and touches no other device directly — it just reads local state.

Broadcast and multicast entries (used for network-wide announcements, not
individual devices) are filtered out for a cleaner, more accurate list.
"""

import subprocess
import platform
import re

BROADCAST_MAC = "FF:FF:FF:FF:FF:FF"


def _run_arp_a() -> str:
    try:
        return subprocess.check_output(
            ["arp", "-a"], text=True, stderr=subprocess.DEVNULL
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def _is_multicast_mac(mac: str) -> bool:
    # Multicast MACs start with 01:00:5E (IPv4) or 33:33 (IPv6).
    return mac.startswith("01:00:5E") or mac.startswith("33:33")


def _is_broadcast_or_multicast(ip: str, mac: str) -> bool:
    if mac == BROADCAST_MAC:
        return True
    if _is_multicast_mac(mac):
        return True
    if ip.endswith(".255"):  # common subnet broadcast pattern
        return True
    if ip.startswith("224.") or ip.startswith("239."):  # multicast IP range
        return True
    if ip == "255.255.255.255":
        return True
    return False


def get_known_devices() -> list[dict]:
    """
    Parse the system ARP table into a list of {ip, mac} dicts,
    excluding broadcast/multicast noise.
    """
    output = _run_arp_a()
    if not output:
        return []

    system = platform.system()
    raw_devices = []

    if system == "Windows":
        pattern = re.compile(
            r"(\d{1,3}(?:\.\d{1,3}){3})\s+([0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5})"
        )
        for ip, mac in pattern.findall(output):
            raw_devices.append({"ip": ip, "mac": mac.replace("-", ":").upper()})

    else:
        pattern = re.compile(
            r"\((\d{1,3}(?:\.\d{1,3}){3})\)\s+at\s+"
            r"([0-9a-fA-F]{1,2}(?::[0-9a-fA-F]{1,2}){5})"
        )
        for ip, mac in pattern.findall(output):
            raw_devices.append({"ip": ip, "mac": mac.upper()})

    # Filter out broadcast/multicast noise and de-duplicate.
    seen = set()
    devices = []
    for d in raw_devices:
        if _is_broadcast_or_multicast(d["ip"], d["mac"]):
            continue
        key = (d["ip"], d["mac"])
        if key in seen:
            continue
        seen.add(key)
        devices.append(d)

    return devices


def compare_to_approved(devices: list[dict], approved_macs: set[str]) -> dict:
    """Split discovered devices into known vs. unknown based on an allowlist."""
    approved_upper = {mac.upper() for mac in approved_macs}
    known, unknown = [], []

    for device in devices:
        if device["mac"] in approved_upper:
            known.append(device)
        else:
            unknown.append(device)

    return {"known": known, "unknown": unknown}


if __name__ == "__main__":
    found = get_known_devices()
    print(f"Devices Found: {len(found)}\n")
    for d in found:
        print(f"{d['ip']:<16} {d['mac']}")
