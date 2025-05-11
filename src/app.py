# src/app.py

from src.database.db_user import initialize_db_user
from src.database.db_product import initialize_db_product
from src.models.model_product import MiscProductModel, REProductModel, RETemplateModel
from src.models.model_user import UserModel, ListedProductModel
from src.controllers.controller_user import UserController

from src.views.mainwindow import MainWindow


class Application:
    def __init__(self):
        pass

    def run(self):
        if not initialize_db_product():
            raise Exception("Initialize product database failed!")
        if not initialize_db_user():
            raise Exception("Initialize user database failed!")
        self.mainWindow = MainWindow()
        self.mainWindow.show()
        print("My manager application is running ...")
