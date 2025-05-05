# src/views/mainwindow.py
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, QPoint, QSortFilterProxyModel, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QMenu, QDialog

from src import constants
from src.views.product.page_re_product import PageREProduct

from src.ui.mainwindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("My manager")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setMinimumSize(960, 540)

        self.page_re_product = PageREProduct(self)

        self.content_container.addWidget(self.page_re_product)

        self.setup_ui()

    def setup_ui(self):
        pass
