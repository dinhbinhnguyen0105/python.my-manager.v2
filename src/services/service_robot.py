from typing import List, Tuple, Dict, Optional
from collections import deque
from PyQt6.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot
from dataclasses import dataclass

from src.my_types import UserType


class RobotWorker(QRunnable):
    pass


@dataclass
class RobotTaskType:
    user_info: UserType
    action_name: str


@dataclass
class InProgressType(RobotTaskType):
    worker: RobotWorker
    proxy_url: str


@dataclass
class FailedType(RobotTaskType):
    error_message: str


@dataclass
class SucceededType(RobotTaskType):
    is_success: bool


class RobotService(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pending_task: deque[RobotTaskType] = deque()
        self._in_progress: Dict[int, InProgressType] = {}
        self._failed: Dict[int, FailedType] = {}
        self._succeeded: Dict[int, SucceededType] = {}
        self._total_tasks = 0

        self.threadpool = QThreadPool.globalInstance()

    @pyqtSlot(list, list)
    def add_tasks(self, tasks: List[RobotTaskType], list_proxy: List[str]):
        pass
