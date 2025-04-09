# src/controllers/re_controller.py
import uuid
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QDataWidgetMapper

from src import constants
from src.models.re_model import BaseSettingModel
from src.services.re_service import (
    RESettingService,
    REProductService,
    RETemplateService,
)


class REProductController(QObject):
    current_record_changed = pyqtSignal(dict)

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.mapper = QDataWidgetMapper(self)
        self._initialize_mapper()

    def _initialize_mapper(self):
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(
            QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.mapper.currentIndexChanged.connect(self._on_current_index_changed)
        self.load_data()

    def bind_ui_widgets(self, **widgets_mapping):
        for field, widget in widgets_mapping.items():
            column = self.model.fieldIndex(field)
            if column != -1:
                self.mapper.addMapping(widget, column)

    def _on_current_index_changed(self, index):
        if index != -1:
            record = self.model.record(index)
            data = {}
            for i in range(record.count()):
                data[record.fieldName(i)] = record.value(i)
            self.current_record_changed.emit(data)

    def load_data(self):
        self.model.select()
        self.mapper.setCurrentIndex(0)  # Hiển thị bản ghi đầu tiên

    def submit_changes(self):
        if self.mapper.submit():
            if self.model.submitAll():
                QMessageBox.information(None, "Success", "Changes saved.")
                return True
            else:
                QMessageBox.critical(
                    None, "Error", f"Database error: {self.model.lastError().text()}"
                )
                return False
        else:
            QMessageBox.warning(
                None, "Warning", "Could not submit changes from UI.")
            return False

    @staticmethod
    def generate_pid(option):
        try:
            while True:
                uuid_str = str(uuid.uuid4())
                pid = uuid_str.replace("-", "")[:8]
                if option.lower() == "sell":
                    pid = "S." + pid
                elif option.lower() == "rent":
                    pid = "R." + pid
                elif option.lower() == "assignment":
                    pid = "A." + pid
                else:
                    raise ValueError("Invalid option")
                pid = ("RE." + pid).lower()
                if not REProductService.check_unique_pid(pid):
                    return pid
                else:
                    continue
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            raise Exception("Failed to generate PID.")

    @staticmethod
    def validate_new_product(data):
        if not len(data.get("image_paths")):
            QMessageBox.critical(None, "Error", "Invalid images.")
            return False
        if not data.get("pid"):
            QMessageBox.critical(None, "Error", "Invalid pid.")
            return False
        if (
            not isinstance(data.get("area"), (int, float))
            or not isinstance(data.get("structure"), (int, float))
            or not isinstance(data.get("price"), (int, float))
        ):
            QMessageBox.critical(
                None, "Error", "Area, structure, and price must be numbers."
            )
            return False
        if not RESettingService.check_exist_id(
            constants.RE_SETTING_STATUS_TABLE, data.get("status_id")
        ):
            QMessageBox.critical(None, "Error", "Invalid status selected.")
            return False
        if not RESettingService.check_exist_id(
            constants.RE_SETTING_PROVINCES_TABLE, data.get("province_id")
        ):
            QMessageBox.critical(None, "Error", "Invalid province selected.")
            return False
        if not RESettingService.check_exist_id(
            constants.RE_SETTING_DISTRICTS_TABLE, data.get("district_id")
        ):
            QMessageBox.critical(None, "Error", "Invalid district selected.")
            return False
        if not RESettingService.check_exist_id(
            constants.RE_SETTING_WARDS_TABLE, data.get("ward_id")
        ):
            QMessageBox.critical(None, "Error", "Invalid ward selected.")
            return False
        if not RESettingService.check_exist_id(
            constants.RE_SETTING_OPTIONS_TABLE, data.get("option_id")
        ):
            QMessageBox.critical(None, "Error", "Invalid option selected.")
            return False
        if not RESettingService.check_exist_id(
            constants.RE_SETTING_CATEGORIES_TABLE, data.get("category_id")
        ):
            QMessageBox.critical(None, "Error", "Invalid category selected.")
            return False
        if not RESettingService.check_exist_id(
            constants.RE_SETTING_BUILDING_LINES_TABLE, data.get(
                "building_line_id")
        ):
            QMessageBox.critical(
                None, "Error", "Invalid building_line selected.")
            return False
        if not RESettingService.check_exist_id(
            constants.RE_SETTING_FURNITURES_TABLE, data.get("furniture_id")
        ):
            QMessageBox.critical(None, "Error", "Invalid furniture selected.")
            return False
        if not RESettingService.check_exist_id(
            constants.RE_SETTING_LEGALS_TABLE, data.get("legal_id")
        ):
            QMessageBox.critical(None, "Error", "Invalid legal selected.")
            return False
        return True

    def add_product(self, data):
        data.setdefault("image_paths", [])
        data.setdefault("area", 0.0)
        data.setdefault("structure", 0.0)
        data.setdefault("function", "")
        data.setdefault("street", "")
        data.setdefault("description", "")
        data.setdefault("price", 0.0)
        try:
            if not self.validate_new_product(data):
                return False
            if len(data.get("image_paths")) < 1:
                QMessageBox.critical(None, "Error", "Invalid images.")
                return False
            if REProductService.create(data):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "Real estate product added successfully."
                )
                return True
            else:
                QMessageBox.critical(
                    None, "Error", "Failed to create new real estate product."
                )
                return False

        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return False

    def read_product(self, record_id):
        try:
            product = REProductService.read(record_id)
            if not product:
                QMessageBox.warning(None, "Warning", "Product not found.")
            return product
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return None

    def read_all_product(self):
        try:
            return REProductService.read_all()
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return []

    def update_product(self, record_id, data):
        data.setdefault("image_path", [])
        data.setdefault("area", 0.0)
        data.setdefault("structure", 0.0)
        data.setdefault("function", "")
        data.setdefault("description", "")
        data.setdefault("price", 0.0)
        try:
            if not self.validate_new_product(data):
                return False
            if REProductService.update(record_id, data):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "Real estate product updated successfully."
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to update product.")
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return False

    def delete_product(self, record_id):
        try:
            if REProductService.delete(record_id):
                self.model.select()
                QMessageBox.information(
                    None, "Success", "Real estate product deleted successfully."
                )
                return True
            else:
                QMessageBox.warning(
                    None, "Warning", "Failed to delete product.")
                return False
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            return False

    @staticmethod
    def get_image_paths(record_id):
        return REProductService.get_images_in_directory(record_id)

    @staticmethod
    def get_columns():
        return REProductService.get_columns()


