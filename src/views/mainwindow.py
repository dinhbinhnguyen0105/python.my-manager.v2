# src/views/mainwindow.py
from typing import List, Optional
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, QPoint, QSortFilterProxyModel, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QMenu, QDialog

from src import constants
from src.my_types import UserType, UserSettingProxyType, UserSettingUDDType
from src.controllers.controller_user import (
    UserController,
    UserSettingUDDController,
    UserSettingProxyController,
)
from src.controllers.controller_robot import RobotController

from src.views.product.page_re_product import PageREProduct
from src.views.user.dialog_update_user import DialogUpdateUser
from src.views.user.dialog_create_user import DialogCreateUser
from src.views.user.dialog_user_settings import DialogUserSettings
from src.views.user.page_user import PageUser
from src.ui.mainwindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(
        self,
        user_controller: UserController,
        setting_udd_controller: UserSettingUDDController,
        setting_proxy_controller: UserSettingProxyController,
        robot_controller: RobotController,
        parent=None,
    ):
        super(MainWindow, self).__init__(parent)

        self.user_controller = user_controller
        self.setting_proxy_controller = setting_proxy_controller
        self.setting_udd_controller = setting_udd_controller
        self.robot_controller = robot_controller
        for controller in [
            self.user_controller,
            self.setting_proxy_controller,
            self.setting_udd_controller,
            self.robot_controller,
        ]:
            controller.operation_success_signal.connect(
                lambda msg: QMessageBox.information(None, "Success", msg)
            )
            controller.operation_error_signal.connect(
                lambda msg: QMessageBox.critical(None, "Error", msg)
            )
            controller.operation_warning_signal.connect(
                lambda msg: QMessageBox.warning(None, "Warning", msg)
            )
            controller.data_changed_signal.connect(lambda: print("data changed!"))

        self.setupUi(self)
        self.setWindowTitle("My manager")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setMinimumSize(960, 540)

        self.page_re_product = PageREProduct(self)
        self.page_user = PageUser(self.user_controller.service.model, self)
        self.page_user.create_new_user_signal.connect(self.on_create_new_user)
        self.page_user.user_settings_signal.connect(self.on_user_settings)
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

    @pyqtSlot()
    def on_user_settings(self):
        dialog_user_settings = DialogUserSettings(
            udd_model=self.setting_udd_controller.service.model,
            proxy_model=self.setting_proxy_controller.service.model,
        )
        dialog_user_settings.create_new_udd_signal.connect(
            self.on_user_setting_create_new_udd
        )
        dialog_user_settings.create_new_proxy_signal.connect(
            self.on_user_setting_create_new_proxy
        )
        dialog_user_settings.delete_proxy_signal.connect(
            self.on_user_setting_delete_proxy
        )
        dialog_user_settings.delete_udd_signal.connect(self.on_user_setting_delete_udd)
        dialog_user_settings.set_selected_udd_signal.connect(
            self.on_user_setting_set_selected_udd
        )
        dialog_user_settings.exec()

    @pyqtSlot(UserSettingUDDType)
    def on_user_setting_create_new_udd(self, payload: UserSettingProxyType):
        self.setting_udd_controller.handle_add_udd(payload)

    @pyqtSlot(UserSettingProxyType)
    def on_user_setting_create_new_proxy(self, payload: UserSettingProxyType):
        self.setting_proxy_controller.handle_add_proxy(payload)

    @pyqtSlot(int)
    def on_user_setting_delete_proxy(self, record_id: str):
        self.setting_proxy_controller.handle_delete_proxy(record_id)

    @pyqtSlot(int)
    def on_user_setting_delete_udd(self, record_id: str):
        self.setting_udd_controller.handle_delete_udd(record_id)

    @pyqtSlot(int)
    def on_user_setting_set_selected_udd(self, record_id: str):
        self.setting_udd_controller.handle_set_selected(record_id)

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
            self.user_controller.handle_delete_user(
                self.setting_udd_controller,
                selected_id,
            )

    @pyqtSlot(list, bool)
    def on_launch_users(self, selected_ids: List[int], is_mobile: bool):
        self.robot_controller.handle_launch_browser(
            selected_ids, headless=False, is_mobile=is_mobile
        )

    @pyqtSlot(list)
    def on_check_users(self, selected_ids: List[int]):
        self.user_controller.handle_check_users(selected_ids)
