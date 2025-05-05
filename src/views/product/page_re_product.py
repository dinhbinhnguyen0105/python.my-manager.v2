# src/views/product/page_re.py
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, QPoint, QSortFilterProxyModel, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QWidget, QMenu, QDialog

from src import constants
from src.ui.page_re_product_ui import Ui_PageREProduct


class PageREProduct(QWidget, Ui_PageREProduct):
    def __init__(self, parent=None):
        super(PageREProduct, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Real Estate Product")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
