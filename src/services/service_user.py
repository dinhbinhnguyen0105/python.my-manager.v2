# src/services/service_user.py
from fake_useragent import UserAgent
from typing import Optional, List
from src.services.base_service import BaseService
from src.models.model_user import (
    UserModel,
    ListedProductModel,
    UserSettingProxyModel,
    UserSettingUDDModel,
)
from src.my_types import (
    UserType,
    ListedProductType,
    UserSettingProxyType,
    UserSettingUDDType,
)


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

    def update_status(self, record_id: int, new_status: int) -> bool:
        """
        Updates the status of a user.

        Args:
            record_id (int): The unique identifier of the user whose status is to be updated.
            new_status (int): The new status to set for the user. Must be either 0 or 1.

        Returns:
            bool: True if the status update was successful, False otherwise.

        Raises:
            ValueError: If `new_status` is not 0 or 1.

        Logs:
            Logs a success message if the status update is successful.
            Logs a failure message if the status update fails.
        """
        if new_status not in [0, 1]:
            raise ValueError(
                f"Invalid status value: {new_status}. Status must be 0 or 1."
            )
        user = self.read(record_id)
        user.status = new_status
        update_success = self.update(record_id, user)
        if update_success:
            print(
                f"[{self.__class__.__name__}.update_status] Successfully toggled status for user ID '{record_id}' to {new_status}."
            )
            return True
        else:
            print(
                f"[{self.__class__.__name__}.update_status] Failed to update status for user ID '{record_id}'."
            )
            return False

    def get_uids_by_record_ids(self, record_ids: List[int]) -> List[str]:
        return self.model.get_uids_by_record_ids(record_ids)

    def handle_new_desktop_ua(self) -> str:
        ua_desktop = UserAgent(os="Mac OS X")
        return ua_desktop.random

    def handle_new_mobile_ua(self) -> str:
        ua_mobile = UserAgent(os="iOS")
        return ua_mobile.random


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

    def delete(self, record_id: int) -> bool:
        return super().delete(record_id)

    def delete_multiple(self, record_ids):
        return super().delete_multiple(record_ids)

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


class UserSettingUDDService(BaseService):
    DATA_TYPE = UserSettingUDDType

    def __init__(self, model: UserSettingUDDModel):
        if not isinstance(model, UserSettingUDDModel):
            raise TypeError(
                "model must be an instance of UserSettingUDDType or its subclass."
            )
        super().__init__(model)

    def read(self, record_id: int) -> UserSettingUDDType:
        return super().read(record_id)

    def create(self, payload: UserSettingUDDType):
        return super().create(payload)

    def read_all(self) -> List[UserSettingUDDType]:
        return super().read_all()

    def delete(self, record_id: int) -> bool:
        return super().delete(record_id)

    def delete_multiple(self, record_ids):
        return super().delete_multiple(record_ids)

    def set_selected(self, record_id: int) -> bool:
        udds = self.read_all()
        for udd in udds:
            udd.is_selected = 0
            self.update(udd.id, udd)

        current_udd = self.read(record_id)
        current_udd.is_selected = 1
        update_success = self.update(record_id, current_udd)
        if update_success:
            print(
                f"[{self.__class__.__name__}.set_selected] Successfully toggled status for udd ID '{record_id}' to 1."
            )
            return True
        else:
            print(
                f"[{self.__class__.__name__}.set_selected] Failed to update status for udd ID '{record_id}'."
            )
            return False

    def get_selected(self) -> Optional[str]:
        udds = self.read_all()
        for udd in udds:
            if udd.is_selected == 1:
                return udd.value
        return None


class UserSettingProxyService(BaseService):
    DATA_TYPE = UserSettingProxyType

    def __init__(self, model: UserSettingProxyModel):
        if not isinstance(model, UserSettingProxyModel):
            raise TypeError(
                "model must be an instance of UserSettingProxyType or its subclass."
            )
        super().__init__(model)

    def create(self, payload: UserSettingProxyType):
        return super().create(payload)

    def read_all(self) -> List[UserSettingProxyType]:
        return super().read_all()

    def delete(self, record_id: int) -> bool:
        return super().delete(record_id)

    def delete_multiple(self, record_ids):
        return super().delete_multiple(record_ids)
