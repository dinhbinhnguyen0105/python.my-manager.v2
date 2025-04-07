# src/ui/product_real_estate_ui.py
# Form implementation generated from reading ui file '/Volumes/KINGSTON/Dev/python/python.my-manager.v1/ui/product_real_estate.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_REProduct(object):
    def setupUi(self, REProduct):
        REProduct.setObjectName("REProduct")
        REProduct.resize(1139, 519)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        REProduct.setFont(font)
        REProduct.setStyleSheet(
            "QGroupBox {\n"
            'font-family: "Courier New";\n'
            "font-size: 13px;\n"
            "background-color: rgba(248, 249, 250, 1);\n"
            "}\n"
            "QLineEdit{\n"
            "border: 1px solid #CED4DA;\n"
            "border-radius: 4px;\n"
            "margin-left: 8px;\n"
            "padding: 4px 0 4px 4px;\n"
            "}\n"
            "QLabel{\n"
            "font-size: 10px;\n"
            "color: rgb(90, 93, 97);\n"
            "max-height: 16px\n"
            "}"
        )
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(REProduct)
        self.horizontalLayout_6.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.contents_container_w = QtWidgets.QWidget(parent=REProduct)
        self.contents_container_w.setObjectName("contents_container_w")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.contents_container_w)
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.verticalLayout_27 = QtWidgets.QVBoxLayout()
        self.verticalLayout_27.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_27.setSpacing(0)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.search_container = QtWidgets.QGroupBox(parent=self.contents_container_w)
        self.search_container.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.search_container.setFont(font)
        self.search_container.setAutoFillBackground(False)
        self.search_container.setStyleSheet("")
        self.search_container.setTitle("")
        self.search_container.setObjectName("search_container")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.search_container)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.furniture_cotnainer_w = QtWidgets.QWidget(parent=self.search_container)
        self.furniture_cotnainer_w.setObjectName("furniture_cotnainer_w")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.furniture_cotnainer_w)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.furniture_label = QtWidgets.QLabel(parent=self.furniture_cotnainer_w)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.furniture_label.setFont(font)
        self.furniture_label.setStyleSheet("margin: 0;")
        self.furniture_label.setObjectName("furniture_label")
        self.verticalLayout_10.addWidget(self.furniture_label)
        self.furniture_input = QtWidgets.QLineEdit(parent=self.furniture_cotnainer_w)
        self.furniture_input.setStyleSheet("margin: 0;\n" "padding-left: 4px;")
        self.furniture_input.setObjectName("furniture_input")
        self.verticalLayout_10.addWidget(self.furniture_input)
        self.verticalLayout_9.addLayout(self.verticalLayout_10)
        self.gridLayout.addWidget(self.furniture_cotnainer_w, 1, 4, 1, 1)
        self.wards_container_w = QtWidgets.QWidget(parent=self.search_container)
        self.wards_container_w.setObjectName("wards_container_w")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.wards_container_w)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.wards_label = QtWidgets.QLabel(parent=self.wards_container_w)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.wards_label.setFont(font)
        self.wards_label.setStyleSheet("margin: 0;")
        self.wards_label.setObjectName("wards_label")
        self.verticalLayout_16.addWidget(self.wards_label)
        self.wards_combobox = QtWidgets.QComboBox(parent=self.wards_container_w)
        self.wards_combobox.setObjectName("wards_combobox")
        self.wards_combobox.addItem("")
        self.verticalLayout_16.addWidget(self.wards_combobox)
        self.verticalLayout_15.addLayout(self.verticalLayout_16)
        self.gridLayout.addWidget(self.wards_container_w, 0, 0, 1, 1)
        self.options_container_w = QtWidgets.QWidget(parent=self.search_container)
        self.options_container_w.setStyleSheet("padding")
        self.options_container_w.setObjectName("options_container_w")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.options_container_w)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.options_label = QtWidgets.QLabel(parent=self.options_container_w)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.options_label.setFont(font)
        self.options_label.setStyleSheet("margin: 0;")
        self.options_label.setObjectName("options_label")
        self.verticalLayout_14.addWidget(self.options_label)
        self.options_combobox = QtWidgets.QComboBox(parent=self.options_container_w)
        self.options_combobox.setObjectName("options_combobox")
        self.options_combobox.addItem("")
        self.verticalLayout_14.addWidget(self.options_combobox)
        self.verticalLayout_13.addLayout(self.verticalLayout_14)
        self.gridLayout.addWidget(self.options_container_w, 0, 1, 1, 1)
        self.categories_container_w = QtWidgets.QWidget(parent=self.search_container)
        self.categories_container_w.setObjectName("categories_container_w")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.categories_container_w)
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout()
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.categories_label = QtWidgets.QLabel(parent=self.categories_container_w)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.categories_label.setFont(font)
        self.categories_label.setStyleSheet("margin: 0;")
        self.categories_label.setObjectName("categories_label")
        self.verticalLayout_26.addWidget(self.categories_label)
        self.categories_combobox = QtWidgets.QComboBox(
            parent=self.categories_container_w
        )
        self.categories_combobox.setObjectName("categories_combobox")
        self.categories_combobox.addItem("")
        self.verticalLayout_26.addWidget(self.categories_combobox)
        self.verticalLayout_25.addLayout(self.verticalLayout_26)
        self.gridLayout.addWidget(self.categories_container_w, 0, 3, 1, 1)
        self.building_line_s_container_w = QtWidgets.QWidget(
            parent=self.search_container
        )
        self.building_line_s_container_w.setObjectName("building_line_s_container_w")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.building_line_s_container_w)
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout()
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.building_line_s_label = QtWidgets.QLabel(
            parent=self.building_line_s_container_w
        )
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.building_line_s_label.setFont(font)
        self.building_line_s_label.setStyleSheet("margin: 0;")
        self.building_line_s_label.setObjectName("building_line_s_label")
        self.verticalLayout_22.addWidget(self.building_line_s_label)
        self.building_line_s_combobox = QtWidgets.QComboBox(
            parent=self.building_line_s_container_w
        )
        self.building_line_s_combobox.setObjectName("building_line_s_combobox")
        self.building_line_s_combobox.addItem("")
        self.verticalLayout_22.addWidget(self.building_line_s_combobox)
        self.verticalLayout_21.addLayout(self.verticalLayout_22)
        self.gridLayout.addWidget(self.building_line_s_container_w, 0, 4, 1, 1)
        self.furniture_s_container_w = QtWidgets.QWidget(parent=self.search_container)
        self.furniture_s_container_w.setObjectName("furniture_s_container_w")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.furniture_s_container_w)
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.furniture_s_lable = QtWidgets.QLabel(parent=self.furniture_s_container_w)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.furniture_s_lable.setFont(font)
        self.furniture_s_lable.setStyleSheet("margin: 0;")
        self.furniture_s_lable.setObjectName("furniture_s_lable")
        self.verticalLayout_20.addWidget(self.furniture_s_lable)
        self.furniture_s_combobox = QtWidgets.QComboBox(
            parent=self.furniture_s_container_w
        )
        self.furniture_s_combobox.setObjectName("furniture_s_combobox")
        self.furniture_s_combobox.addItem("")
        self.verticalLayout_20.addWidget(self.furniture_s_combobox)
        self.verticalLayout_19.addLayout(self.verticalLayout_20)
        self.gridLayout.addWidget(self.furniture_s_container_w, 0, 5, 1, 1)
        self.legal_s_container_w = QtWidgets.QWidget(parent=self.search_container)
        self.legal_s_container_w.setObjectName("legal_s_container_w")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.legal_s_container_w)
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout()
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.legal_s_label = QtWidgets.QLabel(parent=self.legal_s_container_w)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.legal_s_label.setFont(font)
        self.legal_s_label.setStyleSheet("margin: 0;")
        self.legal_s_label.setObjectName("legal_s_label")
        self.verticalLayout_24.addWidget(self.legal_s_label)
        self.legal_s_combobox = QtWidgets.QComboBox(parent=self.legal_s_container_w)
        self.legal_s_combobox.setObjectName("legal_s_combobox")
        self.legal_s_combobox.addItem("")
        self.verticalLayout_24.addWidget(self.legal_s_combobox)
        self.verticalLayout_23.addLayout(self.verticalLayout_24)
        self.gridLayout.addWidget(self.legal_s_container_w, 0, 6, 1, 1)
        self.pid_container_w = QtWidgets.QWidget(parent=self.search_container)
        self.pid_container_w.setObjectName("pid_container_w")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pid_container_w)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pid_label = QtWidgets.QLabel(parent=self.pid_container_w)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pid_label.setFont(font)
        self.pid_label.setStyleSheet("margin: 0;")
        self.pid_label.setObjectName("pid_label")
        self.verticalLayout.addWidget(self.pid_label)
        self.pid_input = QtWidgets.QLineEdit(parent=self.pid_container_w)
        self.pid_input.setStyleSheet("margin: 0;\n" "padding-left: 4px;")
        self.pid_input.setObjectName("pid_input")
        self.verticalLayout.addWidget(self.pid_input)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.pid_container_w, 1, 0, 1, 1)
        self.street_container_w = QtWidgets.QWidget(parent=self.search_container)
        self.street_container_w.setObjectName("street_container_w")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.street_container_w)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.street_label = QtWidgets.QLabel(parent=self.street_container_w)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.street_label.setFont(font)
        self.street_label.setStyleSheet("margin: 0;")
        self.street_label.setObjectName("street_label")
        self.verticalLayout_4.addWidget(self.street_label)
        self.street_input = QtWidgets.QLineEdit(parent=self.street_container_w)
        self.street_input.setStyleSheet("margin: 0;\n" "padding-left: 4px;")
        self.street_input.setObjectName("street_input")
        self.verticalLayout_4.addWidget(self.street_input)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.gridLayout.addWidget(self.street_container_w, 1, 1, 1, 1)
        self.area_container_w = QtWidgets.QWidget(parent=self.search_container)
        self.area_container_w.setObjectName("area_container_w")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.area_container_w)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.area_label = QtWidgets.QLabel(parent=self.area_container_w)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.area_label.setFont(font)
        self.area_label.setStyleSheet("margin: 0;")
        self.area_label.setObjectName("area_label")
        self.verticalLayout_6.addWidget(self.area_label)
        self.area_input = QtWidgets.QLineEdit(parent=self.area_container_w)
        self.area_input.setStyleSheet("margin: 0;\n" "padding-left: 4px;")
        self.area_input.setObjectName("area_input")
        self.verticalLayout_6.addWidget(self.area_input)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.gridLayout.addWidget(self.area_container_w, 1, 6, 1, 1)
        self.price_container_w = QtWidgets.QWidget(parent=self.search_container)
        self.price_container_w.setObjectName("price_container_w")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.price_container_w)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.price_label = QtWidgets.QLabel(parent=self.price_container_w)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.price_label.setFont(font)
        self.price_label.setStyleSheet("margin: 0;")
        self.price_label.setObjectName("price_label")
        self.verticalLayout_12.addWidget(self.price_label)
        self.price_input = QtWidgets.QLineEdit(parent=self.price_container_w)
        self.price_input.setStyleSheet("margin: 0;\n" "padding-left: 4px;")
        self.price_input.setObjectName("price_input")
        self.verticalLayout_12.addWidget(self.price_input)
        self.verticalLayout_11.addLayout(self.verticalLayout_12)
        self.gridLayout.addWidget(self.price_container_w, 1, 3, 1, 1)
        self.structure_container_w = QtWidgets.QWidget(parent=self.search_container)
        self.structure_container_w.setObjectName("structure_container_w")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.structure_container_w)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.structure_label = QtWidgets.QLabel(parent=self.structure_container_w)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(10)
        self.structure_label.setFont(font)
        self.structure_label.setStyleSheet("margin: 0;")
        self.structure_label.setObjectName("structure_label")
        self.verticalLayout_8.addWidget(self.structure_label)
        self.structure_input = QtWidgets.QLineEdit(parent=self.structure_container_w)
        self.structure_input.setStyleSheet("margin: 0;\n" "padding-left: 4px;")
        self.structure_input.setObjectName("structure_input")
        self.verticalLayout_8.addWidget(self.structure_input)
        self.verticalLayout_7.addLayout(self.verticalLayout_8)
        self.gridLayout.addWidget(self.structure_container_w, 1, 5, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout_27.addWidget(self.search_container)
        self.actions_container_w = QtWidgets.QGroupBox(parent=self.contents_container_w)
        self.actions_container_w.setStyleSheet("")
        self.actions_container_w.setTitle("")
        self.actions_container_w.setObjectName("actions_container_w")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.actions_container_w)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.action_create_btn = QtWidgets.QPushButton(parent=self.actions_container_w)
        self.action_create_btn.setObjectName("action_create_btn")
        self.horizontalLayout.addWidget(self.action_create_btn)
        self.action_upload_btn = QtWidgets.QPushButton(parent=self.actions_container_w)
        self.action_upload_btn.setObjectName("action_upload_btn")
        self.horizontalLayout.addWidget(self.action_upload_btn)
        self.action_download_btn = QtWidgets.QPushButton(
            parent=self.actions_container_w
        )
        self.action_download_btn.setObjectName("action_download_btn")
        self.horizontalLayout.addWidget(self.action_download_btn)
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_27.addWidget(self.actions_container_w)
        self.products_table = QtWidgets.QTableView(parent=self.contents_container_w)
        self.products_table.setObjectName("products_table")
        self.verticalLayout_27.addWidget(self.products_table)
        self.verticalLayout_28.addLayout(self.verticalLayout_27)
        self.horizontalLayout_5.addWidget(self.contents_container_w)
        self.line = QtWidgets.QFrame(parent=REProduct)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        self.details_container_w = QtWidgets.QWidget(parent=REProduct)
        self.details_container_w.setObjectName("details_container_w")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.details_container_w)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.image_label = QtWidgets.QLabel(parent=self.details_container_w)
        self.image_label.setMinimumSize(QtCore.QSize(0, 200))
        self.image_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.verticalLayout_17.addWidget(self.image_label)
        self.detail_text = QtWidgets.QPlainTextEdit(parent=self.details_container_w)
        self.detail_text.setObjectName("detail_text")
        self.verticalLayout_17.addWidget(self.detail_text)
        self.detail_action_container_w = QtWidgets.QGroupBox(
            parent=self.details_container_w
        )
        self.detail_action_container_w.setTitle("")
        self.detail_action_container_w.setObjectName("detail_action_container_w")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.detail_action_container_w)
        self.horizontalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.action_default_btn = QtWidgets.QPushButton(
            parent=self.detail_action_container_w
        )
        self.action_default_btn.setObjectName("action_default_btn")
        self.horizontalLayout_3.addWidget(self.action_default_btn)
        self.action_random_btn = QtWidgets.QPushButton(
            parent=self.detail_action_container_w
        )
        self.action_random_btn.setObjectName("action_random_btn")
        self.horizontalLayout_3.addWidget(self.action_random_btn)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_17.addWidget(self.detail_action_container_w)
        self.verticalLayout_18.addLayout(self.verticalLayout_17)
        self.horizontalLayout_5.addWidget(self.details_container_w)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)

        self.retranslateUi(REProduct)
        QtCore.QMetaObject.connectSlotsByName(REProduct)

    def retranslateUi(self, REProduct):
        _translate = QtCore.QCoreApplication.translate
        REProduct.setWindowTitle(_translate("REProduct", "Form"))
        self.furniture_label.setText(_translate("REProduct", "Công năng"))
        self.wards_label.setText(_translate("REProduct", "Phường"))
        self.wards_combobox.setItemText(0, _translate("REProduct", "Tất cả"))
        self.options_label.setText(_translate("REProduct", "Loại hình kinh doanh"))
        self.options_combobox.setItemText(0, _translate("REProduct", "Tất cả"))
        self.categories_label.setText(_translate("REProduct", "Danh mục bất động sản"))
        self.categories_combobox.setItemText(0, _translate("REProduct", "Tất cả"))
        self.building_line_s_label.setText(_translate("REProduct", "Lộ giới"))
        self.building_line_s_combobox.setItemText(0, _translate("REProduct", "Tất cả"))
        self.furniture_s_lable.setText(_translate("REProduct", "Nội thất"))
        self.furniture_s_combobox.setItemText(0, _translate("REProduct", "Tất cả"))
        self.legal_s_label.setText(_translate("REProduct", "Pháp lý"))
        self.legal_s_combobox.setItemText(0, _translate("REProduct", "Tất cả"))
        self.pid_label.setText(_translate("REProduct", "PID"))
        self.street_label.setText(_translate("REProduct", "Tên đường"))
        self.area_label.setText(_translate("REProduct", "Diện tích"))
        self.price_label.setText(_translate("REProduct", "Giá"))
        self.structure_label.setText(_translate("REProduct", "Kết cấu"))
        self.action_create_btn.setText(_translate("REProduct", "Create new"))
        self.action_upload_btn.setText(_translate("REProduct", "Upload"))
        self.action_download_btn.setText(_translate("REProduct", "Download"))
        self.image_label.setText(_translate("REProduct", "Images"))
        self.action_default_btn.setText(_translate("REProduct", "Default"))
        self.action_random_btn.setText(_translate("REProduct", "Random"))
