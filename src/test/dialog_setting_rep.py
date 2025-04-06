import sys
from PyQt6.QtWidgets import (
    QApplication,
)
from src.models.re_database import initialize_re_products
from src.views.dialog_re_product_settings import DialogREProductSetting

if __name__ == "__main__":
    app = QApplication([])
    initialize_re_products()
    dialog = DialogREProductSetting()
    dialog.show()
    sys.exit(app.exec())
