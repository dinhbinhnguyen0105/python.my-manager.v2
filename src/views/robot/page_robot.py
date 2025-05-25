# src/views/robot/page_robot.py
from typing import Any
from PyQt6.QtWidgets import QWidget, QTableView
from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    QModelIndex,
    QSortFilterProxyModel,
    QVariant,
    pyqtSlot,
    QItemSelection,
)

from src.models.model_user import UserModel
from src.ui.page_robot_ui import Ui_PageRobot
from src.views.robot.action_payload_container import ActionPayloadContainer


class CustomTableModelProxy(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filters = {}
        self.action_payload_data = {}  # row:value

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Return the number of columns, including the new STT column
        """
        # Return the number of columns from the source model plus 1 for the action_payload column
        return super().columnCount(parent) + 1

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Returns the data for the given and role.
        Provides the action_payload for the virtual column.
        """
        # If the index is invalid, return a default QVariant
        if not index.isValid():
            return QVariant()

        if index.column() == self.columnCount():
            if role == Qt.ItemDataRole.DisplayRole:
                return self.action_payload_data.get(index.row(), "")
            return QVariant()
        else:
            source_row = self.mapToSource(index).row()
            source_column = index.column()
            source_index = self.sourceModel().index(source_row, source_column)
            return self.sourceModel().data(source_index, role)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if orientation == Qt.Orientation.Horizontal:
            if section == super().columnCount() and role == Qt.ItemDataRole.DisplayRole:
                return "action_payload"
            else:
                return super().headerData(section, orientation, role)
        return super().headerData(section, orientation, role)

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

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

    def set_action_payload(self, row: int, value: Any):
        self.action_payload_data[row] = value
        left = self.index(row, super().columnCount())
        right = self.index(row, super().columnCount())
        self.dataChanged.emit(left, right, [Qt.ItemDataRole.DisplayRole])


class PageRobot(QWidget, Ui_PageRobot):
    run_robot_signal = pyqtSignal(dict)

    def __init__(self, user_model: UserModel, parent=None):
        super(PageRobot, self).__init__(parent)
        self.user_model = user_model
        self.proxy_model = CustomTableModelProxy()
        self.proxy_model.setSourceModel(self.user_model)
        self.robot_table = QTableView()
        self.selected_user_ids = set()
        self.action_payload_widgets = []

        self.setupUi(self)
        self.setWindowTitle("Robot")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setup_ui()
        self.setup_events()

    def setup_ui(self):
        self.robot_table.setModel(self.proxy_model)
        self.robot_table.setSortingEnabled(True)
        # self.robot_table.setSelectionMode(QTableView.SelectionMode.MultiSelection)
        # self.robot_table.setSelectionBehavior(
        #     self.robot_table.SelectionBehavior.SelectRows
        # )
        self.robot_table_container.layout().addWidget(self.robot_table)
        self.robot_table.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )
        self.set_hide_col_in_table()

        self.actions_container.setFixedWidth(480)

    def setup_events(self):
        self.action_add_btn.clicked.connect(self.on_add_action_payload_clicked)
        self.action_save_btn.clicked.connect(self.on_save_action_clicked)
        self.action_run_btn.clicked.connect(self.on_run_action_clicked)

    def set_hide_col_in_table(self):
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
                self.robot_table.setColumnHidden(col, True)

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_selection_changed(
        self, selected: QItemSelection, deselected: QItemSelection
    ):
        id_column_index_in_source = self.user_model.fieldIndex("id")
        selected_indexes = selected.indexes()
        deselected_indexes = deselected.indexes()
        for index in selected_indexes:
            source_index = self.proxy_model.mapToSource(index)
            source_row = source_index.row()
            id_index = self.user_model.index(source_row, id_column_index_in_source)
            self.selected_user_ids.add(self.user_model.data(id_index))

        for index in deselected_indexes:
            source_index = self.proxy_model.mapToSource(index)
            source_row = source_index.row()
            id_index = self.user_model.index(source_row, id_column_index_in_source)
            try:
                self.selected_user_ids.remove(self.user_model.data(id_index))
            except KeyError:
                pass

        sorted(self.selected_user_ids)

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

        print()

    @pyqtSlot()
    def on_run_action_clicked(self):

        print()
