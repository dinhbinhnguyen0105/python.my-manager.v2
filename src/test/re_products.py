import sys
from PyQt6.QtWidgets import QApplication, QWidget
from src.views.re_product import REProduct
from src.models.re_database import initialize_re_products

if __name__ == "__main__":

    app = QApplication(sys.argv)
    initialize_re_products()

    window = REProduct()
    window.show()
    sys.exit(app.exec())
