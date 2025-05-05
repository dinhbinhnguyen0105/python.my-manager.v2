# model_user.py
from PyQt6.QtSql import QSqlDatabase

from src import constants
from src.models.base_model import BaseModel


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
            print("[BaseModel] 'uid' field not found for search.")
            return -1

        for row in range(self.rowCount()):
            index = self.index(row, uid_col_index)
            if self.data(index) == uid:
                return row
        return -1


class ListedProductModel(BaseModel):

    def __init__(self, parent=None):
        db = QSqlDatabase.database(constants.CONNECTION_DB_USER)
        if not db.isValid() or not db.isOpen():
            warning_msg = f"Warning: Database connection '{constants.CONNECTION_DB_USER}' is not valid or not open."
            print(warning_msg)
        super().__init__(constants.TABLE_LISTED_PRODUCT, db, parent)
