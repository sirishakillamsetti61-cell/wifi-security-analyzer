"""
Module: Overall security scorer.

Combines results from the connection security check, device scan, and
nearby network scan into a single overall score (0-100) and letter grade.

Scoring breakdown:
    - Connection security (auth + cipher): up to 60 points
    - Unknown/unexpected device presence:  up to 20 points
    - Nearby weak/outdated networks:       up to 20 points
      (this reflects general area risk, not your own network's fault,
      but still useful context — e.g. WPS/rogue-AP risk nearby)
"""


def score_connection_security(sec_info: dict, warnings: list[str]) -> int:
    """Score the current connection's auth/cipher out of 60."""
    if "error" in sec_info:
        return 0

    auth = sec_info.get("authentication", "Unknown")
    cipher = sec_info.get("cipher", "Unknown")
    score = 0

    if "WPA3" in auth:
        score += 30
    elif "WPA2" in auth:
        score += 20
    elif "WPA" in auth:
        score += 10
    elif "WEP" in auth or "Open" in auth:
        score += 0
    else:
        score += 5  # unknown, partial credit

    if "CCMP" in cipher or "AES" in cipher or "GCMP" in cipher:
        score += 30
    elif "TKIP" in cipher:
        score += 10
    elif "None" in cipher:
        score += 0
    else:
        score += 5

    return min(score, 60)


def score_devices(devices: list[dict], unknown_count: int = 0) -> int:
    """
    Score device presence out of 20. Full marks if no unexpected/unknown
    devices are on the network. Deduct per unknown device found.
    """
    if unknown_count == 0:
        return 20
    return max(20 - (unknown_count * 10), 0)


def score_nearby_networks(weak_networks: list[dict]) -> int:
    """Score nearby-area risk out of 20 based on weak networks detected."""
    if not weak_networks:
        return 20
    return max(20 - (len(weak_networks) * 5), 0)


def grade_from_score(score: int) -> str:
    if score >= 90:
        return "A — Excellent"
    elif score >= 75:
        return "B — Good"
    elif score >= 60:
        return "C — Fair, room for improvement"
    elif score >= 40:
        return "D — Weak, review your settings"
    else:
        return "F — Poor, take action immediately"


def compute_overall_score(
    sec_info: dict,
    sec_warnings: list[str],
    devices: list[dict],
    weak_nearby: list[dict],
    unknown_device_count: int = 0,
) -> dict:
    conn_score = score_connection_security(sec_info, sec_warnings)
    device_score = score_devices(devices, unknown_device_count)
    nearby_score = score_nearby_networks(weak_nearby)

    total = conn_score + device_score + nearby_score
    grade = grade_from_score(total)

    return {
        "connection_score": conn_score,
        "device_score": device_score,
        "nearby_score": nearby_score,
        "total_score": total,
        "grade": grade,
    }