class RESettingController(QObject):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.model = BaseSettingModel(self.table_name)

    def create_new(self, data: dict):
        try:
            record_id = RESettingService.create(self.table_name, data)
            if record_id:
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", "Failed to create new record.")
        except Exception as e:
            error_msg = f"Error creating new record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def get(self, record_id: int):
        try:
            return RESettingService.read(self.table_name, record_id)
        except Exception as e:
            error_msg = f"Error reading record: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return None

    def update(self, record_id: int, data: dict):
        try:
            if RESettingService.update(self.table_name, record_id, data):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", f"Failed to update record with ID: {record_id}."
                )
        except Exception as e:
            error_msg = f"Error updating record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def delete(self, record_id: int):
        try:
            if RESettingService.delete(self.table_name, record_id):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", f"Failed to delete record with ID: {record_id}."
                )
        except Exception as e:
            error_msg = f"Error deleting record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def get_all(self):
        try:
            return RESettingService.read_all(self.table_name)
        except Exception as e:
            error_msg = f"Error fetching all records: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return []

    @staticmethod
    def static_get_all(table_name):
        try:
            return RESettingService.read_all(table_name)
        except Exception as e:
            error_msg = f"Error fetching all records: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return []

    @staticmethod
    def static_get_id_by_value(table_name, value):
        try:
            return RESettingService.get_id_by_value(table_name, value)
        except Exception as e:
            error_msg = f"Error fetching id: {e}"
            QMessageBox.critical(None, "Error", error_msg)


class RETemplateController(QObject):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.model = BaseSettingModel(self.table_name)

    def create_new(self, data):
        if not data.get("value"):
            QMessageBox.critical(
                None, "Error", f"Input field cannot be empty.")
        try:
            tid = self.generate_tid()
            result = RETemplateService.create(
                self.table_name,
                {"tid": tid, "value": data.get(
                    "value"), "option_id": data.get("option_id")},
            )
            self.model.select()
            return result
        except Exception as e:
            error_msg = f"Error creating new record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def get(self, record_id: int):
        try:
            return RETemplateService.read(self.table_name, record_id)
        except Exception as e:
            error_msg = f"Error reading record: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return None

    @staticmethod
    def get(table_name, record_id):
        try:
            return RETemplateService.read(table_name, record_id)
        except Exception as e:
            error_msg = f"Error reading record: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return None

    def update(self, record_id: int, data: dict):
        try:
            if RETemplateService.update(self.table_name, record_id, data):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", f"Failed to update record with ID: {record_id}."
                )
        except Exception as e:
            error_msg = f"Error updating record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def delete(self, record_id: int):
        try:
            if RETemplateService.delete(self.table_name, record_id):
                self.model.select()
            else:
                QMessageBox.critical(
                    None, "Error", f"Failed to delete record with ID: {record_id}."
                )
        except Exception as e:
            error_msg = f"Error deleting record: {e}"
            QMessageBox.critical(None, "Error", error_msg)

    def get_all(self):
        try:
            return RETemplateService.read_all(self.table_name)
        except Exception as e:
            error_msg = f"Error fetching all records: {e}"
            QMessageBox.critical(None, "Error", error_msg)
            return []

    def generate_tid(self):
        try:
            while True:
                uuid_str = str(uuid.uuid4())
                tid = uuid_str.replace("-", "")[:8]
                if self.table_name == constants.RE_TEMPLATE_TITLE_TABLE:
                    tid = "T.T." + tid
                elif self.table_name == constants.RE_TEMPLATE_DESCRIPTION_TABLE:
                    tid = "T.D." + tid
                if not RETemplateService.is_tid_existed(self.table_name, tid):
                    return tid
                else:
                    continue
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
            raise Exception("Failed to generate TID.")

    @staticmethod
    def get_ids(table_name, option_id=-1):
        # ids = RETemplateService.get_ids(table_name)
        # if option_id == -1:
        #     return ids
        # else:
        #     new_ids = []
        #     for id in ids:
        #         if id.get("option_id")
        return RETemplateService.get_ids(table_name, option_id)

    # @staticmethod
    # def get_ids(table_name, option):
    #     pass
