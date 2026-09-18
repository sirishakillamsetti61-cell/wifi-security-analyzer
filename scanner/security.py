"""
security.py - Wi-Fi security configuration checker (Windows)

Uses the Windows `netsh` command to inspect the currently connected
Wi-Fi network's authentication type, cipher, and other security details.
"""

import subprocess
import re


def get_current_wifi_security():
    """
    Runs `netsh wlan show interfaces` and parses out security-relevant fields
    for the currently connected Wi-Fi network.
    """
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        return {"error": f"Failed to run netsh: {e}"}
    except FileNotFoundError:
        return {"error": "netsh command not found. Are you on Windows?"}

    info = {}

    patterns = {
        "ssid": r"^\s*SSID\s*:\s*(.+)$",
        "signal": r"^\s*Signal\s*:\s*(.+)$",
        "radio_type": r"^\s*Radio type\s*:\s*(.+)$",
        "authentication": r"^\s*Authentication\s*:\s*(.+)$",
        "cipher": r"^\s*Cipher\s*:\s*(.+)$",
        "channel": r"^\s*Channel\s*:\s*(.+)$",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, output, re.MULTILINE)
        if match:
            info[key] = match.group(1).strip()
        else:
            info[key] = "Unknown"

    return info


def evaluate_security(info):
    """
    Gives a plain-English risk assessment based on the authentication
    and cipher type found.
    """
    auth = info.get("authentication", "Unknown")
    cipher = info.get("cipher", "Unknown")

    warnings = []

    if "Open" in auth:
        warnings.append("Network is OPEN (no encryption) — high risk.")
    elif "WEP" in auth:
        warnings.append("WEP is used — WEP is broken and easily cracked.")
    elif "WPA2" in auth and "WPA3" not in auth:
        warnings.append("WPA2 is decent but consider upgrading to WPA3 if supported.")
    elif "WPA3" in auth:
        warnings.append("WPA3 in use — good, this is currently the strongest standard.")
    else:
        warnings.append(f"Unrecognized authentication type: {auth}")

    if "TKIP" in cipher:
        warnings.append("TKIP cipher detected — TKIP is deprecated, prefer AES/CCMP.")

    return warnings


def print_report():
    info = get_current_wifi_security()

    if "error" in info:
        print(f"[!] {info['error']}")
        return

    print("=== Current Wi-Fi Security Report ===")
    for key, value in info.items():
        print(f"{key.capitalize():15}: {value}")

    print("\n=== Assessment ===")
    for warning in evaluate_security(info):
        print(f"- {warning}")


if __name__ == "__main__":
    print_report()