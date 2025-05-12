# src/views/mainwindow.py
from typing import List
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, QPoint, QSortFilterProxyModel, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QMenu, QDialog

from src import constants
from src.my_types import UserType
from src.controllers.controller_user import UserController

from src.views.product.page_re_product import PageREProduct
from src.views.user.dialog_update_user import DialogUpdateUser
from src.views.user.dialog_create_user import DialogCreateUser
from src.views.user.page_user import PageUser
from src.ui.mainwindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(
        self,
        user_controller: UserController,
        parent=None,
    ):
        super(MainWindow, self).__init__(parent)

        self.user_controller = user_controller
        # self.user_controller.user_service.model
        # self.user_controller.operation_success_signal.connect(self.operation_success)
        self.user_controller.operation_success_signal.connect(
            lambda msg: QMessageBox.information(None, "Success", msg)
        )
        self.user_controller.operation_error_signal.connect(
            lambda msg: QMessageBox.critical(None, "Error", msg)
        )
        self.user_controller.operation_warning_signal.connect(
            lambda msg: QMessageBox.warning(None, "Warning", msg)
        )
        self.user_controller.data_changed_signal.connect(lambda: print("data changed!"))

        self.setupUi(self)
        self.setWindowTitle("My manager")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setMinimumSize(960, 540)

        self.page_re_product = PageREProduct(self)
        self.page_user = PageUser(self.user_controller.user_service.model, self)
        self.page_user.create_new_user_signal.connect(self.on_create_new_user)
        self.page_user.updated_users_signal.connect(self.on_updated_users)
        self.page_user.deleted_users_signal.connect(self.on_deleted_users)
        self.page_user.launch_users_signal.connect(self.on_launch_users)
        self.page_user.check_users_signal.connect(self.on_check_users)

        self.content_container.addWidget(self.page_re_product)
        self.content_container.addWidget(self.page_user)
        self.content_container.setCurrentIndex(1)

        self.setup_ui()

    def setup_ui(self):
        pass

    @pyqtSlot()
    def data_changed(self):
        pass

    @pyqtSlot()
    def on_create_new_user(self):
        # current_time =
        # current_password
        current_time = self.user_controller.handle_new_time()
        dialog_create_user = DialogCreateUser(
            {
                "password": self.user_controller.handle_new_password(),
                "created_at": current_time,
                "updated_at": current_time,
                "user_group": "-1",
                "mobile_ua": self.user_controller.handle_new_mobile_ua(),
                "desktop_ua": self.user_controller.handle_new_desktop_ua(),
            }
        )
        dialog_create_user.accepted_signal.connect(self.handle_create_user)
        dialog_create_user.exec()

    @pyqtSlot(UserType)
    def handle_create_user(self, user_data: UserType) -> bool:
        self.user_controller.handle_add_user(user_data)

    @pyqtSlot(list)
    def on_updated_users(self, selected_ids: List[int]):
        selected_id = selected_ids[0]
        user_data = self.user_controller.handle_read_user(selected_id)
        if not user_data:
            return False
        dialog_update_user = DialogUpdateUser(user_data)
        dialog_update_user.accepted_signal.connect(self.handle_update_user)
        dialog_update_user.exec()

        # TODO custom dialog

    @pyqtSlot(UserType)
    def handle_update_user(self, user_data: UserType) -> bool:
        self.user_controller.handle_update_user(user_data.id, user_data)

    @pyqtSlot(list)
    def on_deleted_users(self, selected_ids: List[int]):
        selected_id = selected_ids[0]
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the user with ID {selected_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.user_controller.handle_delete_user(selected_id)

    @pyqtSlot(list)
    def on_launch_users(self, selected_ids: List[int]):
        pass

    @pyqtSlot(list)
    def on_check_users(self, selected_ids: List[int]):
        self.user_controller.handle_check_users(selected_ids)
