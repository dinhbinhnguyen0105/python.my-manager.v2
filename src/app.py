# src/app.py

from src.database.db_user import initialize_db_user
from src.database.db_product import initialize_db_product
from src.models.model_product import MiscProductModel, REProductModel, RETemplateModel
from src.models.model_user import (
    UserModel,
    ListedProductModel,
    UserSettingProxyModel,
    UserSettingUDDModel,
    UserActionModel,
)
from src.services.service_user import (
    UserService,
    ListedProductService,
    UserSettingUDDService,
    UserSettingProxyService,
    UserActionService,
)
from src.services.service_robot import RobotService
from src.controllers.controller_user import (
    UserController,
    UserSettingUDDController,
    UserSettingProxyController,
    UserActionController,
)
from src.controllers.controller_robot import RobotController

from src.views.mainwindow import MainWindow


class Application:
    def __init__(self):
        if not initialize_db_product():
            raise Exception("Initialize product database failed!")
        if not initialize_db_user():
            raise Exception("Initialize user database failed!")
        self.user_model = UserModel()
        self.user_setting_udd_model = UserSettingUDDModel()
        self.user_setting_proxy_model = UserSettingProxyModel()
        self.listed_product_model = ListedProductModel()
        self.user_action_model = UserActionModel()

        self.user_service = UserService(self.user_model)
        self.user_action_service = UserActionService(self.user_action_model)
        self.user_setting_proxy_service = UserSettingProxyService(
            self.user_setting_proxy_model
        )
        self.user_setting_udd_service = UserSettingUDDService(
            self.user_setting_udd_model
        )
        self.listed_product_service = ListedProductService(self.listed_product_model)

        self.user_controller = UserController(self.user_service)
        self.user_action_controller = UserActionController(self.user_action_service)
        self.user_setting_proxy_controller = UserSettingProxyController(
            self.user_setting_proxy_service
        )
        self.user_setting_udd_controller = UserSettingUDDController(
            self.user_setting_udd_service
        )

        self.robot_controller = RobotController(
            self.user_service,
            self.user_setting_proxy_service,
            self.user_setting_udd_service,
            self.user_action_service,
        )

        self.mainWindow = MainWindow(
            user_controller=self.user_controller,
            setting_udd_controller=self.user_setting_udd_controller,
            setting_proxy_controller=self.user_setting_proxy_controller,
            robot_controller=self.robot_controller,
            user_action_controller=self.user_action_controller,
        )
        self.mainWindow.show()
        print("My manager application is running ...")
