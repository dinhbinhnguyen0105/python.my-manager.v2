# src/views/user/dialog_user.py
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIntValidator

from src.my_types import UserType

from src.ui.dialog_user_ui import Ui_Dialog_User


class DialogUpdateUser(QDialog, Ui_Dialog_User):
    accepted_signal = pyqtSignal(UserType)

    def __init__(self, user_info: UserType, parent=None):
        super(DialogUpdateUser, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.user_info = user_info
        self.setWindowTitle(f"Update user {self.user_info.uid} - ({self.user_info.id})")

        self.group_input.setValidator(QIntValidator())
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.handle_save)

    def set_input_fields(self):
        self.uid_input.setText(self.user_info.uid)
        self.status_checkbox.setChecked(self.user_info.status == 1)
        self.username_input.setText(self.user_info.username)
        self.password_input.setText(self.user_info.password)
        self.two_fa_input.setText(self.user_info.two_fa)
        self.email_input.setText(self.user_info.email)
        self.email_password_input.setText(self.user_info.email_password)
        self.phone_number_input.setText(self.user_info.phone_number)
        self.note_input.setText(self.user_info.note)
        self.type_input.setText(self.user_info.type)
        self.group_input.setText(self.user_info.user_group)
        self.mobile_ua_input.setText(self.user_info.mobile_ua)
        self.desktop_ua_input.setText(self.user_info.desktop_ua)
        self.updated_at_input.setText(self.user_info.updated_at)
        self.created_at_input.setText(self.user_info.created_at)

    def handle_save(self):
        self.accepted_signal.emit(
            UserType(
                id=self.user_info.id,
                uid=self.uid_input.text(),
                username=self.username_input.text(),
                password=self.password_input.text(),
                two_fa=self.two_fa_input.text(),
                email=self.email_input.text(),
                email_password=self.email_password_input.text(),
                phone_number=self.phone_number_input.text(),
                note=self.note_input.text(),
                type=self.type_input.text(),
                user_group=self.group_input.text(),
                mobile_ua=self.mobile_ua_input.text(),
                desktop_ua=self.desktop_ua_input.text(),
                status=self.status_checkbox.isChecked(),
                created_at=self.created_at_input.text(),
                updated_at=self.updated_at_input.text(),
            )
        )
        self.accept()
