# src/services/base_service.py
from datetime import datetime
from typing import List, Any, Dict, Optional, Type
from contextlib import contextmanager
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlRecord
from dataclasses import fields
from src.models.base_model import BaseModel


@contextmanager
def transaction(db: QSqlDatabase):
    if not db.transaction():
        error_msg = (
            f"[{transaction.__name__}] Failed to start transaction. Error: {db.lastError().text()}"
            if db.isOpen()
            else f"[{transaction.__name__}] db not open"
        )
        print()
        raise RuntimeError(error_msg)
    try:
        yield db
        if not db.commit():
            error_msg = (
                f"[{transaction.__name__}] Failed to commit transaction. Error: { db.lastError().text()}"
                if db.isOpen()
                else f"[{transaction.__name__}] db not open"
            )
            print()
            if db.isOpen() and db.transactionActivate():
                db.rollback()
                print(
                    f"[{transaction.__name__}] Attempted rollback after commit failure."
                )
            raise RuntimeError(error_msg)
    except Exception as e:
        print(f"[{transaction.__name__}] Exception during transaction: {e}")
        if db.isOpen() and db.transactionActivate():
            if db.rollback():
                print(f"[{transaction.__name__}] Transaction rolled back.")
            else:
                error_msg = f"[{transaction.__name__}] Failed to rollback transaction. Error: {db.lastError().text()}"
                print(error_msg)


