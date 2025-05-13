# src/controllers/base_controller.py
from typing import Optional, Any
from PyQt6.QtCore import QObject, pyqtSignal


class BaseController(QObject):
    operation_success_signal = pyqtSignal(str)
    operation_error_signal = pyqtSignal(str)
    operation_warning_signal = pyqtSignal(str)
    data_changed_signal = pyqtSignal()

    def __init__(self, service: Optional[Any], parent=None):
        super().__init__(parent)
        self.service = service
