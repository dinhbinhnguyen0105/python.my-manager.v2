from PyQt6.QtCore import QObject, pyqtSignal
from src.services.service_user import UserService, ListedProductService
from src.my_types import UserType, ListedProductType


class UserController(QObject):
    operation_success_signal = pyqtSignal(str)
    operation_error_signal = pyqtSignal(str)
    operation_warning_signal = pyqtSignal(str)
    data_changed_signal = pyqtSignal()

    def __init__(
        self, user_service: UserService, listed_product_service: ListedProductService
    ):
        super().__init__()
        self.user_service = user_service
        self.listed_product_service = listed_product_service

    def handle_add_user(self, user_data: UserType):
        try:
            if not isinstance(user_data, UserType):
                raise TypeError(f"Expected UserType, got {type(user_data)}")
            if self.user_service.find_by_uid(user_data.uid):
                self.operation_warning_signal.emit(
                    f"User with UID '{user_data.uid}' already exists."
                )
                return False
            if not self.user_service.create(user_data):
                self.operation_error_signal.emit(
                    "Failed to create new user. Check logs for details."
                )
                return False
            else:
                self.operation_success_signal.emit("Successfully created new user. id ")
            return True
        except Exception as e:
            print(f"[{self.__class__.__name__}.handle_add_user] Error: {e}")
            self.operation_error_signal.emit(
                "Error occurred while create user. Check logs for details."
            )
            return False
