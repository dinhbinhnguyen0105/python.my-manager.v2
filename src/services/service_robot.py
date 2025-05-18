from typing import List, Dict
from collections import deque
from PyQt6.QtCore import QThreadPool, QObject, pyqtSignal, pyqtSlot

from src.robot.browser_worker import BrowserWorker
from src.my_types import RobotTaskType


class RobotService(QObject):
    task_succeeded_signal = pyqtSignal(RobotTaskType)
    task_failed_signal = pyqtSignal(RobotTaskType)
    all_task_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.max_worker_num = 0
        self._pending_tasks: deque[RobotTaskType] = deque()
        self._pending_proxies: deque[str] = deque()
        self._in_progress: Dict[str, dict] = {}
        self._total_tasks = 0

        self.threadpool = QThreadPool.globalInstance()

    @pyqtSlot(list, list)
    def add_tasks(self, list_task: List[RobotTaskType], list_proxy: List[str]):
        existing_uid = set(task.user_info.uid for task in self._pending_tasks) | set(
            key for key in self._in_progress.keys()
        )
        add_uid_in_current_call = set()

        for task in list_task:
            if (
                task.user_info.uid not in existing_uid
                and task.user_info.uid not in add_uid_in_current_call
            ):
                self._pending_tasks.append(task)
                self._total_tasks += 1
                add_uid_in_current_call.add(task.user_info.uid)
        for proxy in list_proxy:
            if proxy not in self._pending_proxies:
                self._pending_proxies.append(proxy)

        self._try_start_tasks()

    def set_max_worker(self, max_worker: int):
        self.max_worker_num = max_worker

    def _try_start_tasks(self):
        available = min(
            self.threadpool.maxThreadCount() - self.threadpool.activeThreadCount(),
            self.max_worker_num,
            len(self._pending_proxies),
        )
        while available > 0 and self._pending_tasks and self._pending_proxies:
            task = self._pending_tasks.popleft()
            proxy = self._pending_proxies.popleft()

            worker = BrowserWorker(
                task=task,
                proxy=proxy,
            )

            available -= 1
            self._in_progress[task.user_info.uid] = {
                "task": task,
                "proxy": proxy,
                "worker": worker,
            }

            worker.signals.error_signal.connect(self.on_worker_error)
            worker.signals.succeeded_signal.connect(self.on_worker_succeeded)
            worker.signals.failed_signal.connect(self.on_worker_failed)
            worker.signals.proxy_unavailable_signal.connect(
                self.on_worker_proxy_unavailable
            )
            worker.signals.proxy_not_ready_signal.connect(
                self.on_worker_proxy_not_ready
            )
            worker.signals.progress_signal.connect(self.on_worker_progress)

            self.threadpool.start(worker)
        if not self._pending_tasks and not self._in_progress:
            self.handle_all_task_finished()

    def set_max_worker(self, max_worker_num: int):
        self.max_worker_num = max_worker_num

    def handle_all_task_finished(self):
        print("Finished!")

    def check_if_done(self) -> bool:
        return not self._pending_tasks and not self._in_progress

    @pyqtSlot(RobotTaskType, str, str)
    def on_worker_succeeded(self, task: RobotTaskType, proxy: str, message: str):
        print(f"[{task.user_info.uid}] {message}.")
        self._pending_proxies.append(proxy)
        if task.user_info.uid in self._in_progress.keys():
            del self._in_progress[task.user_info.uid]
        self._try_start_tasks()

    @pyqtSlot(RobotTaskType, str)
    def on_worker_proxy_unavailable(self, task: RobotTaskType, proxy_url: str):
        print(
            f"[{task.user_info.uid}] Unavailable proxy ({proxy_url})",
        )
        self._pending_tasks.append(task)
        self._try_start_tasks()

    @pyqtSlot(RobotTaskType, str)
    def on_worker_proxy_not_ready(self, task: RobotTaskType, proxy_url: str):
        self._pending_tasks.append(task)
        self._pending_proxies.append(proxy_url)
        self._try_start_tasks()

    @pyqtSlot(RobotTaskType, str)
    def on_worker_error(self, task: RobotTaskType, message: str):
        print(f"[{task.user_info.uid}] Error message: {message}")

    @pyqtSlot(RobotTaskType, str)
    def on_worker_failed(self, task: RobotTaskType, message: str):
        pass

    @pyqtSlot(RobotTaskType, str, int, int)
    def on_worker_progress(
        self, task: RobotTaskType, message: str, current_step: int, total_step: int
    ):
        print(
            f"[{task.user_info.uid}] <{task.action_name}>: Message: {message} ({current_step}/{total_step})"
        )
