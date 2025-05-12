# src/services/service_user.py
from fake_useragent import UserAgent
from typing import Optional, List
from src.services.base_service import BaseService
from src.models.model_user import UserModel, ListedProductModel
from src.my_types import UserType, ListedProductType


class UserService(BaseService):
    DATA_TYPE = UserType

    def __init__(self, model: UserModel):
        if not isinstance(model, UserModel):
            raise TypeError("model must be an instance of UserModel or its subclass.")
        super().__init__(model)

    def create(self, payload: UserType) -> bool:
        ua_desktop = UserAgent(os="Mac OS X")
        ua_mobile = UserAgent(os="iOS")
        payload.mobile_ua = ua_mobile.random
        payload.desktop_ua = ua_desktop.random
        return super().create(payload)

    def read(self, record_id: int) -> Optional[UserType]:
        return super().read(record_id)

    def read_all(self) -> List[UserType]:
        return super().read_all()

    def update(self, record_id: int, payload: UserType) -> bool:
        return super().update(record_id, payload)

    def delete(self, record_id: int) -> bool:
        return super().delete(record_id)

    def delete_multiple(self, record_ids):
        return super().delete_multiple(record_ids)

    def import_data(self, payload: List[UserType]):
        return super().import_data(payload)

    def find_by_uid(self, uid: str) -> Optional[UserType]:
        return self._find_by_model_index(find_method_name="find_row_by_uid", value=uid)

    def toggle_status(self, user_id: str) -> bool:
        """
        Toggles the status of a user between active (1) and inactive (0).

        Args:
            user_id (str): The unique identifier of the user whose status is to be toggled.

        Returns:
            bool: True if the status was successfully toggled and updated in the database,
                  False otherwise.

        Behavior:
            - If the user with the given ID does not exist, logs an error message and returns False.
            - If the user's current status is 0 (inactive), it will be toggled to 1 (active).
            - If the user's current status is 1 (active), it will be toggled to 0 (inactive).
            - If the user's current status is neither 0 nor 1, logs an error message and returns False.
            - Attempts to update the user's status in the database. Logs success or failure of the update.

        Logs:
            - Logs messages indicating the success or failure of the operation, including unexpected
              status values or database update failures.
        """
        user = self.read(user_id)
        if user is None:
            print(
                f"[{self.__class__.__name__}.toggle_status] User with ID '{user_id}' not found."
            )
            return False
        current_status = user.status
        if current_status == 0:
            new_status = 1
        elif current_status == 1:
            new_status = 0
        else:
            print(
                f"[{self.__class__.__name__}.toggle_status] Unexpected status value for user ID '{user_id}': {current_status}. Cannot toggle."
            )
            return False
        user_db_id = user_id
        user.status = new_status
        update_success = self.update(user_db_id, user)
        if update_success:
            print(
                f"[{self.__class__.__name__}.toggle_status] Successfully toggled status for user ID '{user_id}' to {new_status}."
            )
            return True
        else:
            print(
                f"[{self.__class__.__name__}.toggle_status] Failed to update status for user ID '{user_id}'."
            )
            return False


