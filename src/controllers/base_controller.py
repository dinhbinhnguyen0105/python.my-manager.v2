from typing import Any, Optional, Type
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QModelIndex
from PyQt6.QtWidgets import (
    QDataWidgetMapper,
    QWidget,
)  # Import QWidget for type hinting
from PyQt6.QtSql import QSqlRecord  # Import QSqlRecord

# Import BaseModel
from src.models.base_model import BaseModel

# Import BaseServiceWithModel
from src.services.base_service import BaseServiceWithModel

# Import your specific types and services if needed for examples or type hinting in subclasses
# from src.my_types import UserType, ...
# from src.services.service_user import UserService, ...


class BaseController(QObject):
    """
    Base class for controllers that manage a BaseModel (QSqlTableModel)
    and bind UI widgets using QDataWidgetMapper.
    Requires subclasses to define DATA_TYPE.
    """

    # Class attribute to hold the specific data type (dataclass)
    # Subclasses MUST set this attribute
    DATA_TYPE: Optional[Type[Any]] = None

    # Signal emitted when the currently mapped record changes
    # Emits a dictionary representing the data of the current record
    current_record_changed = pyqtSignal(dict)

    def __init__(self, service: BaseServiceWithModel, parent: Optional[QObject] = None):
        """
        Initializes the BaseController with a service instance.
        """
        super().__init__(parent)
        if not isinstance(service, BaseServiceWithModel):
            raise TypeError(
                "service must be an instance of BaseServiceWithModel or its subclass."
            )

        self.service = service  # Store the service instance
        self.model = service.model  # Get the model instance from the service

        # Ensure DATA_TYPE is set in the subclass
        if self.DATA_TYPE is None:
            raise NotImplementedError(
                "BaseController subclasses must define DATA_TYPE class attribute."
            )
        # Ensure the service's DATA_TYPE matches or is compatible
        if (
            self.service.DATA_TYPE is not None
            and self.service.DATA_TYPE != self.DATA_TYPE
        ):
            print(
                f"[{self.__class__.__name__}.__init__] WARNING: Service DATA_TYPE ({self.service.DATA_TYPE.__name__}) does not match Controller DATA_TYPE ({self.DATA_TYPE.__name__})."
            )
            # Decide if this should be a strict error or just a warning

        self.mapper = QDataWidgetMapper(self)
        self._initialize_mapper()

    def _initialize_mapper(self):
        """Sets up the QDataWidgetMapper."""
        self.mapper.setModel(self.model)
        # Set submit policy to manual so changes are buffered until submitAll() is called
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        # Connect signal to update UI based on current index
        self.mapper.currentIndexChanged.connect(self._on_current_index_changed)

        # Initial load of data and set mapper index
        # Note: Load data should ideally be called after UI is visible or ready
        # self.load_data() # Moved to a separate method/called externally

    def bind_ui_widgets(self, **widgets_mapping: QWidget):
        """
        Binds UI widgets to model columns using QDataWidgetMapper.
        widgets_mapping: A dictionary where keys are model field names (str)
                         and values are QWidget instances.
        """
        if self.model.columnCount() == 0:
            print(
                f"[{self.__class__.__name__}.bind_ui_widgets] Model has no columns loaded. Cannot bind widgets."
            )
            return

        # Clear any existing mappings before adding new ones
        self.mapper.clearMapping()

        for field_name, widget in widgets_mapping.items():
            # Find the column index for the field name in the model
            column = self.model.fieldIndex(field_name)
            if column != -1:
                # Add mapping for the widget to the specified column
                # QDataWidgetMapper handles different widget types automatically (QLineEdit, QSpinBox, QComboBox etc.)
                self.mapper.addMapping(widget, column)
                # print(f"[{self.__class__.__name__}.bind_ui_widgets] Bound widget {type(widget).__name__} to field '{field_name}' (column {column}).") # Optional debug print
            else:
                print(
                    f"[{self.__class__.__name__}.bind_ui_widgets] WARNING: Field '{field_name}' not found as a column in model '{self.model.tableName()}'. Widget not bound."
                )

    @pyqtSlot(int)
    def _on_current_index_changed(self, index: int):
        """Slot connected to mapper.currentIndexChanged."""
        # When mapper index changes, get the record data and emit a signal
        # This allows UI/other components to update based on the current record
        print(
            f"[{self.__class__.__name__}._on_current_index_changed] Current index changed to {index}."
        )
        if index != -1:
            record = self.model.record(index)
            # Convert QSqlRecord to a dictionary to emit
            data = {}
            for i in range(record.count()):
                field_name = record.fieldName(i)
                # Use value() to get Python native type
                data[field_name] = record.value(i)
            # print(f"[{self.__class__.__name__}._on_current_index_changed] Emitting current_record_changed with data for index {index}.") # Optional debug print
            self.current_record_changed.emit(data)  # Emit signal with record data
        else:
            # Handle case when index is -1 (e.g., empty model)
            print(
                f"[{self.__class__.__name__}._on_current_index_changed] Mapper index is -1 (empty model?). Emitting empty dict."
            )
            self.current_record_changed.emit({})  # Emit empty dict or None

    def load_data(self):
        """Loads/refreshes data in the model from the database and sets mapper to first record."""
        print(f"[{self.__class__.__name__}.load_data] Loading data from database...")
        if self.model.select():  # Select data from the database
            print(
                f"[{self.__class__.__name__}.load_data] Data loaded successfully. Row count: {self.model.rowCount()}"
            )
            if self.model.rowCount() > 0:
                self.mapper.setCurrentIndex(0)  # Set mapper to the first record
                print(f"[{self.__class__.__name__}.load_data] Mapper set to index 0.")
            else:
                self.mapper.setCurrentIndex(-1)  # No records, set mapper to -1
                print(
                    f"[{self.__class__.__name__}.load_data] Model is empty. Mapper set to index -1."
                )
            return True
        else:
            print(
                f"[{self.__class__.__name__}.load_data] Failed to load data. Error: {self.model.lastError().text()}"
            )
            # Handle error display in UI (e.g., via a signal from controller)
            self.mapper.setCurrentIndex(-1)  # Ensure mapper is reset on error
            return False

    def submit_changes(self) -> bool:
        """
        Submits changes from the mapper buffer to the model, then submits model changes to the database.
        Returns True on success, False on failure.
        """
        print(
            f"[{self.__class__.__name__}.submit_changes] Attempting to submit changes from mapper."
        )
        if self.mapper.submit():  # Submit changes from widgets to the model buffer
            print(
                f"[{self.__class__.__name__}.submit_changes] Changes submitted to model buffer from mapper."
            )
            # Now submit the model's buffered changes to the database
            print(
                f"[{self.__class__.__name__}.submit_changes] Model is dirty before submitAll: {self.model.isDirty()}"
            )  # Debug print
            if self.model.submitAll():
                print(
                    f"[{self.__class__.__name__}.submit_changes] Model changes saved to database."
                )
                # Optionally re-select to get auto-generated IDs or updated timestamps
                # self.model.select() # Often needed after submitAll for inserts
                # QMessageBox.information(None, "Success", "Changes saved.") # UI messages in Controller/UI
                print(
                    f"[{self.__class__.__name__}.submit_changes] Model is dirty after successful submitAll: {self.model.isDirty()}"
                )  # Should be False
                return True
            else:
                print(
                    f"[{self.__class__.__name__}.submit_changes] Database error during submitAll: {self.model.lastError().text()}"
                )
                self.model.revertAll()  # Revert model changes on DB error
                # QMessageBox.critical(None, "Error", f"Database error: {self.model.lastError().text()}") # UI messages in Controller/UI
                print(
                    f"[{self.__class__.__name__}.submit_changes] Model is dirty after failed submitAll and revertAll: {self.model.isDirty()}"
                )  # Should be False
                return False
        else:
            print(
                f"[{self.__class__.__name__}.submit_changes] Could not submit changes from mapper to model buffer."
            )
            # QMessageBox.warning(None, "Warning", "Could not submit changes from UI.") # UI messages in Controller/UI
            # Changes were not even moved to the model buffer, no need to revert model
            print(
                f"[{self.__class__.__name__}.submit_changes] Model is dirty after failed mapper.submit(): {self.model.isDirty()}"
            )
            return False  # Mapper submit failed

    # =========================================================================
    # Navigation Methods
    # =========================================================================

    @pyqtSlot()
    def first_record(self):
        """Navigates to the first record."""
        self.mapper.toFirst()

    @pyqtSlot()
    def previous_record(self):
        """Navigates to the previous record."""
        self.mapper.toPrevious()

    @pyqtSlot()
    def next_record(self):
        """Navigates to the next record."""
        self.mapper.toNext()

    @pyqtSlot()
    def last_record(self):
        """Navigates to the last record."""
        self.mapper.toLast()

    @pyqtSlot(int)
    def go_to_record(self, row: int):
        """Navigates to a specific record by row index."""
        if 0 <= row < self.model.rowCount():
            self.mapper.setCurrentIndex(row)
        else:
            print(f"[{self.__class__.__name__}.go_to_record] Invalid row index: {row}")
