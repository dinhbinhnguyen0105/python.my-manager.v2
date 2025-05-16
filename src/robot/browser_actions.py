from playwright.sync_api import Page

from PyQt6.QtCore import QRunnable, QObject, pyqtSignal
from src.my_types import RobotTaskType, SucceededType, FailedType


def do_launch_browser(page: Page, task: RobotTaskType, signals):
    try:
        page.goto("http://httpbin.org/ip")
        page.wait_for_event("close", timeout=0)
    except Exception as e:
        print(f"[{task.action_name}] Error: {e}")
        signals.error_signal.emit(
            FailedType(
                user_info=task.user_info,
                udd=task.udd,
                headless=task.headless,
                action_name=task.action_name,
                error_message="Error while launching browser. Check log.",
            )
        )


ACTION_MAP = {
    "launch_browser": do_launch_browser,
}
