# model_product.py
from PyQt6.QtSql import QSqlDatabase

from src import constants
from src.models.base_model import BaseModel


class REProductModel(BaseModel):

    def __init__(self, parent=None):
        db = QSqlDatabase.database(constants.CONNECTION_DB_PRODUCT)
        if not db.isValid() or not db.isOpen():
            warning_msg = f"Warning: Database connection '{constants.CONNECTION_DB_PRODUCT}' is not valid or not open."
            print(warning_msg)
        super().__init__(constants.TABLE_RE_PRODUCT, db, parent)

    def find_row_by_pid(self, pid: str) -> int:
        pid_col_index = self.fieldIndex("pid")
        if pid_col_index == -1:
            print("[BaseModel] 'pid' field not found for search.")
            return -1

        for row in range(self.rowCount()):
            index = self.index(row, pid_col_index)
            if self.data(index) == pid:
                return row
        return -1


class MiscProductModel(BaseModel):

    def __init__(self, parent=None):
        db = QSqlDatabase.database(constants.CONNECTION_DB_PRODUCT)
        if not db.isValid() or not db.isOpen():
            warning_msg = f"Warning: Database connection '{constants.CONNECTION_DB_PRODUCT}' is not valid or not open."
            print(warning_msg)
        super().__init__(constants.TABLE_MISC_PRODUCT, db, parent)

    def find_row_by_pid(self, pid: str) -> int:
        pid_col_index = self.fieldIndex("pid")
        if pid_col_index == -1:
            print("[BaseModel] 'pid' field not found for search.")
            return -1

        for row in range(self.rowCount()):
            index = self.index(row, pid_col_index)
            if self.data(index) == pid:
                return row
        return -1


class RETemplateModel(BaseModel):

    def __init__(self, parent=None):
        db = QSqlDatabase.database(constants.CONNECTION_DB_PRODUCT)
        if not db.isValid() or not db.isOpen():
            warning_msg = f"Warning: Database connection '{constants.CONNECTION_DB_PRODUCT}' is not valid or not open."
            print(warning_msg)
        super().__init__(constants.TABLE_RE_TEMPLATE, db, parent)

    def find_row_by_tid(self, tid: str) -> int:
        tid_col_index = self.fieldIndex("tid")
        if tid_col_index == -1:
            print("[BaseModel] 'tid' field not found for search.")
            return -1

        for row in range(self.rowCount()):
            index = self.index(row, tid_col_index)
            if self.data(index) == tid:
                return row
        return -1
