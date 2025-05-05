# src/services/base_service.py
from datetime import datetime
from typing import List, Any, Dict, Optional, Type
from contextlib import contextmanager
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlRecord

from src.models.base_model import BaseModel


@contextmanager
def transaction(db: QSqlDatabase):
    if not db.transaction():
        error_text = db.lastError().text() if db.isOpen() else "DB not open"
        print(f"[DB_TRANSACTION] Failed to start transaction. Error: {error_text}")

        raise RuntimeError(f"Failed to start transaction: {error_text}")
    try:
        yield db
        if not db.commit():
            error_text = db.lastError().text() if db.isOpen() else "DB not open"
            print(f"[DB_TRANSACTION] Failed to commit transaction. Error: {error_text}")

            if db.isOpen() and db.transactionActive():
                db.rollback()
                print("[DB_TRANSACTION] Attempted rollback after commit failure.")
            raise RuntimeError(f"Failed to commit transaction: {error_text}")
    except Exception as e:
        print(f"[DB_TRANSACTION] Exception during transaction: {e}")
        if db.isOpen() and db.transactionActive():
            if db.rollback():
                print("[DB_TRANSACTION] Transaction rolled back.")
            else:
                print(
                    f"[DB_TRANSACTION] Failed to rollback transaction. Rollback Error: {db.lastError().text()}"
                )
        raise


