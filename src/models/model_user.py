# src/models/model_user.py
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel

from src import constants
from src.models.base_model import BaseModel
from typing import List, Optional


class UserModel(BaseModel):

    def __init__(self, parent=None):
        db = QSqlDatabase.database(constants.CONNECTION_DB_USER)
        if not db.isValid() or not db.isOpen():
            warning_msg = f"Warning: Database connection '{constants.CONNECTION_DB_USER}' is not valid or not open."
            print(warning_msg)
        super().__init__(constants.TABLE_USER, db, parent)

    def find_row_by_uid(self, uid: str) -> int:
        uid_col_index = self.fieldIndex("uid")
        if uid_col_index == -1:
            print(
                f"[{self.__class__.__name__}.find_row_by_uid] 'uid' field not found for search."
            )
            return -1

        for row in range(self.rowCount()):
            index = self.index(row, uid_col_index)
            if self.data(index) == uid:
                return row
        return -1

    def get_uids_by_record_ids(self, record_ids: List[int]) -> List[str]:
        """
        Get the 'uid' values for the given list of record IDs.

        Args:
            record_ids (List[int]): List of record IDs.

        Returns:
            List[str]: List of 'uid' values corresponding to the record IDs.
        """
        uid_col_index = self.fieldIndex("uid")
        id_col_index = self.fieldIndex("id")
        if uid_col_index == -1 or id_col_index == -1:
            print(
                f"[{self.__class__.__name__}.get_uids_by_record_ids] 'uid' or 'id' field not found for search."
            )
            return []

        uids = []
        for row in range(self.rowCount()):
            id_index = self.index(row, id_col_index)
            uid_index = self.index(row, uid_col_index)
            if self.data(id_index) in record_ids:
                uids.append(self.data(uid_index))
        return uids


class ListedProductModel(BaseModel):

    def __init__(self, parent=None):
        db = QSqlDatabase.database(constants.CONNECTION_DB_USER)
        if not db.isValid() or not db.isOpen():
            warning_msg = f"Warning: Database connection '{constants.CONNECTION_DB_USER}' is not valid or not open."
            print(warning_msg)
        super().__init__(constants.TABLE_LISTED_PRODUCT, db, parent)

    def get_rows_by_user_id(self, user_id: int) -> Optional[int]:
        """
        Get all rows in the model where the "user_id" field matches the given user_id.

        Args:
            user_id (str): The user ID to search for.

        Returns:
            Optional[int]: A list of row indices where the "user_id" matches the given value.
                           Returns [] if the "user_id" field is not found in the model.
        """
        user_id_col_index = self.fieldIndex("user_id")
        if user_id_col_index == -1:
            print(
                f"[{self.__class__.__name__}.get_rows_by_user_id] 'user_id' field not found for search."
            )
            return -1
        rows = []
        for row in range(self.rowCount()):
            index = self.index(row, user_id_col_index)
            if self.data(index) == user_id:
                rows.append(row)
        return rows


class UserSettingProxyModel(BaseModel):

    def __init__(self, parent=None):
        db = QSqlDatabase.database(constants.CONNECTION_DB_USER)
        if not db.isValid() or not db.isOpen():
            warning_msg = f"Warning: Database connection '{constants.CONNECTION_DB_USER}' is not valid or not open."
            print(warning_msg)
        super().__init__(constants.TABLE_USER_SETTING_PROXY, db, parent)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)


class UserSettingUDDModel(BaseModel):

    def __init__(self, parent=None):
        db = QSqlDatabase.database(constants.CONNECTION_DB_USER)
        if not db.isValid() or not db.isOpen():
            warning_msg = f"Warning: Database connection '{constants.CONNECTION_DB_USER}' is not valid or not open."
            print(warning_msg)
        super().__init__(constants.TABLE_USER_SETTING_UDD, db, parent)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)


class UserActionModel(BaseModel):
    def __init__(self, parent=None):
        db = QSqlDatabase.database(constants.CONNECTION_DB_USER)
        if not db.isValid() or not db.isOpen():
            warning_msg = f"Warning: Database connection '{constants.CONNECTION_DB_USER}' is not valid or not open."
            print(warning_msg)
        super().__init__(constants.TABLE_ROBOT_ACTION, db, parent)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
