# src/app.py

from src.database.db_user import initialize_db_user
from src.database.db_product import initialize_db_product
from src.models.model_product import MiscProductModel, REProductModel, RETemplateModel
from src.models.model_user import UserModel, ListedProductModel
from src.services.service_user import UserService, ListedProductService
from src.controllers.controller_user import UserController

from src.views.mainwindow import MainWindow


class Application:
    def __init__(self):
        if not initialize_db_product():
            raise Exception("Initialize product database failed!")
        if not initialize_db_user():
            raise Exception("Initialize user database failed!")
        self.user_model = UserModel()
        self.listed_product_model = ListedProductModel()
        self.user_service = UserService(self.user_model)
        self.listed_product_service = ListedProductService(self.listed_product_model)
        self.user_controller = UserController(
            self.user_service, self.listed_product_service
        )
        self.mainWindow = MainWindow(user_controller=self.user_controller)
        self.mainWindow.show()
        print("My manager application is running ...")
