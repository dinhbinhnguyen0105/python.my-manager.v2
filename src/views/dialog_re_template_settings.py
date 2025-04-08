# src/views/dialog_re_template_settings.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QMessageBox, QTableView

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
        self.setup_events()
        self.setup_ui()

    def setup_events(self):
        self.title_radio.clicked.connect(self.set_title_section)
        self.description_radio.clicked.connect(self.set_description_section)
        self.create_btn.clicked.connect(self.handle_create)
        self.delete_btn.clicked.connect(self.handle_delete)

    def setup_ui(self):
        options = RESettingController.static_get_all(
            constants.RE_SETTING_OPTIONS_TABLE)
        for option in options:
            self.options_combobox.addItem(
                option.get("label_vi").capitalize(), option.get("id"))

        self.title_container.setHidden(True)
        self.description_container.setHidden(True)

    def set_title_section(self):
        self.description_container.setHidden(True)
        self.title_container.setHidden(False)
        self.set_model(constants.RE_TEMPLATE_TITLE_TABLE)

    def set_description_section(self):
        self.description_container.setHidden(False)
        self.title_container.setHidden(True)
        self.set_model(constants.RE_TEMPLATE_DESCRIPTION_TABLE)
        self.set_table()

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

    def handle_create(self):
        if not self.controller:
            return
        self.controller.create_new({})

    def handle_delete(self): pass
