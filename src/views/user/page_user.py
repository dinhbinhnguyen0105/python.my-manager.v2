# src/views/user/page_user.py
from typing import List

from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QSortFilterProxyModel
from PyQt6.QtGui import QAction

from src.my_types import UserType
from src.models.model_user import UserModel

from src.ui.page_user_ui import Ui_PageUser


class PageUser(QWidget, Ui_PageUser):
    create_new_user_signal = pyqtSignal()
    user_settings_signal = pyqtSignal()

    updated_users_signal = pyqtSignal(list)
    deleted_users_signal = pyqtSignal(list)
    launch_users_signal = pyqtSignal(list)
    check_users_signal = pyqtSignal(list)

    def __init__(self, user_model: UserModel, parent=None):
        super(PageUser, self).__init__(parent)
        self.user_model = user_model
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.user_model)

        self.setupUi(self)
        self.setWindowTitle("User")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setup_ui()
        self.setup_events()

    def setup_events(self):
        self.action_create_btn.clicked.connect(self.create_new_user_signal)
        self.action_setting_btn.clicked.connect(self.user_settings_signal)

    def setup_ui(self):
        self.users_table.setModel(self.proxy_model)
        self.users_table.setSortingEnabled(True)
        self.users_table.setSelectionBehavior(
            self.users_table.SelectionBehavior.SelectRows
        )
        # self.users_table.setSelectionMode()
        self.users_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.users_table.customContextMenuRequested.connect(self.on_context_menu)
        self.users_table.setColumnHidden(0, True)
        self.users_table.setColumnHidden(1, True)

        self.users_table.setEditTriggers(self.users_table.EditTrigger.NoEditTriggers)

    def on_context_menu(self, pos: QPoint):
        index = self.users_table.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            launch_action = QAction("Launch", self)
            check_action = QAction("Check live", self)
            edit_action = QAction("Edit", self)
            delete_action = QAction("Delete", self)

            launch_action.triggered.connect(
                lambda: self.on_item_context_clicked("launch")
            )
            check_action.triggered.connect(
                lambda: self.on_item_context_clicked("check")
            )
            edit_action.triggered.connect(lambda: self.on_item_context_clicked("edit"))
            delete_action.triggered.connect(
                lambda: self.on_item_context_clicked("delete")
            )
            menu.addAction(launch_action)
            menu.addAction(check_action)
            menu.addAction(edit_action)
            menu.addAction(delete_action)

            menu.popup(self.users_table.viewport().mapToGlobal(pos))

    def on_item_context_clicked(self, action_name: str):
        selected_ids = self.get_selected_id()
        action_method = {
            "launch": self.launch_users_signal,
            "check": self.check_users_signal,
            "edit": self.updated_users_signal,
            "delete": self.deleted_users_signal,
        }
        if action_name in action_method.keys():
            action_method[action_name].emit(selected_ids)

    def get_selected_id(self) -> List[int]:
        selected_rows = self.users_table.selectionModel().selectedRows()
        id_column_index = self.user_model.fieldIndex("id")
        selected_ids = []
        for selected_row in selected_rows:
            source_index = self.proxy_model.mapToSource(selected_row)
            if source_index.isValid():
                id_data = self.user_model.data(
                    source_index.siblingAtColumn(id_column_index),
                    Qt.ItemDataRole.DisplayRole,
                )
                selected_ids.append(id_data)
        return sorted(selected_ids)

    # def on_create_btn_clicked(self):
    #     self.dialog_create = DialogUpdateUser(self)
    #     self.dialog_create.setWindowTitle("Create user")
    #     self.dialog_create.accepted_signal = self.create_new_users_signal
    #     self.dialog_create.exec()
