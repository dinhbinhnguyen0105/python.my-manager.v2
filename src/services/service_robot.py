from typing import List, Tuple, Dict, Optional
from collections import deque
from PyQt6.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot
from dataclasses import dataclass

from src.robot.browser_worker import BrowserWorker
from src.my_types import (
    UserType,
    RobotTaskType,
    InProgressType,
    FailedType,
    SucceededType,
)


class RobotService(QObject):
    task_succeeded = pyqtSignal(RobotTaskType)
    task_failed = pyqtSignal(RobotTaskType)
    tasks_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.max_workers_num = 0
        self._pending_task: deque[RobotTaskType] = deque()
        self._proxy_pool: deque[str] = deque()
        self._in_progress: Dict[str, InProgressType] = {}
        self._failed: Dict[str, FailedType] = {}
        self._succeeded: Dict[str, SucceededType] = {}
        self._total_tasks = 0

        self.threadpool = QThreadPool.globalInstance()

    @pyqtSlot(list, list)
    def add_tasks(self, tasks: List[RobotTaskType], list_proxy: List[str]):
        existing_uids = set(ptask.user_info.uid for ptask in self._pending_task) | set(
            ip_task_data.user_info.uid for ip_task_data in self._in_progress.values()
        )

        added_uids_in_current_call = set()

        for task in tasks:
            uid_to_check = task.user_info.uid
            if (
                uid_to_check not in existing_uids
                and uid_to_check not in added_uids_in_current_call
            ):
                self._pending_task.append(task)
                self._total_tasks += 1
                added_uids_in_current_call.add(uid_to_check)

        self._proxy_pool.extend(list_proxy)
        self._try_start_tasks()

    def set_max_workers(self, max_workers: int):
        self.max_workers_num = max_workers

    def _try_start_tasks(self):
        available = min(
            self.threadpool.maxThreadCount() - self.threadpool.activeThreadCount(),
            self.max_workers_num,
        )
        while available > 0 and self._pending_task and self._proxy_pool:
            task = self._pending_task.popleft()
            proxy_url = self._proxy_pool.popleft()
            worker = BrowserWorker(proxy_url, task, self._on_task_complete)

            worker.signals.success_signal.connect(self.on_success)
            worker.signals.error_signal.connect(self.on_error)
            worker.signals.invalid_proxy_signal.connect(self.on_error_proxy)
            worker.signals.finished.connect(self.on_finished)

            self._in_progress[task.user_info.uid] = InProgressType(
                user_info=task.user_info,
                udd=task.udd,
                action_name=task.action_name,
                proxy_url=proxy_url,
                worker=worker,
            )
            self.threadpool.start(worker)
            available -= 1

    def _on_task_complete(self, proxy: str):
        self._proxy_pool.append(proxy)
        self._try_start_tasks()

    @pyqtSlot(RobotTaskType)
    def on_finished(self, taks_info: RobotTaskType):
        if taks_info.user_info.uid in self._in_progress:
            del self._in_progress[taks_info.user_info.uid]

        self._try_start_tasks()
        if not self._pending_task and not self._in_progress:
            self.tasks_finished.emit()

    @pyqtSlot(SucceededType)
    def on_success(self, succeeded_info: SucceededType):
        print(f"uid: {succeeded_info.user_info.uid} succeeded.")

    @pyqtSlot(FailedType)
    def on_error(self, error_info: FailedType):
        print(error_info)

    @pyqtSlot(str)
    def on_error_proxy(self, invalid_proxy: str):
        print(invalid_proxy)

    def check_if_done(self) -> bool:
        is_done = not self._pending_task and not self._in_progress
        processed_count = len(self._succeeded) + len(self._failed)
        if self._total_tasks > 0 and processed_count != self._total_tasks:
            print(
                f"[{self.__class__.__name__}.check_if_done] Warning: Process count ({processed_count}) does not match total tasks ({self._total_tasks})."
            )
            return False
        return is_done
