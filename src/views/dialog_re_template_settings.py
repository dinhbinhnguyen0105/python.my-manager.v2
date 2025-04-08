# src/views/dialog_re_template_settings.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QMessageBox, QMenu
from PyQt6.QtGui import QAction

from src.ui.dialog_re_template_settings_ui import Ui_Dialog_RETemplateSettings
from src.controllers.re_controller import RETemplateController, RESettingController
from src import constants


class DialogRETemplateSetting(QDialog, Ui_Dialog_RETemplateSettings):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("real estate template setting".title())
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.controller = None
        self.current_model_name = None
        self.setup_events()
        self.setup_ui()

    def setup_events(self):
        self.title_radio.clicked.connect(self.set_title_section)
        self.description_radio.clicked.connect(self.set_description_section)
        self.create_btn.clicked.connect(self.handle_create)
        # self.delete_btn.clicked.connect(self.handle_delete)

    def setup_ui(self):
        options = RESettingController.static_get_all(
            constants.RE_SETTING_OPTIONS_TABLE)
        for option in options:
            self.options_combobox.addItem(
                option.get("label_vi").capitalize(), option.get("id")
            )

        self.title_container.setHidden(True)
        self.description_container.setHidden(True)
        self.delete_btn.setHidden(True)

    def set_title_section(self):
        self.description_container.setHidden(True)
        self.title_container.setHidden(False)
        self.set_model(constants.RE_TEMPLATE_TITLE_TABLE)
        self.current_model_name = constants.RE_TEMPLATE_TITLE_TABLE

    def set_description_section(self):
        self.description_container.setHidden(False)
        self.title_container.setHidden(True)
        self.set_model(constants.RE_TEMPLATE_DESCRIPTION_TABLE)
        self.set_table()
        self.current_model_name = constants.RE_TEMPLATE_DESCRIPTION_TABLE

    def set_model(self, table_name):
        self.controller = RETemplateController(table_name)
        self.current_table = table_name
        self.tableView.setModel(self.controller.model)
        self.set_table()

    def set_table(self):
        self.tableView.hideColumn(0)
        self.tableView.hideColumn(5)
        # self.tableView.resizeColumnsToContents()
        self.tableView.setSortingEnabled(True)
        self.tableView.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(
            self.show_context_menu)
        self.tableView.setSelectionBehavior(
            self.tableView.SelectionBehavior.SelectRows)

    def show_context_menu(self, pos):
        global_pos = self.tableView.mapToGlobal(pos)
        menu = QMenu(self.tableView)
        delete_aciton = QAction("Delete", self)
        menu.addAction(delete_aciton)
        menu.popup(global_pos)
        delete_aciton.triggered.connect(self.handle_delete)

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

    def handle_create(self):
        if not self.controller or not self.current_model_name:
            return
        self.controller.create_new(
            {
                "option_id": self.options_combobox.currentData(),
                "value": (
                    self.title_input.text()
                    if self.current_model_name == constants.RE_TEMPLATE_TITLE_TABLE
                    else self.description_input.toPlainText()
                ),
            }
        )

    def handle_delete(self):
        if not self.controller:
            return False
        record_ids = self.get_selected_ids()
        if record_ids:
            reply = QMessageBox.question(
                self,
                "Confirm",
                f"Delete record(s) with ID(s): {record_ids}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if reply == QMessageBox.StandardButton.Yes:
                for record_id in record_ids:
                    self.controller.delete(record_id)
        else:
            QMessageBox.warning(
                self, "Warning", "Please select a row to delete.")
