# src/controllers/user_controller.py
from typing import List, Dict, Any, Optional
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QModelIndex
from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QMessageBox,
)
from src.controllers.base_controller import (
    BaseController,
)
from src.services.service_user import (
    UserService,
)
from src.models.model_user import UserModel
from src.my_types import UserType


class UserController(BaseController):
    def __init__(self, service: UserService, user_form_view: QWidget, parent=None):
        super().__init__(service, parent)
