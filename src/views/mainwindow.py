# src/views/mainwindow.py
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, QPoint, QSortFilterProxyModel, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QMenu, QDialog

from src import constants
from src.my_types import UserType
from src.controllers.controller_user import UserController

from src.views.product.page_re_product import PageREProduct
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

        self.setupUi(self)
        self.setWindowTitle("My manager")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setMinimumSize(960, 540)

        self.page_re_product = PageREProduct(self)
        self.page_user = PageUser(self.user_controller.user_service.model, self)
        self.page_user.create_new_user_signal.connect(
            self.user_controller.handle_add_user
        )

        self.content_container.addWidget(self.page_re_product)
        self.content_container.addWidget(self.page_user)
        self.content_container.setCurrentIndex(1)

        self.setup_ui()

    def setup_ui(self):
        pass
