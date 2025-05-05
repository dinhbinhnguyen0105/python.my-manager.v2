# src/views/re/dialog_re_product.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from src import constants
from src.ui.dialog_re_product_ui import Ui_DialogREProduct


class DialogREProduct(QDialog, Ui_DialogREProduct):
    def __init__(self, parent=None):
        super(DialogREProduct, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Real Estate")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
