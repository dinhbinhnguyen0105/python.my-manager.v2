# src/views/robot/page_robot.py
from typing import Any
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QModelIndex, QSortFilterProxyModel, QVariant

from src.models.model_user import UserModel
from src.ui.page_robot_ui import Ui_PageRobot


class CustomTableModelProxy(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filters = {}

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

        if index.column() == self.columnCount() - 1:
            if role == Qt.ItemDataRole.DisplayRole:
                pass
            return QVariant()
        else:
            source_index = self.mapToSource(index)
            source_column = index.column() - 1
            adjusted_source_index = self.sourceModel().index(
                source_index.row(), source_column
            )
            return super().data(adjusted_source_index, role)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if orientation == Qt.Orientation.Horizontal:
            pass

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
    signal = pyqtSignal()

    def __init__(self, user_model: UserModel, parent=None):
        super(PageRobot, self).__init__(parent)
        self.user_model = user_model
