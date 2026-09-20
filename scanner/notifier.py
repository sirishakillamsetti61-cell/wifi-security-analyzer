"""
Module: Desktop notifications.

Uses winotify to show Windows toast notifications.
"""

from winotify import Notification


def send_notification(title: str, message: str, timeout: int = 10) -> None:
    """
    Show a Windows toast notification. duration can be 'short' or 'long'.
    """
    try:
        toast = Notification(
            app_id="Wi-Fi Security Analyzer",
            title=title,
            msg=message,
            duration="short" if timeout <= 10 else "long",
        )
        toast.show()
    except Exception as e:
        print(f"[!] Could not send notification: {e}")