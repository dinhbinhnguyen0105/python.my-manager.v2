# src/views/setting_view.py
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableView, QLineEdit, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from src.models.re_model import RESettingProvincesModel
from src.models.re_database import initialize_re_products
from src.controllers.re_controller import RESettingController


class SettingView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings - Provinces")
        self.resize(800, 600)
        self.controller = RESettingController(
            constants.RE_SETTING_WARDS_TABLE)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows)
        # self.table_view.setSelectionMode(
        #     QTableView.SelectionMode.SingleSelection)
        main_layout.addWidget(self.table_view)

        self.table_view.setModel(self.controller.model)

        form_layout = QHBoxLayout()
        self.label_vi_edit = QLineEdit()
        self.label_en_edit = QLineEdit()
        self.value_edit = QLineEdit()
        form_layout.addWidget(QLabel("Label VI:"))
        form_layout.addWidget(self.label_vi_edit)
        form_layout.addWidget(QLabel("Label EN:"))
        form_layout.addWidget(self.label_en_edit)
        form_layout.addWidget(QLabel("Value:"))
        form_layout.addWidget(self.value_edit)
        main_layout.addLayout(form_layout)

        self.save_btn = QPushButton("Add new")
        self.save_btn.clicked.connect(self.handle_save)
        form_layout.addWidget(self.save_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.handle_delete)
        main_layout.addWidget(self.delete_btn)

    def handle_save(self):
        data = {
            "label_vi": self.label_vi_edit.text(),
            "label_en": self.label_en_edit.text(),
            "value": self.value_edit.text(),
        }
        self.controller.create_new(data)
        self.controller.refresh_data()

    def handle_delete(self):
        record_ids = self.get_selected_ids()
        if record_ids:
            reply = QMessageBox.question(self, "Confirm", f"Delete record(s) with ID(s): {record_ids}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            if reply == QMessageBox.StandardButton.Yes:
                for record_id in record_ids:
                    self.controller.delete(record_id)
        else:
            QMessageBox.warning(
                self, "Warning", "Please select a row to delete.")

    def get_selected_ids(self):
        selection_model = self.table_view.selectionModel()
        selected_rows = selection_model.selectedRows()
        record_ids = []
        for selected_row in selected_rows:
            row = selected_row.row()
            id_column = self.controller.model.fieldIndex("id")
            if id_column != -1:
                index = self.controller.model.index(row, id_column)
                record_ids.append(self.controller.model.data(index))
        return record_ids

    def on_row_changed(self, current, previous):
        if current.isValid():
            self.controller.set_current_index(current.row())


if __name__ == "__main__":
    import sys
    from src import constants  # đảm bảo constants có RE_SETTING_PROVINCES_TABLE
    app = QApplication(sys.argv)
    initialize_re_products()
    window = SettingView()
    window.show()
    sys.exit(app.exec())
