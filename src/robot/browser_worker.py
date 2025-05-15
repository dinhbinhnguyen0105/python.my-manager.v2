# src/robot/browser_worker.py
from time import sleep
from typing import List, Tuple, Dict, Optional, Callable
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal

from src.my_types import RobotTaskType, SucceededType, FailedType


class WorkerSignals(QObject):
    success_signal = pyqtSignal(SucceededType)
    error_signal = pyqtSignal(FailedType)
    invalid_proxy_signal = pyqtSignal(str)
    finished = pyqtSignal(RobotTaskType)


class BrowserWorker(QRunnable):
    def __init__(
        self,
        proxy_url: Optional[str],
        task: Optional[RobotTaskType],
        callback: Callable,
    ):
        super().__init__()
        self._proxy_url = proxy_url
        self._task = task
        self._callback = callback
        self.signals = WorkerSignals()
        self.setAutoDelete(True)

    def run(self):
        # TODO: Implement the actual task logic here
        try:

            if self._task:
                print(
                    f"Runing uid [{self._task.user_info.uid}] with proxy [{self._proxy_url}]."
                )
                for _ in range(3):
                    sleep(1)
                    print(
                        f"[{self._task.user_info.uid}] Running {self._task.action_name} with proxy [{self._proxy_url}]."
                    )
                self.signals.success_signal.emit(
                    SucceededType(
                        user_info=self._task.user_info,
                        udd=self._task.udd,
                        action_name=self._task.action_name,
                        is_success=True,
                    )
                )

        except Exception as e:
            print(f"[{self.__class__.__name__}.run] Error: {e}")
            # self.signals.error_signal.emit(FailedType(
            #     user_info=self._tasks
            # ))
            return False
        finally:
            self._callback(self._proxy_url)
            self.signals.finished.emit(self._task)
