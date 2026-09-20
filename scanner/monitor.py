"""
Module: Wi-Fi connection monitor.

Runs in a loop, checking your Wi-Fi connection state at a set interval.
Fires a desktop notification the moment you disconnect, and another when
you reconnect. Run this in its own terminal window in the background
while you work — press Ctrl+C to stop it.
"""

import subprocess
import time
import re

from scanner.notifier import send_notification

CHECK_INTERVAL_SECONDS = 10


def _get_connection_state() -> str:
    """
    Returns 'connected', 'disconnected', or 'unknown' based on
    `netsh wlan show interfaces`.
    """
    try:
        output = subprocess.check_output(
            ["netsh", "wlan", "show", "interfaces"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"

    match = re.search(r"^\s*State\s*:\s*(.+)$", output, re.MULTILINE)
    if not match:
        return "unknown"

    state = match.group(1).strip().lower()
    return "connected" if state == "connected" else "disconnected"


def monitor_connection():
    print("Monitoring Wi-Fi connection... (Ctrl+C to stop)")
    last_state = _get_connection_state()
    print(f"Initial state: {last_state}")

    try:
        while True:
            time.sleep(CHECK_INTERVAL_SECONDS)
            current_state = _get_connection_state()

            if current_state != last_state:
                if current_state == "disconnected":
                    print("[!] Wi-Fi disconnected!")
                    send_notification(
                        "Wi-Fi Disconnected",
                        "Your Wi-Fi connection was lost.",
                    )
                elif current_state == "connected":
                    print("[✓] Wi-Fi reconnected.")
                    send_notification(
                        "Wi-Fi Reconnected",
                        "Your Wi-Fi connection is back.",
                    )
                last_state = current_state

    except KeyboardInterrupt:
        print("\nMonitor stopped.")


if __name__ == "__main__":
    monitor_connection()