class ListedProductService(BaseService):
    DATA_TYPE = ListedProductType

    def __init__(self, model: ListedProductModel):
        if not isinstance(model, ListedProductModel):
            raise TypeError(
                "model must be an instance of ListedProductType or its subclass."
            )
        super().__init__(model)
        # self.model = model

    def create(self, payload: ListedProductType):
        return super().create(payload)

    def read(self, record_id: int) -> ListedProductType:
        return super().read(record_id)

    def read_all(self) -> List[ListedProductType]:
        return super().read_all()

    def read_by_user_id(self, user_id: int) -> List[ListedProductType]:
        """
        Retrieves a list of products associated with a specific user ID.

        This method fetches rows from the database corresponding to the given user ID,
        maps each row to the specified data type, and returns the results as a list.

        Args:
            user_id (int): The ID of the user whose associated products are to be retrieved.

        Returns:
            List[ListedProductType]: A list of products associated with the user ID,
            mapped to the specified data type. Returns None if the DATA_TYPE is not set
            or if the database connection is not open.

        Notes:
            - Ensure that the `DATA_TYPE` attribute is set before calling this method.
            - Verify that the database connection is open before invoking this method.
        """
        if self.DATA_TYPE is None:
            info_msg = f"[{self.__class__.__name__}.read_by_user_id] DATA_TYPE is not set. Cannot read. => return None"
            print(info_msg)
            return None
        if not self._db.isOpen():
            info_msg = f"[{self.__class__.__name__}.read_by_user_id] Database is not open. => return None"
            print(info_msg)
            return None
        rows = self.model.get_rows_by_user_id(user_id)
        results = []
        for row in rows:
            record = self.model.record(row)
            results.append(self._map_record_to_datatype(record))
        return results

    def shift_record_by_user_id(self, user_id: int) -> Optional[ListedProductType]:
        """
        Removes a record associated with the given user ID from the model and database.

        This method retrieves rows associated with the specified `user_id` from the model,
        removes the corresponding row, and submits the changes to the database. If the
        operation is successful, the removed record is returned. Otherwise, appropriate
        error messages are logged, and the method returns `None` or `False` depending on
        the failure scenario.

        Args:
            user_id (int): The ID of the user whose record is to be removed.

        Returns:
            Optional[ListedProductType]: The removed record if the operation is successful.
            Returns `None` if the `DATA_TYPE` is not set or the database is not open.
            Returns `False` if the record is not found, the row removal fails, or the
            submission of changes fails.

        Notes:
            - The method checks if `DATA_TYPE` is set and if the database connection is open
              before proceeding.
            - If the record is not found or an error occurs during row removal or submission,
              appropriate error messages are printed to the console.
            - If the submission of changes fails, the model's changes are reverted.

        Raises:
            None
        """
        if self.DATA_TYPE is None:
            info_msg = f"[{self.__class__.__name__}.shift_record_by_user_id] DATA_TYPE is not set. Cannot read. => return None"
            print(info_msg)
            return None
        if not self._db.isOpen():
            info_msg = f"[{self.__class__.__name__}.shift_record_by_user_id] Database is not open. => return None"
            print(info_msg)
            return None
        rows_to_remove = self.model.get_rows_by_user_id(user_id)
        if not rows_to_remove:
            info_msg = f"[{self.__class__.__name__}.shift_record_by_user_id] No record found for user ID {user_id}."
            print(info_msg)
            return None
        row_index_to_remove = rows_to_remove[0]
        try:
            record_to_return = self.model.record(row_index_to_remove)
            removed_data_instance = self._map_record_to_datatype(record_to_return)
            if removed_data_instance is None:
                error_msg = f"[{self.__class__.__name__}.shift_record_by_user_id] Failed to map record to DATA_TYPE for row {row_index_to_remove}."
                print(error_msg)
                return None

        except IndexError:
            error_msg = f"[{self.__class__.__name__}.shift_record_by_user_id] Invalid row index {row_index_to_remove} after finding rows."
            print(error_msg)
            return None
        if not self.model.removeRow(row_index_to_remove):
            error_msg = f"[{self.__class__.__name__}.shift_record_by_user_id] Failed to remove row {row_index_to_remove} from model buffer. Error: {self.model.lastError().text()}"
            print(error_msg)
            self.model.revertAll()
            return None

        if self.model.submitAll():
            return removed_data_instance
        else:
            error_msg = f"[{self.__class__.__name__}.shift_record_by_user_id] Failed to submit deletion for row {row_index_to_remove}. Error: {self.model.lastError().text()}"
            print(error_msg)
            self.model.revertAll()
            self.model.select()
            return None


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from src.database.db_user import initialize_db_user
    from src.database.db_product import initialize_db_product
    from src.models.model_user import UserModel
    from src.models.model_product import REProductModel
    from src.my_types import UserType

    app = QApplication([])
    if initialize_db_user() and initialize_db_product():
        user_model = UserModel()
        user_service = UserService(user_model)

        # user_payload: List[UserType] = [
        #     UserType(
        #         id=None,
        #         uid="uid_test_user_00",
        #         username="username_test_user_00",
        #         password="password_test_user_00",
        #         two_fa="two_fa_test_user_00",
        #         email="email_test_user_00",
        #         email_password="email_password_test_user_00",
        #         phone_number="phone_number_test_user_00",
        #         note="note_test_user_00",
        #         type="type_test_user_00",
        #         user_group=1,
        #         mobile_ua="mobile_ua_test_user_00",
        #         desktop_ua="desktop_ua_test_user_00",
        #         status=1,
        #         created_at="2025-05-11 01:52:59.538249",
        #         updated_at="2025-05-11 01:52:59.538249",
        #     ),
        #     UserType(
        #         id=None,
        #         uid="uid_test_user_01",
        #         username="username_test_user_01",
        #         password="password_test_user_01",
        #         two_fa="two_fa_test_user_01",
        #         email="email_test_user_01",
        #         email_password="email_password_test_user_01",
        #         phone_number="phone_number_test_user_01",
        #         note="note_test_user_01",
        #         type="type_test_user_01",
        #         user_group=1,
        #         mobile_ua="mobile_ua_test_user_01",
        #         desktop_ua="desktop_ua_test_user_01",
        #         status=1,
        #         created_at="2025-05-11 01:52:59.538249",
        #         updated_at="2025-05-11 01:52:59.538249",
        #     ),
        #     UserType(
        #         id=None,
        #         uid="uid_test_user_02",
        #         username="username_test_user_02",
        #         password="password_test_user_02",
        #         two_fa="two_fa_test_user_02",
        #         email="email_test_user_02",
        #         email_password="email_password_test_user_02",
        #         phone_number="phone_number_test_user_02",
        #         note="note_test_user_02",
        #         type="type_test_user_02",
        #         user_group=1,
        #         mobile_ua="mobile_ua_test_user_02",
        #         desktop_ua="desktop_ua_test_user_02",
        #         status=1,
        #         created_at="2025-05-11 01:52:59.538249",
        #         updated_at="2025-05-11 01:52:59.538249",
        #     ),
        #     UserType(
        #         id=None,
        #         uid="uid_test_user_03",
        #         username="username_test_user_03",
        #         password="password_test_user_03",
        #         two_fa="two_fa_test_user_03",
        #         email="email_test_user_03",
        #         email_password="email_password_test_user_03",
        #         phone_number="phone_number_test_user_03",
        #         note="note_test_user_03",
        #         type="type_test_user_03",
        #         user_group=1,
        #         mobile_ua="mobile_ua_test_user_03",
        #         desktop_ua="desktop_ua_test_user_03",
        #         status=1,
        #         created_at="2025-05-11 01:52:59.538249",
        #         updated_at="2025-05-11 01:52:59.538249",
        #     ),
        # ]
        # user_service.import_data(payload=user_payload)
        user_service.toggle_status(4)
        _all = user_service.read_all()
        for user in _all:
            print(user)

        # listed_payload: List[ListedProductType] = [
        #     ListedProductType(
        #         id=None,
        #         user_id=1,
        #         pid="pid_test_01",
        #         created_at=None,
        #         updated_at=None,
        #     )
        # ]

        # listed_model = ListedProductModel()
        # listed_service = ListedProductService(listed_model)
        # print(listed_service.shift_record_by_user_id(1))
        # # print(listed_service.create(listed_payload[0]))
        # _all = listed_service.read_by_user_id(1)
        # # _all = listed_service.read_all()
        # for listed in _all:
        #     print(listed)
