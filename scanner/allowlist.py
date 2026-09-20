"""
Module: Known device allowlist.

Stores trusted device MAC addresses (with optional nicknames) in a local
JSON file, so the device scanner can tell "your phone" apart from
"unknown device on my network."

The allowlist file is personal to your network, so it's excluded from
git via .gitignore — each user builds their own.
"""

import json
import os

ALLOWLIST_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "approved_devices.json",
)


def load_allowlist() -> dict:
    """
    Returns a dict of {MAC_ADDRESS: nickname}. Returns an empty dict if
    the file doesn't exist yet (first run).
    """
    if not os.path.exists(ALLOWLIST_PATH):
        return {}

    try:
        with open(ALLOWLIST_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_allowlist(allowlist: dict) -> None:
    with open(ALLOWLIST_PATH, "w") as f:
        json.dump(allowlist, f, indent=2)


def add_device(mac: str, nickname: str = "") -> None:
    allowlist = load_allowlist()
    allowlist[mac.upper()] = nickname or mac.upper()
    save_allowlist(allowlist)


def remove_device(mac: str) -> bool:
    allowlist = load_allowlist()
    mac = mac.upper()
    if mac in allowlist:
        del allowlist[mac]
        save_allowlist(allowlist)
        return True
    return False


def get_approved_macs() -> set[str]:
    return set(load_allowlist().keys())


if __name__ == "__main__":
    # Simple CLI: python -m scanner.allowlist add AA:BB:CC:DD:EE:FF "My Phone"
    #             python -m scanner.allowlist list
    #             python -m scanner.allowlist remove AA:BB:CC:DD:EE:FF
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print('  python -m scanner.allowlist add <MAC> "<nickname>"')
        print("  python -m scanner.allowlist list")
        print("  python -m scanner.allowlist remove <MAC>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add" and len(sys.argv) >= 3:
        mac = sys.argv[2]
        nickname = sys.argv[3] if len(sys.argv) > 3 else ""
        add_device(mac, nickname)
        print(f"Added {mac} to allowlist" + (f" as '{nickname}'" if nickname else ""))

    elif command == "list":
        allowlist = load_allowlist()
        if not allowlist:
            print("Allowlist is empty.")
        else:
            print(f"Approved devices ({len(allowlist)}):")
            for mac, nickname in allowlist.items():
                print(f"  {mac}  —  {nickname}")

    elif command == "remove" and len(sys.argv) >= 3:
        mac = sys.argv[2]
        if remove_device(mac):
            print(f"Removed {mac} from allowlist")
        else:
            print(f"{mac} was not in the allowlist")

    else:
        print("Unknown command or missing arguments.")