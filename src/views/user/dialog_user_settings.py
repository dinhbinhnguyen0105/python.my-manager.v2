# src/views/user/dialog_user_settings.py
from typing import List, Optional
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDialog, QMenu
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QModelIndex, pyqtSlot

from src.my_types import UserSettingProxyType, UserSettingUDDType
from src.constants import TABLE_USER_SETTING_UDD, TABLE_USER_SETTING_PROXY
from src.models.model_user import UserSettingUDDModel, UserSettingProxyModel

from src.ui.dialog_user_settings_ui import Ui_Dialog_UserSettings


class DialogUserSettings(QDialog, Ui_Dialog_UserSettings):
    create_new_proxy_signal = pyqtSignal(UserSettingProxyType)
    create_new_udd_signal = pyqtSignal(UserSettingUDDType)
    delete_udd_signal = pyqtSignal(int)
    delete_proxy_signal = pyqtSignal(int)
    set_selected_udd_signal = pyqtSignal(int)

    def __init__(
        self,
        udd_model: UserSettingUDDModel,
        proxy_model: UserSettingProxyModel,
        parent=None,
    ):
        super(DialogUserSettings, self).__init__(parent)
        self.fields = {}
        self.udd_model = udd_model
        self.proxy_model = proxy_model
        self.table_name = None
        self.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle("Setting user")
        self.setup_ui()
        self.setup_events()

    def setup_ui(self):
        self.fields_container.setHidden(True)
        self.proxy_container.setHidden(True)
        self.udd_container.setHidden(True)
        self.udd_is_selected_checkbox.setHidden(True)

    def setup_events(self):
        self.udd_radio.clicked.connect(lambda: self.set_table(TABLE_USER_SETTING_UDD))
        self.proxy_radio.clicked.connect(
            lambda: self.set_table(TABLE_USER_SETTING_PROXY)
        )
        self.create_new_btn.clicked.connect(self.on_create_new_clicked)

    def set_table(self, table_name):
        self.table_name = table_name
        self.fields_container.setHidden(False)
        if table_name == TABLE_USER_SETTING_PROXY:
            self.tableView.setModel(self.proxy_model)

        elif table_name == TABLE_USER_SETTING_UDD:
            self.tableView.setModel(self.udd_model)
        else:
            pass

        self.proxy_container.setVisible(table_name == TABLE_USER_SETTING_PROXY)
        self.udd_container.setVisible(table_name == TABLE_USER_SETTING_UDD)

        self.tableView.setSortingEnabled(True)
        self.tableView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.on_context_menu)
        self.tableView.setSelectionBehavior(self.tableView.SelectionBehavior.SelectRows)

    def on_context_menu(self, pos: QPoint):
        index = self.tableView.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(self.on_delete_clicked)

            menu.addAction(delete_action)
            if self.table_name == TABLE_USER_SETTING_UDD:
                set_selected_action = QAction("Set selected", self)
                set_selected_action.triggered.connect(self.on_set_selected_clicked)
                menu.addAction(set_selected_action)
            menu.popup(self.tableView.viewport().mapToGlobal(pos))

    def get_selected_id(
        self, model: Optional[UserSettingUDDModel | UserSettingProxyModel]
    ) -> List[int]:
        selected_rows = self.tableView.selectionModel().selectedRows()
        id_column_index = model.fieldIndex("id")
        selected_ids = []
        for selected_row in selected_rows:
            id_data = model.data(
                selected_row.siblingAtColumn(id_column_index),
                Qt.ItemDataRole.DisplayRole,
            )
            selected_ids.append(id_data)
        return sorted(selected_ids)

    @pyqtSlot()
    def on_delete_clicked(self):
        selected_ids = []
        if self.table_name == TABLE_USER_SETTING_PROXY:
            selected_ids = self.get_selected_id(self.proxy_model)
            self.delete_proxy_signal.emit(selected_ids[0])
        elif self.table_name == TABLE_USER_SETTING_UDD:
            selected_ids = self.get_selected_id(self.udd_model)
            self.delete_udd_signal.emit(selected_ids[0])

    @pyqtSlot()
    def on_set_selected_clicked(self):
        selected_ids = self.get_selected_id(self.udd_model)
        self.set_selected_udd_signal.emit(selected_ids[0])

    @pyqtSlot()
    def on_create_new_clicked(self):
        if self.table_name == TABLE_USER_SETTING_PROXY:
            self.create_new_proxy_signal.emit(
                UserSettingProxyType(
                    id=None,
                    value=self.proxy_input.text(),
                    created_at=None,
                    updated_at=None,
                ),
            )
        elif self.table_name == TABLE_USER_SETTING_UDD:
            self.create_new_udd_signal.emit(
                UserSettingUDDType(
                    id=None,
                    value=self.udd_input.text(),
                    is_selected=1 if self.udd_is_selected_checkbox.isChecked() else 0,
                    created_at=None,
                    updated_at=None,
                ),
            )
        else:
            print(f"[{__class__.__name__}.on_create_new_clicked] Invalid table name")
