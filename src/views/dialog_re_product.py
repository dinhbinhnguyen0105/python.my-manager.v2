# src/views/dialog_re_product.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from PyQt6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox
from src import constants
from src.controllers.re_controller import REProductController, RESettingController
from src.ui.dialog_re_product_ui import Ui_Dialog_REProduct


class DialogREProduct(QDialog, Ui_Dialog_REProduct):
    def __init__(self, data={
        "image_paths": [],
        "pid": "",
        "street": "",
        "status_id": -1,
        "province_id": -1,
        "district_id": -1,
        "ward_id": -1,
        "option_id": -1,
        "category_id": -1,
        "building_line_id": -1,
        "furniture_id": -1,
        "legal_id": -1,
        "area": 0.0,
        "structure": 0.0,
        "function": "",
        "description": "",
        "price": 0.0,
    }, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("real estate product".title())
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.fields = data
        self._setupImageDrop()
        self._connect_signals()
        self._initialize_option_radios()
        self._load_initial_data()

    def _connect_signals(self):
        self.pid_input.textChanged.connect(
            lambda: self.set_field("pid", self.pid_input.text()))
        self.street_input.textChanged.connect(
            lambda: self.set_field("street", self.street_input.text()))
        self.description_input.textChanged.connect(lambda: self.set_field(
            "description", self.description_input.toPlainText()))
        self.area_input.textChanged.connect(
            lambda: self.set_field("area", self.area_input.text()))
        self.structure_input.textChanged.connect(
            lambda: self.set_field("structure", self.structure_input.text()))
        self.function_input.textChanged.connect(
            lambda: self.set_field("function", self.function_input.text()))
        self.price_input.textChanged.connect(
            lambda: self.set_field("price", self.price_input.text()))
        self.provinces_combobox.currentIndexChanged.connect(
            lambda: self.set_field("province_id", self.provinces_combobox.currentData()))
        self.districts_combobox.currentIndexChanged.connect(
            lambda: self.set_field("district_id", self.districts_combobox.currentData()))
        self.wards_combobox.currentIndexChanged.connect(
            lambda: self.set_field("ward_id", self.wards_combobox.currentData()))
        self.statuses_combobox.currentIndexChanged.connect(
            lambda: self.set_field("status_id", self.statuses_combobox.currentData()))
        self.categories_combobox.currentIndexChanged.connect(
            lambda: self.set_field("category_id", self.categories_combobox.currentData()))
        self.building_line_s_combobox.currentIndexChanged.connect(lambda: self.set_field(
            "building_line_id", self.building_line_s_combobox.currentData()))
        self.furniture_s_combobox.currentIndexChanged.connect(
            lambda: self.set_field("furniture_id", self.furniture_s_combobox.currentData()))
        self.legal_s_combobox.currentIndexChanged.connect(
            lambda: self.set_field("legal_id", self.legal_s_combobox.currentData()))

        self.buttonBox.accepted.disconnect()
        self.btn_save = self.buttonBox.button(
            QDialogButtonBox.StandardButton.Save)
        self.btn_save.clicked.connect(self.handle_save)
        self.buttonBox.rejected.connect(self.handle_rejected)

    def handle_rejected(self):
        pass

    def handle_save(self):
        if not REProductController.validate_new_product(self.fields):
            return False
        self.accept()

    def _initialize_option_radios(self):
        """Khởi tạo trạng thái và kết nối tín hiệu cho các radio button tùy chọn."""
        setting_controller = RESettingController(
            constants.RE_SETTING_OPTIONS_TABLE)
        options = setting_controller.get_all()
        option_values = {option.get("value"): option.get("id")
                         for option in options}

        def set_option(option_value):
            self.initialize_ui(option_value)
            option_id = option_values.get(option_value)
            self.set_field("option_id", option_id)
            # Tạo PID mới dựa trên option và cập nhật input
            new_pid = REProductController.generate_pid(option_value)
            self.pid_input.setText(new_pid)
            self.set_field("pid", new_pid)  # Cập nhật cả self.fields

        current_option_id = self.fields.get("option_id")
        initial_option_value = None
        for value, id in option_values.items():
            if id == current_option_id:
                initial_option_value = value
                if value == "sell":
                    self.option_sell_radio.setChecked(True)
                    self.initialize_ui("sell")
                elif value == "rent":
                    self.option_rent_radio.setChecked(True)
                    self.initialize_ui("rent")
                elif value == "assignment":
                    self.option_assignment_radio.setChecked(True)
                    self.initialize_ui("assignment")
                break
        else:
            # Nếu không có option_id ban đầu, mặc định chọn sell
            self.option_sell_radio.setChecked(True)
            initial_option_value = "sell"
            self.set_field("option_id", option_values.get("sell"))
            self.initialize_ui("sell")

        # Tạo PID ban đầu dựa trên option được chọn khi khởi tạo
        if not self.fields.get("pid"):
            self.pid_input.setText(
                REProductController.generate_pid(initial_option_value))
        else:
            self.pid_input.setText(self.fields.get("pid"))
        self.pid_input.setReadOnly(True)

        self.option_sell_radio.clicked.connect(lambda: set_option("sell"))
        self.option_rent_radio.clicked.connect(lambda: set_option("rent"))
        self.option_assignment_radio.clicked.connect(
            lambda: set_option("assignment"))

    def _load_initial_data(self):
        if self.fields.get("image_paths"):
            self._display_image(self.fields["image_paths"][0])

        self.street_input.setText(self.fields.get("street"))
        self.description_input.setPlainText(self.fields.get("description"))
        self.area_input.setText(str(self.fields.get("area")))
        self.structure_input.setText(str(self.fields.get("structure")))
        self.function_input.setText(str(self.fields.get("function")))
        self.price_input.setText(str(self.fields.get("price")))

        self._load_combobox_data(
            self.provinces_combobox, constants.RE_SETTING_PROVINCES_TABLE, self.fields.get("province_id"))
        self._load_combobox_data(
            self.districts_combobox, constants.RE_SETTING_DISTRICTS_TABLE, self.fields.get("district_id"))
        self._load_combobox_data(
            self.wards_combobox, constants.RE_SETTING_WARDS_TABLE, self.fields.get("ward_id"))
        self._load_combobox_data(
            self.statuses_combobox, constants.RE_SETTING_STATUS_TABLE, self.fields.get("status_id"))
        self._load_combobox_data(
            self.categories_combobox, constants.RE_SETTING_CATEGORIES_TABLE, self.fields.get("category_id"))
        self._load_combobox_data(self.building_line_s_combobox,
                                 constants.RE_SETTING_BUILDING_LINES_TABLE, self.fields.get("building_line_id"))
        self._load_combobox_data(
            self.furniture_s_combobox, constants.RE_SETTING_FURNITURES_TABLE, self.fields.get("furniture_id"))
        self._load_combobox_data(
            self.legal_s_combobox, constants.RE_SETTING_LEGALS_TABLE, self.fields.get("legal_id"))

    def set_field(self, field, value):
        if not value:
            return False
        if isinstance(value, str):
            float_val = str_to_float(value)
            self.fields[field] = float_val if float_val is not False else value.strip(
            ).lower() if field != "description" else value.strip()
        else:
            self.fields[field] = value
        return self.fields

    def initialize_ui(self, option):
        self.legal_s_combobox.setEnabled(option not in ("assignment", "rent"))

    def _load_combobox_data(self, combobox_widget, table_name, current_id=-1):
        combobox_widget.clear()
        get_all_setting = RESettingController.static_get_all
        records = get_all_setting(table_name)
        for record in records:
            record_id = record.get("id", -1)
            record_vi_label = record.get("label_vi", "undefined").title()
            combobox_widget.addItem(record_vi_label, record_id)
            if current_id == record_id:
                combobox_widget.setCurrentIndex(
                    combobox_widget.count() - 1)  # Chọn sau khi thêm

    def _setupImageDrop(self):
        self.image_input.setAcceptDrops(True)
        self.image_input.dragEnterEvent = self._imagesDragEnterEvent
        self.image_input.dropEvent = self._imagesDropEvent

    def _imagesDragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def _imagesDropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            images = [url.toLocalFile() for url in event.mimeData().urls()]
            self._handleDroppedImages(images)
            self.fields["image_paths"] = images

    def _handleDroppedImages(self, image_paths):
        if image_paths:
            self._display_image(image_paths[0])
        else:
            self.image_input.setText("No images dropped.")

    def _display_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_input.setPixmap(
                pixmap.scaled(
                    self.image_input.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            self.image_input.setText("Failed to load image.")


def str_to_float(string):
    try:
        return float(string)
    except (ValueError, TypeError):
        return False