class BaseService:
    DATA_TYPE: Optional[Type[Any]] = None

    def __init__(self, model: BaseModel):
        if not isinstance(model, BaseModel):
            raise TypeError("model mus be an instance of BaseModel or its subclass.")
        self.model = model
        self._db = model.database()

        if not self._db.isValid or not self._db.isOpen():
            warning_msg = f"[{self.__class__.__name__}.__init__] Warning: db connection '{self._db.connectionName()}' is not valid or not open."
            print(warning_msg)

        self._column_names: List[str] = []
        for i in range(self.model.columnCount()):
            col_name = self.model.headerData(
                i,
                Qt.Orientation.Horizontal,
                Qt.ItemDataRole.DisplayRole,
            )
            if isinstance(col_name, str):
                self._column_names.append(col_name)
            else:
                warning_msg = f"[{self.__class__.__name__}.__init__] Warning: Column header at index {i} is not a string: {col_name}."
                print(warning_msg)
        if self.model.fieldIndex("id") == -1:
            warning_msg = f"[{self.__class__.__name__}.__init__] Warning: Table '{self.model.tableName()}' must have an 'id' column for some operations."
            print(warning_msg)
        if self.DATA_TYPE is not None:
            dataclass_fields = [f.name for f in fields(self.DATA_TYPE)]
            for field_name in dataclass_fields:
                warning_msg = f"[{self.__class__.__name__}.__init__] Warning: Field '{field_name}' from DATA_TYPE '{self.DATA_TYPE.__name__}' not found as a column in table '{self.model.tableName()}'."
                print(warning_msg)

    # ========================================================================
    # Helper method
    # ========================================================================
    def _map_record_to_datatype(self, record: QSqlRecord) -> Optional[Any]:
        """Helper to map a QSqlRecord to an instance of the specific DATA_TYPE dataclass."""
        if self.DATA_TYPE is None:
            info_msg = f"[{self.__class__.__name__}._map_record_to_datatype] DATA_TYPE is not set. Cannot map record. => return None"
            print(info_msg)
            return None
        data: Dict[str, Any] = {}
        for i in range(record.count()):
            field_name = record.fieldName(i)
            data[field_name] = record.value(i)
        try:
            dataclass_field_names = {f.name for f in fields(self.DATA_TYPE)}
            valid_data = {field: data.get(field) for field in dataclass_field_names}
            return self.DATA_TYPE(**valid_data)
        except Exception as e:
            error_msg = f"[{self.__class__.__name__}._map_record_to_datatype] Error: converting dict to {self.DATA_TYPE.__name__}: {e} -- Data: {data}"
            print(error_msg)
            return None

    def _fill_row_from_payload(self, row: int, payload: Any):
        """Helper to set data in a model row from a DATA_TYPE payload."""
        if self.DATA_TYPE is None:
            info_msg = f"[{self.__class__.__name__}._fill_row_from_payload] DATA_TYPE is not set. Cannot fill row. => return False"
            print(info_msg)
            return False
        if not isinstance(payload, self.DATA_TYPE):
            info_msg = f"[{self.__class__.__name__}._fill_row_from_payload] Invalid payload type. Expected {self.DATA_TYPE.__name__}, got {type(payload).__name__}. => return False"
            print(info_msg)
            return False
        fields_set_count = 0
        for col_index in range(self.model.columnCount()):
            field_name = self.model.headerData(
                col_index,
                Qt.Orientation.Horizontal,
                Qt.ItemDataRole.DisplayRole,
            )
            if not isinstance(field_name, str):
                continue
            if hasattr(payload, field_name):
                value = getattr(payload, field_name)
                if (
                    field_name == "created_at" or field_name == "updated_at"
                ) and value is None:
                    value = str(datetime.now())
            if field_name != "id":
                index = self.model.index(row, col_index)
                if index.isValid():
                    set_success = self.model.setData(
                        index,
                        value,
                        Qt.ItemDataRole.EditRole,
                    )
                    if set_success:
                        fields_set_count += 1
                    else:
                        warning_msg = f"[{self.__class__.__name__}._fill_row_from_payload] Warning: setData returned False for col '{field_name}' (index {col_index}) at row {row}."
                        print(warning_msg)
                else:
                    warning_msg = f"[{self.__class__.__name__}._fill_row_from_payload] Warning: Invalid index for field '{field_name}' (col index {col_index}) at row {row}. Data not set."
                    print(warning_msg)
        return fields_set_count > 0

    # ========================================================================
    # CRUD method
    # ========================================================================
    def create(self, payload: Any) -> bool:
        if self.DATA_TYPE is None:
            info_msg = f"[{self.__class__.__name__}.create] DATA_TYPE is not set. Cannot create. => return False"
            print(info_msg)
            return False
        if not isinstance(payload, self.DATA_TYPE):
            info_msg = f"[{self.__class__.__name__}.create] Invalid payload type. Expected {self.DATA_TYPE.__name__}, got {type(payload).__name__}. => return False"
            print(info_msg)
            return False
        if not self._db.isOpen():
            info_msg = f"[{self.__class__.__name__}.create] Database is not open. => return False"
            print(info_msg)
            return False

        row = self.model.rowCount()
        if not self.model.insertRow(row):
            error_msg = f"[{self.__class__.__name__}.create] Failed to insert row into model buffer. Error: {self.model.lastError().text()}. => return False"
            print(error_msg)
            return False
        # --- Handle created_at and updated_at if None in payload ---
        self._fill_row_from_payload(row, payload=payload)

        if self.model.submitAll():
            self.model.select()
            return True
        else:
            error_msg = f"[{self.__class__.__name__}.create] Failed to submit changes to database. Error: {self.model.lastError().text()}. => return False"
            self.model.revertAll()
            return False

    def read(self, record_id: int) -> Optional[Any]:
        """Reads a record by ID using the model's find method.
        Returns an instance of DATA_TYPE or None if not found."""
        if self.DATA_TYPE is None:
            info_msg = f"[{self.__class__.__name__}.read] DATA_TYPE is not set. Cannot read. => return None"
            print(info_msg)
            return None
        if not self._db.isOpen():
            info_msg = (
                f"[{self.__class__.__name__}.read] Database is not open. => return None"
            )
            print(info_msg)
            return None
        row = self.model.get_row_by_id(record_id)
        if row != -1:
            record = self.model.record(row)
            return self._map_record_to_datatype(record)
        return None

    def read_all(self) -> List[Any]:
        """Reads all records currently loaded in the model.
        Returns a list of DATA_TYPE instances."""
        if self.DATA_TYPE is None:
            info_msg = f"[{self.__class__.__name__}.read] DATA_TYPE is not set. Cannot read. => return []"
            print(info_msg)
            return []
        if not self._db.isOpen():
            info_msg = (
                f"[{self.__class__.__name__}.read] Database is not open. => return []"
            )
            print(info_msg)
            return []

        results: List[Any] = []
        for row in range(self.model.rowCount()):
            record = self.model.record(row)
            data_instance = self._map_record_to_datatype(record)
            if data_instance is not None:
                results.append(data_instance)
        return results

    def update(self, record_id: Any, payload: Any) -> bool:
        """Updates an existing record by ID from a DATA_TYPE payload using the model.
        Updates only the fields present (not None) in the payload.
        Automatically sets updated_at if it's None in payload and exists as a column.
        Returns True on success, False on failure."""

    def delete(self, record_id: Any) -> bool:
        """Deletes a single record by ID using the model.
        Returns True on success, False on failure."""

    def delete_multiple(self, record_ids: List[Any]) -> bool:
        """Deletes multiple records by IDs using the model within a transaction.
        Returns True on success, False on failure (any failure causes rollback)."""

    def import_data(self, payload: List[Any]) -> bool:
        """Imports multiple records from a list of DATA_TYPE payloads using the model
        within a transaction.
        Returns True on success (all imported), False on failure (rollback).
        Automatically sets created_at and updated_at if they are None in payload
        and exist as columns."""

    def _find_by_model_index(self, find_method_name: str, value: Any) -> Optional[Any]:
        """Helper to find a single record based on a custom find method in the model.
        Intended for use by subclasses to implement methods like find_by_uid, find_by_email.
        find_method_name: The name of the method in the model (e.g., 'find_row_by_uid').
        value: The value to pass to the model's find method."""
