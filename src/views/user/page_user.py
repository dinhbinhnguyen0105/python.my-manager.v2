# src/views/user/page_user.py
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget

from src.my_types import UserType
from src.models.model_user import UserModel

from src.views.user.dialog_user import DialogUser
from src.ui.page_user_ui import Ui_PageUser


class PageUser(QWidget, Ui_PageUser):
    create_new_user_signal = pyqtSignal(UserType)

    def __init__(self, user_model: UserModel, parent=None):
        super(PageUser, self).__init__(parent)
        self.user_model = user_model

        self.setupUi(self)
        self.setWindowTitle("User")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setup_ui()
        self.setup_events()

    def setup_events(self):
        self.action_create_btn.clicked.connect(self.on_create_btn_clicked)

    def setup_ui(self):
        self.users_table.setModel(self.user_model)

    def on_create_btn_clicked(self):
        self.dialog_create = DialogUser(self)
        self.dialog_create.setWindowTitle("Create user")
        self.dialog_create.accepted_signal = self.create_new_user_signal
        self.dialog_create.exec()
