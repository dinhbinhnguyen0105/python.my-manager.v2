import sys
from PyQt6.QtWidgets import (
    QApplication,
)
from src.models.re_database import initialize_re_products
from src.views.dialog_re_template_settings import DialogRETemplateSetting

if __name__ == "__main__":
    app = QApplication([])
    initialize_re_products()
    dialog = DialogRETemplateSetting()
    dialog.show()
    sys.exit(app.exec())
