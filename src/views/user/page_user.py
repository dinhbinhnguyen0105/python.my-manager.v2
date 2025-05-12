# src/views/user/page_user.py
from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QSortFilterProxyModel
from PyQt6.QtGui import QAction

from src.my_types import UserType
from src.models.model_user import UserModel

from src.views.user.dialog_update_user import DialogUpdateUser
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
        # self.action_create_btn.clicked.connect(self.on_create_btn_clicked)
        pass

    def setup_ui(self):
        self.users_table.setModel(self.user_model)
        self.users_table.setSortingEnabled(True)
        self.users_table.setSelectionBehavior(
            self.users_table.SelectionBehavior.SelectRows
        )
        self.users_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.users_table.customContextMenuRequested.connect(
            self.on_context_menu_requested
        )
        self.users_table.setColumnHidden(0, True)

    def on_context_menu_requested(self, pos: QPoint):
        index = self.users_table.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            edit_action = QAction("Edit", self)
            delete_action = QAction("Delete", self)
            edit_action.triggered.connect(self.on_edit_user)
            delete_action.triggered.connect(self.on_delete_user)
            menu.addAction(edit_action)
            menu.addAction(delete_action)

            menu.popup(self.users_table.viewport().mapToGlobal(pos))

    def on_edit_user(self):
        pass

    def on_delete_user(self):
        pass

    # def on_create_btn_clicked(self):
    #     self.dialog_create = DialogUpdateUser(self)
    #     self.dialog_create.setWindowTitle("Create user")
    #     self.dialog_create.accepted_signal = self.create_new_user_signal
    #     self.dialog_create.exec()
