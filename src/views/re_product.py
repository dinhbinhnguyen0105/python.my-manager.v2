# src/views/re_product.py
from PyQt6.QtCore import Qt, QPoint, QSortFilterProxyModel
from PyQt6.QtWidgets import (
    QMessageBox,
    QDialog,
    QWidget,
    QMenu,
    QTableView,
    QAbstractItemView,
)
from PyQt6.QtGui import QAction


from src.ui.re_product_ui import Ui_REProduct
from src.models.re_model import REProductRelationalModel
from src.controllers.re_controller import REProductController
from src.views.dialog_re_product import DialogREProduct


class REProduct(QWidget, Ui_REProduct):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Real Estate Product")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(self.size())
        self.model = REProductRelationalModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.product_controller = REProductController(self.model)
        self.setup_ui()

    def setup_ui(self):
        self.setup_table()
        self.setup_buttons()
        pass

    def setup_table(self):
        self.products_table.setModel(self.proxy_model)
        self.products_table.setSelectionBehavior(
            self.products_table.SelectionBehavior.SelectRows
        )
        self.products_table.setSelectionMode(
            self.products_table.SelectionMode.SingleSelection
        )
        self.products_table.resizeColumnsToContents()
        self.products_table.setSortingEnabled(True)

        self.products_table.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.products_table.customContextMenuRequested.connect(
            self.show_context_menu)

        # self.products_table.setColumnHidden(0, True)
        # self.products_table.setColumnHidden(9, True)
        # self.products_table.setColumnHidden(10, True)
        # self.products_table.setColumnHidden(16, True)
        # self.products_table.setColumnHidden(17, True)
        # self.products_table.setColumnHidden(18, True)

        self.products_table.horizontalHeader()

        # self.products_table.selectionModel().selectionChanged.connect(
        #     self.setup_details
        # )

    def setup_buttons(self):
        self.action_create_btn.clicked.connect(self.on_create_btn_clicked)

    def filter_logics(self, row, parent, conditions):
        source_model = self.proxy_model.sourceModel()

    def show_context_menu(self, pos: QPoint):
        global_pos = self.products_table.mapToGlobal(pos)
        menu = QMenu(self.products_table)
        edit_action = QAction("Edit", self)
        delete_action = QAction("Delete", self)

        edit_action.triggered.connect(self.handle_update)
        delete_action.triggered.connect(self.handle_delete)

        menu.addAction(edit_action)
        menu.addAction(delete_action)

        menu.popup(global_pos)
        # menu.exec(global_pos)

    def get_selected_id(self):
        selected_proxy_indexes = self.products_table.selectionModel().selectedRows()
        if not selected_proxy_indexes:
            return None
        proxy_index = selected_proxy_indexes[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        row = source_index.row()
        if 0 <= row < self.model.rowCount():
            return self.model.get_record_id(row)
            # record = self.model.record(row)
            # return record.value("id")
        return None

    def handle_update(self):
        id = self.get_selected_id()
        if id is not None:
            current_product_data = self.product_controller.read_product(id)
            edit_dialog = DialogREProduct(current_product_data)
            edit_dialog.setWindowTitle("Edit Product")
            edit_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            edit_dialog.setFixedSize(edit_dialog.size())
            edit_dialog.accepted.connect(
                lambda: self.product_controller.update_product(
                    id, edit_dialog.fields
                )
            )
            edit_dialog.exec()

        else:
            QMessageBox.warning(self, "Warning", "No product selected.")
        pass

    def handle_delete(self):
        id = self.get_selected_id()
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete this product?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            if id is not None:
                self.product_controller.delete_product(id)
            else:
                QMessageBox.warning(self, "Warning", "No product selected.")
        else:
            # User clicked No, do nothing
            pass

    def on_create_btn_clicked(self):
        create_dialog = DialogREProduct()
        create_dialog.setWindowTitle("Create Product")
        create_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        create_dialog.setFixedSize(create_dialog.size())
        create_dialog.accepted.connect(
            lambda: self.product_controller.add_product(create_dialog.fields)
        )
        create_dialog.exec()

    def setup_details(self):
        id = self.get_selected_id()
        if id is None:
            return
        data = self.product_controller.read_product(id)
        image_paths = self.product_controller.get_image_path(id)
