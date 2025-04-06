# src/views/dialog_re_product_settings.py

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QMessageBox, QTableView

from src.ui.dialog_re_product_settings_ui import Ui_Dialog_REProductSettings
from src.controllers.re_controller import RESettingController
from src import constants


class DialogREProductSetting(QDialog, Ui_Dialog_REProductSettings):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("real estate product setting".title())
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.controller = None
        self.current_table = None

        self.tableView.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows)

        self.statuses_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_STATUS_TABLE)
        )
        self.categories_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_CATEGORIES_TABLE))
        self.districts_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_DISTRICTS_TABLE))
        self.options_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_OPTIONS_TABLE))
        self.provinces_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_PROVINCES_TABLE))
        self.wards_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_WARDS_TABLE))
        self.building_line_s_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_BUILDING_LINES_TABLE))
        self.legal_s_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_LEGALS_TABLE))
        self.furniture_s_radio.clicked.connect(
            lambda: self.set_model(constants.RE_SETTING_FURNITURES_TABLE))

        self.create_btn.clicked.connect(self.handle_create)
        self.delete_btn.clicked.connect(self.handle_delete)

    def set_model(self, table_name):
        self.controller = RESettingController(table_name)
        self.current_table = table_name
        if not self.controller:
            return False
        self.tableView.setModel(self.controller.model)

    def handle_create(self):
        if not self.controller:
            return False
        data = {
            "label_vi": self.name_vi_input.text(),
            "label_en": self.name_en_input.text(),
            "value": self.value_input.text(),
        }
        self.controller.create_new(data)

    def handle_delete(self):
        if not self.controller:
            return False
        record_ids = self.get_selected_ids()
        if record_ids:
            reply = QMessageBox.question(self, "Confirm", f"Delete record(s) with ID(s): {record_ids}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            if reply == QMessageBox.StandardButton.Yes:
                for record_id in record_ids:
                    self.controller.delete(record_id)
        else:
            QMessageBox.warning(
                self, "Warning", "Please select a row to delete.")

    def get_selected_ids(self):
        selection_model = self.tableView.selectionModel()
        selected_rows = selection_model.selectedRows()
        record_ids = []
        for selected_row in selected_rows:
            row = selected_row.row()
            id_column = self.controller.model.fieldIndex("id")
            if id_column != -1:
                index = self.controller.model.index(row, id_column)
                record_ids.append(self.controller.model.data(index))
        return record_ids
