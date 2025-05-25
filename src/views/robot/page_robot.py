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
    signal = pyqtSignal()

    def __init__(self, user_model: UserModel, parent=None):
        super(PageRobot, self).__init__(parent)
        self.user_model = user_model
        self.proxy_model = CustomTableModelProxy()
        self.proxy_model.setSourceModel(self.user_model)
        self.robot_table = QTableView()

        self.setupUi(self)
        self.setWindowTitle("Robot")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setup_ui()

    def setup_ui(self):
        self.robot_table.setModel(self.proxy_model)
        self.robot_table.setSortingEnabled(True)
        # self.robot_table.setSelectionBehavior(
        #     self.robot_table.SelectionBehavior.SelectRows
        # )
        self.robot_table_container.layout().addWidget(self.robot_table)
        self.robot_table.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_selection_changed(
        self, selected: QItemSelection, deselected: QItemSelection
    ):
        selected_rows_proxy_indices = self.robot_table.selectionModel().selectedRows()

        # Get the IDs of the selected users
        selected_user_ids = []
        id_column_index_in_source = self.user_model.fieldIndex("id")
        print(selected_rows_proxy_indices)
