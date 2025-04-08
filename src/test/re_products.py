import sys
from PyQt6.QtWidgets import QApplication, QWidget
from src.views.re_product import REProduct
from src.models.re_database import inittialize_re_database

if __name__ == "__main__":

    app = QApplication(sys.argv)
    if not inittialize_re_database():
        exit()

    window = REProduct()
    window.show()
    sys.exit(app.exec())
