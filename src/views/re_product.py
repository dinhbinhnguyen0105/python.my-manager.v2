# src/views/re_product.py
from PyQt6.QtCore import Qt, QPoint, QSortFilterProxyModel, QRegularExpression
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
from src.controllers.re_controller import REProductController, RESettingController
from src.views.dialog_re_product import DialogREProduct
from src import constants


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
        self.setup_filters()

        self.action_create_btn.clicked.connect(self.on_create_btn_clicked)

        # self.products_table.selectionModel().selectionChanged.connect(
        #     self.setup_details
        # )

    def setup_ui(self):
        self.setup_table()
        self.setup_comboboxes()

    # ['id', 'pid', 'status_id', 'option_id'3, 'ward_id', 'street', 'category_id6', 'area', 'price', 'legal_id'9, 'province_id', 'district_id', 'structure'12,
    #  'function'13, 'building_line_id'14, 'furniture_id', 'description', 'image_dir', 'created_at', 'updated_at']
    def setup_filters(self):
        self.options_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(self.options_combobox.currentData(), 3)
        )
        self.wards_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(self.wards_combobox.currentData(), 4)
        )
        self.categories_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(self.categories_combobox.currentData(), 6)
        )
        self.legal_s_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(self.legal_s_combobox.currentData(), 9)
        )
        self.building_line_s_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(
                self.building_line_s_combobox.currentData(), 14
            )
        )
        self.furniture_s_combobox.currentIndexChanged.connect(
            lambda: self.apply_column_filter(
                self.furniture_s_combobox.currentData(), 15
            )
        )

    def apply_column_filter(self, filter_text, column_index):
        if (
            filter_text == "Tất cả" or not filter_text
        ):  # Giả sử "Tất cả" hoặc rỗng là để bỏ lọc
            self.proxy_model.setFilterFixedString("")
        else:
            self.proxy_model.setFilterFixedString(filter_text)
            self.proxy_model.setFilterKeyColumn(column_index)

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

        self.products_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.products_table.customContextMenuRequested.connect(self.show_context_menu)

        self.products_table.setColumnHidden(0, True)
        self.products_table.setColumnHidden(10, True)
        self.products_table.setColumnHidden(11, True)
        self.products_table.setColumnHidden(16, True)
        self.products_table.setColumnHidden(17, True)
        self.products_table.setColumnHidden(18, True)

        self.products_table.horizontalHeader()

    def setup_comboboxes(self):
        wards = RESettingController.static_get_all(constants.RE_SETTING_WARDS_TABLE)
        options = RESettingController.static_get_all(constants.RE_SETTING_OPTIONS_TABLE)
        categories = RESettingController.static_get_all(
            constants.RE_SETTING_CATEGORIES_TABLE
        )
        building_line_s = RESettingController.static_get_all(
            constants.RE_SETTING_BUILDING_LINES_TABLE
        )
        furniture_s = RESettingController.static_get_all(
            constants.RE_SETTING_FURNITURES_TABLE
        )
        legal_s = RESettingController.static_get_all(constants.RE_SETTING_LEGALS_TABLE)

        for ward in wards:
            name = ward.get("label_vi").capitalize()
            value = ward.get("label_vi")
            self.wards_combobox.addItem(name, value)
        for option in options:
            name = option.get("label_vi").capitalize()
            value = option.get("label_vi")
            self.options_combobox.addItem(name, value)
        for category in categories:
            name = category.get("label_vi").capitalize()
            value = category.get("label_vi")
            self.categories_combobox.addItem(name, value)
        for building_line in building_line_s:
            name = building_line.get("label_vi").capitalize()
            value = building_line.get("label_vi")
            self.building_line_s_combobox.addItem(name, value)
        for furniture in furniture_s:
            name = furniture.get("label_vi").capitalize()
            value = furniture.get("label_vi")
            self.furniture_s_combobox.addItem(name, value)
        for legal in legal_s:
            name = legal.get("label_vi").capitalize()
            value = legal.get("label_vi")
            self.legal_s_combobox.addItem(name, value)

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

    def get_selected_id(self):
        selected_proxy_indexes = self.products_table.selectionModel().selectedRows()
        if not selected_proxy_indexes:
            return None
        proxy_index = selected_proxy_indexes[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        row = source_index.row()
        if 0 <= row < self.model.rowCount():
            return self.model.get_record_id(row)
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
                lambda: self.product_controller.update_product(id, edit_dialog.fields)
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
        image_paths = self.product_controller.get_image_paths(id)
        # self.detail_text.toPlainText
        # self.image_label.text()
        print(data)
        print(image_paths)
