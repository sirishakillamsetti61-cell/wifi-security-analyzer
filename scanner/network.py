"""
Module 1 — Network Discovery
Finds the local IP, default gateway, and subnet of the current network.
Uses only the standard library, so it works without admin/root privileges.
"""

import socket
import subprocess
import platform
import re
import ipaddress


def get_local_ip() -> str:
    """Return this machine's LAN IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def _get_gateway_windows() -> str:
    # Primary method: ask Windows routing table directly via PowerShell.
    try:
        output = subprocess.check_output(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-NetRoute -DestinationPrefix '0.0.0.0/0' | "
                "Sort-Object -Property RouteMetric | "
                "Select-Object -First 1 -ExpandProperty NextHop)",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", output):
            return output
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fallback: parse ipconfig output, skipping blank gateway lines.
    try:
        output = subprocess.check_output(
            ["ipconfig"], text=True, stderr=subprocess.DEVNULL
        )
        for match in re.finditer(r"Default Gateway[ .]*: ?([\d.]*)", output):
            candidate = match.group(1).strip()
            if candidate:
                return candidate
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return "Unknown"


def get_default_gateway() -> str:
    """Return the default gateway IP, using OS-specific commands."""
    system = platform.system()

    try:
        if system == "Windows":
            return _get_gateway_windows()

        elif system == "Darwin":  # macOS
            output = subprocess.check_output(
                ["route", "-n", "get", "default"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            match = re.search(r"gateway: ([\d.]+)", output)
            if match:
                return match.group(1)

        else:  # Linux
            output = subprocess.check_output(
                ["ip", "route", "show", "default"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            match = re.search(r"default via ([\d.]+)", output)
            if match:
                return match.group(1)

    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return "Unknown"


def get_subnet(local_ip: str, prefix_len: int = 24) -> str:
    """Return the subnet in CIDR notation for the given IP."""
    try:
        network = ipaddress.ip_network(f"{local_ip}/{prefix_len}", strict=False)
        return str(network)
    except ValueError:
        return "Unknown"


def get_network_info() -> dict:
    """Bundle together the core network facts used by the rest of the app."""
    local_ip = get_local_ip()
    gateway = get_default_gateway()
    subnet = get_subnet(local_ip)

    return {
        "local_ip": local_ip,
        "gateway": gateway,
        "subnet": subnet,
    }


if __name__ == "__main__":
    info = get_network_info()
    print("Network Discovery")
    print("-" * 30)
    print(f"Local IP : {info['local_ip']}")
    print(f"Gateway  : {info['gateway']}")
    print(f"Subnet   : {info['subnet']}")
