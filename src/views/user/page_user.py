# src/views/user/page_user.py
from typing import List, Any
from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    QPoint,
    QSortFilterProxyModel,
    QModelIndex,
    QVariant,
)
from PyQt6.QtGui import QAction

from src.models.model_user import UserModel

from src.ui.page_user_ui import Ui_PageUser


class MultiFieldFilterProxyModel(QSortFilterProxyModel):
    SERIAL_NUMBER_COLUMN_INDEX = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filters = {}

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return super().columnCount(parent) + 1

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return QVariant()
        if index.column() == self.SERIAL_NUMBER_COLUMN_INDEX:
            if role == Qt.ItemDataRole.DisplayRole:
                return index.row() + 1
            return QVariant()

        else:
            source_row = self.mapToSource(index).row()
            source_column = index.column() - 1
            source_index = self.sourceModel().index(source_row, source_column)
            return self.sourceModel().data(source_index, role)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if orientation == Qt.Orientation.Horizontal:
            if (
                section == self.SERIAL_NUMBER_COLUMN_INDEX
                and role == Qt.ItemDataRole.DisplayRole
            ):
                return "STT"
            else:
                source_section = section - 1
                return super().headerData(source_section, orientation, role)
        return super().headerData(section, orientation, role)

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder):
        if column == self.SERIAL_NUMBER_COLUMN_INDEX:
            return
        super().sort(column - 1, order)

    def set_filter(self, column, text):
        self.filters[column] = text.lower()
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        for column, text in self.filters.items():
            if text:
                index = model.index(source_row, column, source_parent)
                data = str(model.data(index, Qt.ItemDataRole.DisplayRole)).lower()
                if text not in data:
                    return False
        return True


class PageUser(QWidget, Ui_PageUser):
    create_new_user_signal = pyqtSignal()
    user_settings_signal = pyqtSignal()

    updated_users_signal = pyqtSignal(list)
    deleted_users_signal = pyqtSignal(list)
    launch_users_signal = pyqtSignal(list, bool)
    check_users_signal = pyqtSignal(list)

    def __init__(self, user_model: UserModel, parent=None):
        super(PageUser, self).__init__(parent)
        self.user_model = user_model
        self.proxy_model = MultiFieldFilterProxyModel()
        self.proxy_model.setSourceModel(self.user_model)

        self.setupUi(self)
        self.setWindowTitle("User")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setup_ui()
        self.setup_events()
        self.setup_filters()

    def setup_events(self):
        self.action_create_btn.clicked.connect(self.create_new_user_signal)
        self.action_setting_btn.clicked.connect(self.user_settings_signal)

    def setup_ui(self):
        self.users_table.setModel(self.proxy_model)
        self.users_table.setSortingEnabled(True)
        self.users_table.setSelectionBehavior(
            self.users_table.SelectionBehavior.SelectRows
        )
        # self.users_table.setSelectionMode()
        self.users_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.users_table.customContextMenuRequested.connect(self.on_context_menu)

        # self.users_table.setColumnHidden(0, True)
        # self.users_table.setColumnHidden(1, True)

        self.users_table.setEditTriggers(self.users_table.EditTrigger.NoEditTriggers)

    def on_context_menu(self, pos: QPoint):
        index = self.users_table.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            launch_as_desktop_action = QAction("Launch as desktop", self)
            launch_as_mobile_action = QAction("Launch as mobile", self)
            check_action = QAction("Check live", self)
            edit_action = QAction("Edit", self)
            delete_action = QAction("Delete", self)

            launch_as_desktop_action.triggered.connect(
                lambda: self.on_item_context_clicked("launch-desktop")
            )
            launch_as_mobile_action.triggered.connect(
                lambda: self.on_item_context_clicked("launch-mobile")
            )
            check_action.triggered.connect(
                lambda: self.on_item_context_clicked("check")
            )
            edit_action.triggered.connect(lambda: self.on_item_context_clicked("edit"))
            delete_action.triggered.connect(
                lambda: self.on_item_context_clicked("delete")
            )
            menu.addAction(launch_as_desktop_action)
            menu.addAction(launch_as_mobile_action)
            menu.addAction(check_action)
            menu.addAction(edit_action)
            menu.addAction(delete_action)

            menu.popup(self.users_table.viewport().mapToGlobal(pos))

    def on_item_context_clicked(self, action_name: str):
        selected_ids = self.get_selected_id()
        action_method = {
            "launch-desktop": self.launch_users_signal,
            "launch-mobile": self.launch_users_signal,
            "check": self.check_users_signal,
            "edit": self.updated_users_signal,
            "delete": self.deleted_users_signal,
        }
        if action_name in action_method.keys():
            if action_name == "launch-desktop":
                action_method[action_name].emit(selected_ids, False)
            elif action_name == "launch-mobile":
                action_method[action_name].emit(selected_ids, True)
            else:
                action_method[action_name].emit(selected_ids)

    def get_selected_id(self) -> List[int]:
        selected_rows = self.users_table.selectionModel().selectedRows()
        id_column_index = self.user_model.fieldIndex("id")
        selected_ids = []
        for selected_row in selected_rows:
            source_index = self.proxy_model.mapToSource(selected_row)
            if source_index.isValid():
                id_data = self.user_model.data(
                    source_index.siblingAtColumn(id_column_index),
                    Qt.ItemDataRole.DisplayRole,
                )
                selected_ids.append(id_data)
        return sorted(selected_ids)

    def setup_filters(self):
        filter_widgets = [
            (self.uid_input, self.user_model.fieldIndex("uid")),
            (self.note_input, self.user_model.fieldIndex("note")),
            (self.type_input, self.user_model.fieldIndex("type")),
            (self.email_input, self.user_model.fieldIndex("email")),
            (self.email_password_input, self.user_model.fieldIndex("email_password")),
            (self.group_input, self.user_model.fieldIndex("group")),
            (self.two_fa_input, self.user_model.fieldIndex("two_fa")),
            (self.username_input, self.user_model.fieldIndex("username")),
            (self.password_input, self.user_model.fieldIndex("password")),
            (self.phone_number_input, self.user_model.fieldIndex("phone_number")),
        ]

        for widget, column in filter_widgets:
            widget.textChanged.connect(
                lambda text, col=column: self.proxy_model.set_filter(col, text)
            )
