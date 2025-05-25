# src/views/robot/page_robot.py
from typing import Any, List
from PyQt6.QtWidgets import QWidget, QTableView
from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    QSortFilterProxyModel,
    pyqtSlot,
    QItemSelection,
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from src.models.model_user import UserModel, UserActionModel
from src.ui.page_robot_ui import Ui_PageRobot
from src.views.robot.action_payload_container import ActionPayloadContainer


class CustomTableModelProxy(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filters = {}

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder):
        if column == super().columnCount():
            return
        super().sort(column, order)

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


class PageRobot(QWidget, Ui_PageRobot):
    run_robot_signal = pyqtSignal(dict)

    def __init__(
        self,
        user_model: UserModel,
        user_action_model: UserActionModel,
        parent=None,
    ):
        super(PageRobot, self).__init__(parent)
        self.user_model = user_model
        self.proxy_model = CustomTableModelProxy()
        self.proxy_model.setSourceModel(self.user_model)
        self.user_action_model = user_action_model
        self.user_table = QTableView()
        self.user_action_table = QTableView()
        self.selected_rows = set()
        self.action_payload_widgets: List[ActionPayloadContainer] = []

        self.setupUi(self)
        self.setWindowTitle("Robot")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setup_ui()
        self.setup_events()

    def setup_ui(self):
        self.actions_container.setFixedWidth(480)
        self.user_table.setModel(self.proxy_model)
        self.user_table.setSortingEnabled(True)
        self.user_table.setSelectionBehavior(
            self.user_table.SelectionBehavior.SelectRows
        )
        self.robot_table_container.layout().addWidget(self.user_table)
        self.user_table.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )
        self.user_table.setWordWrap(True)
        self.set_hide_col_in_user_table()

        self.user_action_table.setModel(self.user_action_model)
        self.robot_table_container.layout().addWidget(self.user_action_table)

    def setup_events(self):
        self.action_add_btn.clicked.connect(self.on_add_action_payload_clicked)
        self.action_save_btn.clicked.connect(self.on_save_action_clicked)
        self.action_run_btn.clicked.connect(self.on_run_action_clicked)

    def set_hide_col_in_user_table(self):
        for col in range(self.proxy_model.columnCount()):
            col_name = self.proxy_model.headerData(
                col,
                Qt.Orientation.Horizontal,
                Qt.ItemDataRole.DisplayRole,
            )
            if col_name not in [
                "uid",
                "username",
                "note",
                "type",
                "user_group",
                "updated_at",
                "action_payload",
            ]:
                self.user_table.setColumnHidden(col, True)

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_selection_changed(
        self, selected: QItemSelection, deselected: QItemSelection
    ):
        selected_indexes = selected.indexes()
        deselected_indexes = deselected.indexes()

        for index in selected_indexes:
            proxy_row = index.row()
            self.selected_rows.add(proxy_row)
        for index in deselected_indexes:
            proxy_row = index.row()
            self.selected_rows.discard(proxy_row)

    @pyqtSlot()
    def on_add_action_payload_clicked(self):
        action_payload = ActionPayloadContainer()
        self.action_payload_container_layout.addWidget(action_payload)
        self.action_payload_widgets.append(action_payload)
        action_payload.action_delete_btn.clicked.connect(
            lambda: self.on_delete_action_payload_clicked(
                len(self.action_payload_widgets) - 1,
                action_payload,
            )
        )

    @pyqtSlot(int, ActionPayloadContainer)
    def on_delete_action_payload_clicked(
        self,
        index,
        action_payload_widget: ActionPayloadContainer,
    ):
        self.action_payload_widgets.pop(index)
        action_payload_widget.deleteLater()

    @pyqtSlot()
    def on_save_action_clicked(self):
        actions = []
        for action_payload_widget in self.action_payload_widgets:
            actions.append(action_payload_widget.get_values())

    @pyqtSlot()
    def on_run_action_clicked(self):

        print()