class BaseService:
    DATA_TYPE: Optional[Type[Any]] = None

    def __init__(self, model: BaseModel):
        """
        Initializes the BaseService with a BaseModel instance.
        """
        if not isinstance(model, BaseModel):
            raise TypeError("model must be an instance of BaseModel or its subclass.")

        self.model = model  # Store the BaseModel instance
        self._db = model.database()  # Get the database connection from the model

        # Check if DB is open and valid
        if not self._db.isValid() or not self._db.isOpen():
            print(
                f"[{self.__class__.__name__}.__init__] WARNING: Database connection '{self._db.connectionName()}' is not valid or not open."
            )
            # Depending on your app structure, you might raise an error or handle this.

        # Get column names from the model's schema
        self._column_names: List[str] = []
        for i in range(self.model.columnCount()):
            col_name = self.model.headerData(
                i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            if isinstance(col_name, str):  # Ensure it's a string
                self._column_names.append(col_name)
            else:
                print(
                    f"[{self.__class__.__name__}.__init__] WARNING: Column header at index {i} is not a string: {col_name}"
                )

        # Ensure essential columns exist (check using fieldIndex)
        if self.model.fieldIndex("id") == -1:
            print(
                f"[{self.__class__.__name__}.__init__] Error: Table '{self.model.tableName()}' must have an 'id' column for some operations."
            )
        # Check for other required columns based on DATA_TYPE if needed
        if self.DATA_TYPE is not None:
            from dataclasses import fields

            dataclass_fields = [f.name for f in fields(self.DATA_TYPE)]
            for field_name in dataclass_fields:
                if self.model.fieldIndex(field_name) == -1:
                    print(
                        f"[{self.__class__.__name__}.__init__] WARNING: Field '{field_name}' from DATA_TYPE '{self.DATA_TYPE.__name__}' not found as a column in table '{self.model.tableName()}'."
                    )

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _map_record_to_datatype(self, record: QSqlRecord) -> Optional[Any]:
        """Helper to map a QSqlRecord to an instance of the specific DATA_TYPE dataclass."""
        if self.DATA_TYPE is None:
            print(
                f"[{self.__class__.__name__}._map_record_to_datatype] DATA_TYPE is not set. Cannot map record."
            )
            return None

        data: Dict[str, Any] = {}
        # Iterate through the record's fields
        for i in range(record.count()):
            field_name = record.fieldName(i)
            # Use value() which handles different DB types and NULLs correctly
            data[field_name] = record.value(i)

        # Filter dictionary keys to match dataclass fields to avoid errors
        # if the database record has more columns than the dataclass definition
        try:
            from dataclasses import fields

            dataclass_field_names = {f.name for f in fields(self.DATA_TYPE)}
            valid_data = {field: data.get(field) for field in dataclass_field_names}

            # Create and return an instance of the specific dataclass
            return self.DATA_TYPE(**valid_data)
        except Exception as e:
            print(
                f"[{self.__class__.__name__}._map_record_to_datatype] Error converting dict to {self.DATA_TYPE.__name__}: {e} -- Data: {data}"
            )
            # Depending on strictness, you might raise the exception or return None
            return None

    def _fill_row_from_payload(self, row: int, payload: Any):
        """Helper to set data in a model row from a DATA_TYPE payload."""
        if self.DATA_TYPE is None:
            print(
                f"[{self.__class__.__name__}._fill_row_from_payload] DATA_TYPE is not set. Cannot fill row."
            )
            return False

        if not isinstance(payload, self.DATA_TYPE):
            print(
                f"[{self.__class__.__name__}._fill_row_from_payload] Invalid payload type. Expected {self.DATA_TYPE.__name__}, got {type(payload).__name__}."
            )
            return False

        # print(f"[{self.__class__.__name__}._fill_row_from_payload] Filling data for row {row}...") # Optional debug print

        fields_set_count = 0
        # Iterate through the model's columns to set data
        for col_index in range(self.model.columnCount()):
            field_name = self.model.headerData(
                col_index, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            if not isinstance(field_name, str):  # Skip if column name is not a string
                continue

            # Check if the field exists in the payload dataclass
            if hasattr(payload, field_name):
                value = getattr(payload, field_name)

                # Decide whether to set data for None values or not
                # Setting None will attempt to set DB field to NULL
                # Omitting None means DB DEFAULTs might be used
                # Let's set data even if value is None, allowing explicit NULL
                # Also, typically don't set 'id' as it's AUTOINCREMENT
                if field_name != "id":
                    index = self.model.index(row, col_index)
                    if index.isValid():
                        # print(f"[{self.__class__.__name__}._fill_row_from_payload] Setting data for col '{field_name}' (index {col_index}) at row {row} with value: {value}") # Optional debug print
                        set_success = self.model.setData(
                            index, value, Qt.ItemDataRole.EditRole
                        )
                        if set_success:
                            fields_set_count += 1
                        else:
                            print(
                                f"[{self.__class__.__name__}._fill_row_from_payload] WARNING: setData returned False for col '{field_name}' (index {col_index}) at row {row}."
                            )
                    else:
                        print(
                            f"[{self.__class__.__name__}._fill_row_from_payload] WARNING: Invalid index for field '{field_name}' (col index {col_index}) at row {row}. Data not set."
                        )
            # else:
            # print(f"[{self.__class__.__name__}._fill_row_from_payload] Field '{field_name}' not found in payload DATA_TYPE.") # Optional debug print

        # print(f"[{self.__class__.__name__}._fill_row_from_payload] Attempted to set data for {fields_set_count} fields for row {row}.") # Optional debug print
        return fields_set_count > 0  # Return True if at least one field was set

    # =========================================================================
    # CRUD Operations using QSqlTableModel
    # =========================================================================

    # Changed to instance method
    def create(self, payload: Any) -> bool:  # Accept DATA_TYPE instance
        """
        Creates a new record from a DATA_TYPE payload using the model.
        Returns True on success, False on failure.
        Automatically sets created_at and updated_at if they are None in payload
        and exist as columns.
        """
        if self.DATA_TYPE is None:
            print(
                f"[{self.__class__.__name__}.create] DATA_TYPE is not set. Cannot create."
            )
            return False
        if not isinstance(payload, self.DATA_TYPE):
            print(
                f"[{self.__class__.__name__}.create] Invalid payload type. Expected {self.DATA_TYPE.__name__}, got {type(payload).__name__}."
            )
            return False
        if not self._db.isOpen():
            print(f"[{self.__class__.__name__}.create] Database is not open.")
            return False

        row = self.model.rowCount()  # Get the index for the new row
        # print(f"[{self.__class__.__name__}.create] Attempting to insert new row at index {row}.") # Optional debug print

        # Insert a new row into the model's buffer
        if not self.model.insertRow(row):
            print(
                f"[{self.__class__.__name__}.create] Failed to insert row into model buffer. Error: {self.model.lastError().text()}"
            )
            return False
        # print(f"[{self.__class__.__name__}.create] Row successfully inserted into model buffer at index {row}.") # Optional debug print

        # --- Handle created_at and updated_at if None in payload ---
        current_time_str = str(datetime.now())
        payload.created_at = current_time_str
        payload.updated_at = current_time_str
        # Iterate through model columns to find created_at and updated_at indices
        created_at_col_index = self.model.fieldIndex("created_at")
        updated_at_col_index = self.model.fieldIndex("updated_at")

        if created_at_col_index != -1:
            # Check if payload has 'created_at' attribute and if its value is None
            if (
                hasattr(payload, "created_at")
                and getattr(payload, "created_at") is None
            ):
                index = self.model.index(row, created_at_col_index)
                if index.isValid():
                    self.model.setData(
                        index, current_time_str, Qt.ItemDataRole.EditRole
                    )
                    # print(f"[{self.__class__.__name__}.create] Set created_at for row {row} to {current_time_str}") # Optional debug print

        if updated_at_col_index != -1:
            # Check if payload has 'updated_at' attribute and if its value is None
            if (
                hasattr(payload, "updated_at")
                and getattr(payload, "updated_at") is None
            ):
                index = self.model.index(row, updated_at_col_index)
                if index.isValid():
                    self.model.setData(
                        index, current_time_str, Qt.ItemDataRole.EditRole
                    )
                    # print(f"[{self.__class__.__name__}.create] Set updated_at for row {row} to {current_time_str}") # Optional debug print
        # --- End Handle created_at and updated_at ---

        # Fill data into the newly inserted row for other fields
        # This will overwrite created_at/updated_at if they were explicitly set in payload
        # and are not None. If they were None, the above logic handled them.
        fields_set = self._fill_row_from_payload(row, payload=payload)

        # If no fields were set (e.g., empty payload or no matching columns),
        # the model might not be marked as dirty for this row.
        # However, insertRow itself usually marks the model as dirty.
        # Let's rely on submitAll to figure it out.

        # Submit changes to the database
        # print(f"[{self.__class__.__name__}.create] Attempting to submit changes to database for row {row}.") # Optional debug print
        if self.model.submitAll():
            # print(f"[{self.__class__.__name__}.create] Successfully created record.") # Optional debug print
            # After successful submission, the model is updated.
            # We might need to re-select or fetch the new ID if needed immediately.
            # self.model.select() # Uncomment if you need the model to refresh immediately after creation
            return True
        else:
            print(
                f"[{self.__class__.__name__}.create] Failed to submit changes to database. Error: {self.model.lastError().text()}"
            )
            # Revert changes if submission fails
            self.model.revertAll()
            return False

    # Changed to instance method
    def read(
        self, record_id: Any
    ) -> Optional[Any]:  # Return type is Optional[DATA_TYPE]
        """
        Reads a record by ID using the model's find method.
        Returns an instance of DATA_TYPE or None if not found.
        """
        if self.DATA_TYPE is None:
            print(
                f"[{self.__class__.__name__}.read] DATA_TYPE is not set. Cannot read."
            )
            return None
        if not self._db.isOpen():
            print(f"[{self.__class__.__name__}.read] Database is not open.")
            return None

        # Use the model's find_row_by_id method (assuming it exists in BaseModel)
        row = self.model.find_row_by_id(record_id)

        if row != -1:
            record = self.model.record(row)
            # Convert QSqlRecord to the specific DATA_TYPE
            return self._map_record_to_datatype(record)

        # print(f"[{self.__class__.__name__}.read] No record with id={record_id} found in model.") # Optional logging
        return None  # Record not found in the model

    # Changed to instance method
    def read_all(self) -> List[Any]:  # Return type is List[DATA_TYPE]
        """
        Reads all records currently loaded in the model.
        Returns a list of DATA_TYPE instances.
        """
        if self.DATA_TYPE is None:
            print(
                f"[{self.__class__.__name__}.read_all] DATA_TYPE is not set. Cannot read all."
            )
            return []

        # Ensure model is up-to-date. select() might be needed if external changes occurred.
        # self.model.select() # Uncomment if you need to refresh data from DB before listing

        results: List[Any] = []
        for row in range(self.model.rowCount()):
            record = self.model.record(row)
            # Convert each QSqlRecord to the specific DATA_TYPE
            data_instance = self._map_record_to_datatype(record)
            if data_instance is not None:  # Only add if conversion was successful
                results.append(data_instance)

        # print(f"[{self.__class__.__name__}.read_all] Retrieved {len(results)} from model.") # Optional logging
        return results

    # Changed to instance method
    def update(self, record_id: Any, payload: Any) -> bool:  # Accept DATA_TYPE instance
        """
        Updates an existing record by ID from a DATA_TYPE payload using the model.
        Updates only the fields present (not None) in the payload.
        Automatically sets updated_at if it's None in payload and exists as a column.
        Returns True on success, False on failure.
        """
        if self.DATA_TYPE is None:
            print(
                f"[{self.__class__.__name__}.update] DATA_TYPE is not set. Cannot update."
            )
            return False
        if not isinstance(payload, self.DATA_TYPE):
            print(
                f"[{self.__class__.__name__}.update] Invalid payload type. Expected {self.DATA_TYPE.__name__}, got {type(payload).__name__}."
            )
            return False
        if not self._db.isOpen():
            print(f"[{self.__class__.__name__}.update] Database is not open.")
            return False

        # Use the model's find_row_by_id method
        row = self.model.find_row_by_id(record_id)
        if row == -1:
            print(
                f"[{self.__class__.__name__}.update] Record with id {record_id} not found in model."
            )
            return False

        # print(f"[{self.__class__.__name__}.update] Model is dirty BEFORE update setData: {self.model.isDirty()}") # Optional debug print
        fields_updated_count = 0

        # Iterate through the model's columns to set data
        for col_index in range(self.model.columnCount()):
            field_name = self.model.headerData(
                col_index, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            if not isinstance(field_name, str):
                continue

            # Check if the field exists in the payload dataclass AND its value is NOT None
            # Also, typically don't update the 'id' field
            if hasattr(payload, field_name) and field_name != "id":
                value = getattr(payload, field_name)
                # Only set data if the value is explicitly provided (not None)
                if value is not None:
                    index = self.model.index(row, col_index)
                    if index.isValid():
                        # print(f"[{self.__class__.__name__}.update] Setting data for col '{field_name}' (index {col_index}) at row {row} with value: {value}") # Optional debug print
                        set_success = self.model.setData(
                            index, value, Qt.ItemDataRole.EditRole
                        )
                        if set_success:
                            fields_updated_count += 1
                        else:
                            print(
                                f"[{self.__class__.__name__}.update] WARNING: setData returned False for col '{field_name}' (index {col_index}) at row {row}."
                            )
                    else:
                        print(
                            f"[{self.__class__.__name__}.update] WARNING: Invalid index for field '{field_name}' (col index {col_index}) at row {row}. Data not set."
                        )
            # Handle 'updated_at' automatically if it's a column and its value in payload is None

            elif (
                field_name == "updated_at"
                and hasattr(payload, "updated_at")
                and getattr(payload, "updated_at") is None
            ):
                # Check if 'updated_at' is a valid column in the model
                index = self.model.index(row, col_index)
                if index.isValid():
                    current_value = self.model.data(index, Qt.ItemDataRole.EditRole)
                    new_value = str(datetime.now())
                    # Only update if the current value is different
                    if (
                        str(current_value) != new_value
                    ):  # Convert current_value to string for comparison
                        # print(f"[{self.__class__.__name__}.update] Setting updated_at for row {row}: {new_value}") # Optional debug print
                        set_success = self.model.setData(
                            index, new_value, Qt.ItemDataRole.EditRole
                        )
                        if set_success:
                            fields_updated_count += 1
                        else:
                            print(
                                f"[{self.__class__.__name__}.update] WARNING: setData returned False for updated_at at row {row}."
                            )

        # print(f"[{self.__class__.__name__}.update] Attempted to update {fields_updated_count} fields for row {row}.") # Optional debug print
        # print(f"[{self.__class__.__name__}.update] Model is dirty AFTER update setData: {self.model.isDirty()}") # Optional debug print

        # Submit changes to the database
        if fields_updated_count > 0 and self.model.submitAll():
            # print(f"[{self.__class__.__name__}.update] Successfully updated record with id: {record_id}") # Optional debug print
            # self.model.select() # Optional: re-select to refresh view if needed
            return True
        elif fields_updated_count == 0:
            # print(f"[{self.__class__.__name__}.update] No fields provided in payload to update for id: {record_id}.") # Optional logging
            # If no fields were updated, it's technically a success from the service perspective
            # but the DB wasn't touched. Return True or False based on desired behavior.
            # Returning True indicates no error occurred, just no changes were applied.
            return True
        else:
            print(
                f"[{self.__class__.__name__}.update] Failed to submit update. Error: {self.model.lastError().text()}"
            )
            self.model.revertAll()  # Discard changes
            return False

    # Changed to instance method
    def delete(self, record_id: Any) -> bool:
        """
        Deletes a single record by ID using the model.
        Returns True on success, False on failure.
        """
        if not self._db.isOpen():
            print(f"[{self.__class__.__name__}.delete] Database is not open.")
            return False

        # Use the model's find_row_by_id method
        row = self.model.find_row_by_id(record_id)
        if row == -1:
            print(
                f"[{self.__class__.__name__}.delete] Record with id {record_id} not found in model for deletion."
            )
            return False

        # print(f"[{self.__class__.__name__}.delete] Model is dirty BEFORE removeRow: {self.model.isDirty()}") # Optional debug print
        # Remove the row from the model buffer
        if not self.model.removeRow(row):
            print(
                f"[{self.__class__.__name__}.delete] Failed to remove row {row} from model buffer. Error: {self.model.lastError().text()}"
            )
            return False
        # print(f"[{self.__class__.__name__}.delete] Row {row} successfully removed from model buffer.") # Optional debug print
        # print(f"[{self.__class__.__name__}.delete] Model is dirty AFTER removeRow: {self.model.isDirty()}") # Optional debug print

        # Submit the deletion to the database
        # print(f"[{self.__class__.__name__}.delete] Attempting to submit deletion to database for row {row}.") # Optional debug print
        if self.model.submitAll():
            # print(f"[{self.__class__.__name__}.delete] Successfully deleted record with id: {record_id}") # Optional debug print
            # self.model.select() # Re-select to refresh the model and view
            return True
        else:
            print(
                f"[{self.__class__.__name__}.delete] Failed to submit deletion. Error: {self.model.lastError().text()}"
            )
            self.model.revertAll()  # Revert the removal from the model buffer
            return False

    # Changed to instance method
    def delete_multiple(
        self, record_ids: List[Any]
    ) -> bool:  # Accept List[Any] for IDs
        """
        Deletes multiple records by IDs using the model within a transaction.
        Returns True on success, False on failure (any failure causes rollback).
        """
        if not self._db.isOpen():
            print(f"[{self.__class__.__name__}.delete_multiple] Database is not open.")
            return False

        if not record_ids:
            print(
                f"[{self.__class__.__name__}.delete_multiple] No record IDs provided."
            )
            return True  # Consider it success if nothing needed deletion

        # Find row indices for the given IDs
        # Sort in reverse order so removing rows doesn't affect indices of rows still to be removed
        rows_to_delete = sorted(
            [
                self.model.find_row_by_id(db_id)
                for db_id in record_ids
                if self.model.find_row_by_id(db_id) != -1
            ],
            reverse=True,
        )

        if not rows_to_delete:
            print(
                f"[{self.__class__.__name__}.delete_multiple] None of the provided IDs were found in the model."
            )
            return True  # Consider it success if no records matched IDs

        # print(f"[{self.__class__.__name__}.delete_multiple] Model is dirty BEFORE transaction: {self.model.isDirty()}") # Optional debug print
        try:
            # Use the transaction context manager (wraps submitAll)
            # Note: QSqlTableModel's submitAll often uses its own transaction.
            # Wrapping submitAll calls in an explicit transaction might be necessary
            # if you mix model operations with QSqlQuery or need atomicity across multiple submitAlls.
            # For simplicity here, let's wrap the removeRow + submitAll sequence.
            with transaction(self._db):
                # print(f"[{self.__class__.__name__}.delete_multiple] Transaction started.") # Optional debug print
                for row in rows_to_delete:
                    # print(f"[{self.__class__.__name__}.delete_multiple] Attempting to remove row {row} from model buffer.") # Optional debug print
                    # Remove row from model buffer. removeRow doesn't submit immediately.
                    if not self.model.removeRow(row):
                        # If removing from buffer fails, raise an error to trigger rollback
                        error_text = self.model.lastError().text()
                        print(
                            f"[{self.__class__.__name__}.delete_multiple] Failed to remove row {row} from model buffer. Error: {error_text}"
                        )
                        raise RuntimeError(
                            f"Failed to remove row from model: {error_text}"
                        )
                    # print(f"[{self.__class__.__name__}.delete_multiple] Row {row} removed from model buffer.") # Optional debug print

                # Submit all pending deletions in the buffer to the database within the transaction
                # print(f"[{self.__class__.__name__}.delete_multiple] Attempting to submit all pending deletions.") # Optional debug print
                if not self.model.submitAll():
                    # If submitAll fails, this error is caught by the transaction context manager
                    error_text = self.model.lastError().text()
                    print(
                        f"[{self.__class__.__name__}.delete_multiple] Failed to submit deletions. Error: {error_text}"
                    )
                    raise RuntimeError(f"Failed to submit deletions: {error_text}")
                # print(f"[{self.__class__.__name__}.delete_multiple] submitAll for deletions successful.") # Optional debug print

            # Transaction committed successfully if we reach here
            # print(f"[{self.__class__.__name__}.delete_multiple] Transaction committed successfully.") # Optional debug print
            # Re-select to refresh the model and view after successful deletion
            self.model.select()
            # print(f"[{self.__class__.__name__}.delete_multiple] Model is dirty AFTER successful transaction and select: {self.model.isDirty()}") # Should be False
            # print(f"[{self.__class__.__name__}.delete_multiple] Successfully deleted {len(record_ids)} records.") # Optional logging
            return True

        except Exception as e:
            # The transaction context manager handles the rollback and re-raises the exception
            print(
                f"[{self.__class__.__name__}.delete_multiple] Transaction failed: {e}"
            )
            # Revert changes in the model buffer and reload data state before failed transaction
            self.model.revertAll()
            self.model.select()
            # print(f"[{self.__class__.__name__}.delete_multiple] Model is dirty AFTER failed transaction, revertAll, and select: {self.model.isDirty()}") # Should be False
            return False

    # Changed to instance method
    def import_data(self, payload: List[Any]) -> bool:  # Accept List[DATA_TYPE]
        """
        Imports multiple records from a list of DATA_TYPE payloads using the model
        within a transaction.
        Returns True on success (all imported), False on failure (rollback).
        Automatically sets created_at and updated_at if they are None in payload
        and exist as columns.
        """
        if self.DATA_TYPE is None:
            print(
                f"[{self.__class__.__name__}.import_data] DATA_TYPE is not set. Cannot import."
            )
            return False
        if not all(isinstance(item, self.DATA_TYPE) for item in payload):
            print(
                f"[{self.__class__.__name__}.import_data] Invalid payload list type. Expected list of {self.DATA_TYPE.__name__}."
            )
            return False

        if not payload:
            print(f"[{self.__class__.__name__}.import_data] Empty payload list.")
            return True  # Consider it success if no data

        if not self._db.isOpen():
            print(f"[{self.__class__.__name__}.import_data] Database is not open.")
            return False

        # print(f"[{self.__class__.__name__}.import_data] Model is dirty BEFORE transaction: {self.model.isDirty()}") # Optional debug print
        try:
            # Use a single transaction for the entire import process
            with transaction(self._db):
                # print(f"[{self.__class__.__name__}.import_data] Transaction started.") # Optional debug print
                current_time_str = str(datetime.now())  # Get time once for the batch

                for record_instance in payload:
                    row = (
                        self.model.rowCount()
                    )  # Get the index for the new row at the end
                    # print(f"[{self.__class__.__name__}.import_data] Attempting to insert row {row} into model buffer.") # Optional debug print
                    if not self.model.insertRow(row):
                        # If inserting row into buffer fails, raise an error to trigger rollback
                        error_text = self.model.lastError().text()
                        print(
                            f"[{self.__class__.__name__}.import_data] Failed to insert row into model buffer. Error: {error_text}"
                        )
                        raise RuntimeError(
                            f"Failed to insert row into model: {error_text}"
                        )
                    # print(f"[{self.__class__.__name__}.import_data] Row {row} inserted into model buffer.") # Optional debug print

                    # --- Handle created_at and updated_at if None in payload for this record ---
                    created_at_col_index = self.model.fieldIndex("created_at")
                    updated_at_col_index = self.model.fieldIndex("updated_at")

                    # if

                    if created_at_col_index != -1:
                        if (
                            hasattr(record_instance, "created_at")
                            and getattr(record_instance, "created_at") is None
                        ):
                            index = self.model.index(row, created_at_col_index)
                            if index.isValid():
                                self.model.setData(
                                    index, current_time_str, Qt.ItemDataRole.EditRole
                                )
                                # print(f"[{self.__class__.__name__}.import_data] Set created_at for row {row} to {current_time_str}") # Optional debug print

                    if updated_at_col_index != -1:
                        if (
                            hasattr(record_instance, "updated_at")
                            and getattr(record_instance, "updated_at") is None
                        ):
                            index = self.model.index(row, updated_at_col_index)
                            if index.isValid():
                                self.model.setData(
                                    index, current_time_str, Qt.ItemDataRole.EditRole
                                )
                                # print(f"[{self.__class__.__name__}.import_data] Set updated_at for row {row} to {current_time_str}") # Optional debug print
                    # --- End Handle created_at and updated_at ---

                    # Fill data into the newly inserted row in the buffer for other fields
                    # This will overwrite created_at/updated_at if they were explicitly set and not None.
                    self._fill_row_from_payload(row, record_instance)
                    # print(f"[{self.__class__.__name__}.import_data] Data filled for row {row}.") # Optional debug print

                # Submit all pending insertions in the buffer to the database within the transaction
                # print(f"[{self.__class__.__name__}.import_data] Attempting to submit all pending insertions.") # Optional debug print
                if not self.model.submitAll():
                    # If submitAll fails, this error is caught by the transaction context manager
                    error_text = self.model.lastError().text()
                    print(
                        f"[{self.__class__.__name__}.import_data] Failed to submit insertions. Error: {error_text}"
                    )
                    raise RuntimeError(f"Failed to submit insertions: {error_text}")
                # print(f"[{self.__class__.__name__}.import_data] submitAll for insertions successful.") # Optional debug print

            # Transaction committed successfully if we reach here
            # print(f"[{self.__class__.__name__}.import_data] Transaction committed successfully.") # Optional debug print
            # Re-select to refresh the model and view after successful import
            self.model.select()
            # print(f"[{self.__class__.__name__}.import_data] Model is dirty AFTER successful transaction and select: {self.model.isDirty()}") # Should be False
            # print(f"[{self.__class__.__name__}.import_data] Successfully imported {len(payload)} records.") # Optional logging
            return True

        except Exception as e:
            # The transaction context manager handles the rollback and re-raises the exception
            print(f"[{self.__class__.__name__}.import_data] Transaction failed: {e}")
            # Revert changes in the model buffer and reload data state before failed transaction
            self.model.revertAll()
            self.model.select()
            # print(f"[{self.__class__.__name__}.import_data] Model is dirty AFTER failed transaction, revertAll, and select: {self.model.isDirty()}") # Should be False
            return False

    # =========================================================================
    # Helper for specific find methods (Optional, can be implemented in subclasses)
    # These helpers use the model's find methods, not QSqlQuery directly
    # =========================================================================
    def _find_one_by_model_index(
        self, find_method_name: str, value: Any
    ) -> Optional[Any]:  # Return Optional[DATA_TYPE]
        """
        Helper to find a single record based on a custom find method in the model.
        Intended for use by subclasses to implement methods like find_by_uid, find_by_email.
        find_method_name: The name of the method in the model (e.g., 'find_row_by_uid').
        value: The value to pass to the model's find method.
        """
        if self.DATA_TYPE is None:
            print(
                f"[{self.__class__.__name__}._find_one_by_model_index] DATA_TYPE is not set. Cannot find record."
            )
            return None

        # Get the find method from the model instance
        find_method = getattr(self.model, find_method_name, None)
        if find_method is None or not callable(find_method):
            print(
                f"[{self.__class__.__name__}._find_one_by_model_index] Error: Model does not have a callable method named '{find_method_name}'."
            )
            return None

        # Call the model's find method to get the row index
        row = find_method(value)

        if row != -1:
            record = self.model.record(row)
            # Convert QSqlRecord to the specific DATA_TYPE
            return self._map_record_to_datatype(record)

        # print(f"[{self.__class__.__name__}._find_one_by_model_index] No record found for {find_method_name} with value '{value}' in model.") # Optional logging
        return None  # Record not found in the model

    # Note: Finding *many* records based on a condition using *only* QSqlTableModel's
    # in-memory data might not be efficient or accurate if the full dataset isn't loaded.
    # QSqlTableModel's select() can apply filters, but that's different from
    # iterating through filtered results. If you need to find many based on a condition
    # efficiently, using QSqlQuery directly (like in your original BaseService)
    # or a QSortFilterProxyModel might be better.
    # For now, let's omit a _find_many_by_model_index helper as it's less common
    # to filter many records from the model's in-memory cache compared to querying the DB.
    # If needed, it would involve iterating through model rows and checking the condition
    # manually or applying a QSortFilterProxyModel.
