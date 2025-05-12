# src/views/user/dialog_user.py
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIntValidator

from src.my_types import UserType

from src.ui.dialog_user_ui import Ui_Dialog_UserCreate


class DialogUser(QDialog, Ui_Dialog_UserCreate):
    accepted_signal = pyqtSignal(UserType)

    def __init__(self, parent=None):
        super(DialogUser, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.input_widgets = [
            self.uid_input,
            self.username_input,
            self.password_input,
            self.two_fa_input,
            self.email_input,
            self.email_password_input,
            self.phone_number_input,
            self.note_input,
            self.type_input,
            self.group_input,
        ]

        self.group_input.setValidator(QIntValidator())
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.handle_save)

    def handle_save(self):
        self.accepted_signal.emit(
            UserType(
                id=None,
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
                mobile_ua=None,
                desktop_ua=None,
                status=1,
                created_at=None,
                updated_at=None,
            )
        )
        self.accept()

    def clear_field(self):
        for input_widget in self.input_widgets:
            input_widget.setText("")
