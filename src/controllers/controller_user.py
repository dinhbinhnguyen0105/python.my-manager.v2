# src/controllers/controller_user.py
from typing import Optional, List
from datetime import datetime
import string, secrets
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from src.services.service_user import UserService, ListedProductService
from src.services.check_live import CheckLive
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
        self._current_check_live_process: Optional[CheckLive] = None

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
                self.operation_success_signal.emit(
                    f"Successfully created new user uid '{user_data.uid}'"
                )
                self.data_changed_signal.emit()
                return True
        except Exception as e:
            print(f"[{self.__class__.__name__}.handle_add_user] Error: {e}")
            self.operation_error_signal.emit(
                "Error occurred while create user. Check logs for details."
            )
            return False

    def handle_read_user(self, record_id: int) -> UserType:
        user_data: Optional[UserType] = None
        try:
            user_data = self.user_service.read(record_id)
            if not user_data:
                self.operation_warning_signal.emit(
                    f"Failed to read user (id: {record_id}). Check logs for details."
                )
                return None
            return user_data
        except Exception as e:
            print(f"[{self.__class__.__name__}.handle_read_user] Error: {e}")
            self.operation_error_signal.emit(
                "Error occurred while create user. Check logs for details."
            )
            return user_data

    def handle_update_user(self, record_id: int, user_data: UserType) -> bool:
        try:
            if not isinstance(user_data, UserType):
                raise TypeError(f"Expected UserType, got {type(user_data)}")
            if not self.user_service.update(record_id, user_data):
                self.operation_error_signal.emit(
                    f"Failed to update user {user_data.uid} (id: {record_id}). Check logs for details."
                )
                return False
            else:
                self.operation_success_signal.emit(
                    f"Successfully update user (id: {record_id}) "
                )
                return True
        except Exception as e:
            print(f"[{self.__class__.__name__}.handle_read_user] Error: {e}")
            self.operation_error_signal.emit(
                "Error occurred while create user. Check logs for details."
            )
            return False

    def handle_delete_user(self, record_id) -> bool:
        try:
            if not self.user_service.delete(record_id):
                self.operation_warning_signal.emit(
                    f"Failed to delete user (id: {record_id}). Check logs for details."
                )
                return False
            return True
        except Exception as e:
            print(f"[{self.__class__.__name__}.handle_read_user] Error: {e}")
            self.operation_error_signal.emit(
                "Error occurred while create user. Check logs for details."
            )
            return False

    def handle_new_desktop_ua(self) -> str:
        return self.user_service.handle_new_desktop_ua()

    def handle_new_mobile_ua(self) -> str:
        return self.user_service.handle_new_mobile_ua()

    def handle_new_time(self) -> str:
        return str(datetime.now())

    def handle_new_password(self) -> str:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = "".join(secrets.choice(alphabet) for i in range(30))
        return password

    def handle_check_users(self, selected_ids: List[int]) -> bool:
        list_uid = self.user_service.get_uids_by_record_ids(selected_ids)
        if not list_uid:
            # TODO emit message
            return True
        tasks = list(zip(selected_ids, list_uid))

        if (
            self._current_check_live_process
            and not self._current_check_live_process._check_if_done()
        ):
            print(
                f"[{self.__class__.__name__}.handleCheckUsersRequest] Check Live process is already running. Adding tasks to the queue."
            )
            self._current_check_live_process.add_tasks(tasks)
        else:
            print(
                f"[{self.__class__.__name__}.handleCheckUsersRequest] Starting new Check Live process."
            )
            self._current_check_live_process = CheckLive(self)

            self._current_check_live_process.task_succeeded.connect(
                self._on_check_live_task_succeeded
            )
            self._current_check_live_process.task_failed.connect(
                self._on_check_live_task_failed
            )
            self._current_check_live_process.all_tasks_finished.connect(
                self.check_live_all_tasks_finished
            )

            self._current_check_live_process.add_tasks(tasks)

    @pyqtSlot(int, str, bool)
    def _on_check_live_task_succeeded(self, record_id: int, uid: str, is_live: bool):
        print(f"{record_id} - {uid} : {is_live}")
        self.user_service.update_status(record_id, 1 if is_live else 0)

    @pyqtSlot(int, str, str)
    def _on_check_live_task_failed(self, record_id: int, uid: str, error_message: str):
        # self.operation_error_signal.emit(
        #     f"Error occurred while check live user {uid} (id: {record_id}). Check logs for details."
        # )
        print(f"'{uid}': {error_message}")

    @pyqtSlot()
    def check_live_all_tasks_finished(self):
        self.operation_success_signal.emit("User active status check completed.")
