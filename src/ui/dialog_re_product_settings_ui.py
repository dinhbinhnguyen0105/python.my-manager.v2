# Form implementation generated from reading ui file '/Volumes/KINGSTON/Dev/python/python.my-manager.v2/ui/dialog_re_product_settings.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_REProductSettings(object):
    def setupUi(self, Dialog_REProductSettings):
        Dialog_REProductSettings.setObjectName("Dialog_REProductSettings")
        Dialog_REProductSettings.resize(535, 346)
        Dialog_REProductSettings.setStyleSheet("QDialog {\n"
"    font-family: \"Courier New\";\n"
"}\n"
"QLabel{\n"
"    font-size: 10px;\n"
"    font-weight: 600;\n"
"    color: rgb(90, 93, 97);\n"
"    max-height: 14px;\n"
"}\n"
"QLineEdit {\n"
"padding: 4px 0;\n"
"border: 1px solid #CED4DA;\n"
"border-radius: 8px;\n"
"margin-left: 8px;\n"
"padding-left: 4px;\n"
"}\n"
"QRadioButton{\n"
"font-family: \"Courier New\";\n"
"}")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Dialog_REProductSettings)
        self.verticalLayout_5.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_4.setSpacing(8)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(parent=Dialog_REProductSettings)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_5.setContentsMargins(8, 4, 8, 4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.districts_radio = QtWidgets.QRadioButton(parent=self.groupBox)
        self.districts_radio.setObjectName("districts_radio")
        self.gridLayout_4.addWidget(self.districts_radio, 0, 4, 1, 1)
        self.categories_radio = QtWidgets.QRadioButton(parent=self.groupBox)
        self.categories_radio.setObjectName("categories_radio")
        self.gridLayout_4.addWidget(self.categories_radio, 0, 2, 1, 1)
        self.legal_s_radio = QtWidgets.QRadioButton(parent=self.groupBox)
        self.legal_s_radio.setObjectName("legal_s_radio")
        self.gridLayout_4.addWidget(self.legal_s_radio, 1, 3, 1, 1)
        self.furniture_s_radio = QtWidgets.QRadioButton(parent=self.groupBox)
        self.furniture_s_radio.setObjectName("furniture_s_radio")
        self.gridLayout_4.addWidget(self.furniture_s_radio, 1, 4, 1, 1)
        self.provinces_radio = QtWidgets.QRadioButton(parent=self.groupBox)
        self.provinces_radio.setObjectName("provinces_radio")
        self.gridLayout_4.addWidget(self.provinces_radio, 0, 3, 1, 1)
        self.options_radio = QtWidgets.QRadioButton(parent=self.groupBox)
        self.options_radio.setObjectName("options_radio")
        self.gridLayout_4.addWidget(self.options_radio, 0, 1, 1, 1)
        self.statuses_radio = QtWidgets.QRadioButton(parent=self.groupBox)
        self.statuses_radio.setObjectName("statuses_radio")
        self.gridLayout_4.addWidget(self.statuses_radio, 0, 0, 1, 1)
        self.wards_radio = QtWidgets.QRadioButton(parent=self.groupBox)
        self.wards_radio.setObjectName("wards_radio")
        self.gridLayout_4.addWidget(self.wards_radio, 1, 0, 1, 1)
        self.building_line_s_radio = QtWidgets.QRadioButton(parent=self.groupBox)
        self.building_line_s_radio.setObjectName("building_line_s_radio")
        self.gridLayout_4.addWidget(self.building_line_s_radio, 1, 1, 1, 2)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.field_container = QtWidgets.QGroupBox(parent=Dialog_REProductSettings)
        self.field_container.setTitle("")
        self.field_container.setObjectName("field_container")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.field_container)
        self.horizontalLayout_2.setContentsMargins(8, 4, 8, 4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name_en_container = QtWidgets.QWidget(parent=self.field_container)
        self.name_en_container.setStyleSheet("")
        self.name_en_container.setObjectName("name_en_container")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.name_en_container)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.name_en_label = QtWidgets.QLabel(parent=self.name_en_container)
        self.name_en_label.setObjectName("name_en_label")
        self.verticalLayout_2.addWidget(self.name_en_label)
        self.name_en_input = QtWidgets.QLineEdit(parent=self.name_en_container)
        self.name_en_input.setObjectName("name_en_input")
        self.verticalLayout_2.addWidget(self.name_en_input)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.name_en_container)
        self.name_vi_container = QtWidgets.QWidget(parent=self.field_container)
        self.name_vi_container.setStyleSheet("")
        self.name_vi_container.setObjectName("name_vi_container")
        self.gridLayout = QtWidgets.QGridLayout(self.name_vi_container)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_v_label = QtWidgets.QLabel(parent=self.name_vi_container)
        self.name_v_label.setObjectName("name_v_label")
        self.verticalLayout.addWidget(self.name_v_label)
        self.name_v_input = QtWidgets.QLineEdit(parent=self.name_vi_container)
        self.name_v_input.setObjectName("name_v_input")
        self.verticalLayout.addWidget(self.name_v_input)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.name_vi_container)
        self.value_container = QtWidgets.QWidget(parent=self.field_container)
        self.value_container.setStyleSheet("")
        self.value_container.setObjectName("value_container")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.value_container)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.value_label = QtWidgets.QLabel(parent=self.value_container)
        self.value_label.setObjectName("value_label")
        self.verticalLayout_3.addWidget(self.value_label)
        self.value_input = QtWidgets.QLineEdit(parent=self.value_container)
        self.value_input.setObjectName("value_input")
        self.verticalLayout_3.addWidget(self.value_input)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.value_container)
        self.create_btn = QtWidgets.QPushButton(parent=self.field_container)
        self.create_btn.setObjectName("create_btn")
        self.horizontalLayout.addWidget(self.create_btn)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addWidget(self.field_container)
        self.tableView = QtWidgets.QTableView(parent=Dialog_REProductSettings)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_4.addWidget(self.tableView)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.delete_btn = QtWidgets.QPushButton(parent=Dialog_REProductSettings)
        self.delete_btn.setObjectName("delete_btn")
        self.horizontalLayout_3.addWidget(self.delete_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog_REProductSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_5.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_REProductSettings)
        self.buttonBox.accepted.connect(Dialog_REProductSettings.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog_REProductSettings.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog_REProductSettings)
        Dialog_REProductSettings.setTabOrder(self.statuses_radio, self.options_radio)
        Dialog_REProductSettings.setTabOrder(self.options_radio, self.categories_radio)
        Dialog_REProductSettings.setTabOrder(self.categories_radio, self.provinces_radio)
        Dialog_REProductSettings.setTabOrder(self.provinces_radio, self.districts_radio)
        Dialog_REProductSettings.setTabOrder(self.districts_radio, self.wards_radio)
        Dialog_REProductSettings.setTabOrder(self.wards_radio, self.building_line_s_radio)
        Dialog_REProductSettings.setTabOrder(self.building_line_s_radio, self.legal_s_radio)
        Dialog_REProductSettings.setTabOrder(self.legal_s_radio, self.furniture_s_radio)
        Dialog_REProductSettings.setTabOrder(self.furniture_s_radio, self.name_en_input)
        Dialog_REProductSettings.setTabOrder(self.name_en_input, self.name_v_input)
        Dialog_REProductSettings.setTabOrder(self.name_v_input, self.create_btn)
        Dialog_REProductSettings.setTabOrder(self.create_btn, self.value_input)
        Dialog_REProductSettings.setTabOrder(self.value_input, self.tableView)
        Dialog_REProductSettings.setTabOrder(self.tableView, self.delete_btn)

    def retranslateUi(self, Dialog_REProductSettings):
        _translate = QtCore.QCoreApplication.translate
        Dialog_REProductSettings.setWindowTitle(_translate("Dialog_REProductSettings", "Dialog"))
        self.districts_radio.setText(_translate("Dialog_REProductSettings", "Districts"))
        self.categories_radio.setText(_translate("Dialog_REProductSettings", "Categories"))
        self.legal_s_radio.setText(_translate("Dialog_REProductSettings", "Legal"))
        self.furniture_s_radio.setText(_translate("Dialog_REProductSettings", "Funiture"))
        self.provinces_radio.setText(_translate("Dialog_REProductSettings", "Provinces"))
        self.options_radio.setText(_translate("Dialog_REProductSettings", "Options"))
        self.statuses_radio.setText(_translate("Dialog_REProductSettings", "Status"))
        self.wards_radio.setText(_translate("Dialog_REProductSettings", "Wards"))
        self.building_line_s_radio.setText(_translate("Dialog_REProductSettings", "Building line"))
        self.name_en_label.setText(_translate("Dialog_REProductSettings", "name_en"))
        self.name_v_label.setText(_translate("Dialog_REProductSettings", "name_vi"))
        self.value_label.setText(_translate("Dialog_REProductSettings", "value"))
        self.create_btn.setText(_translate("Dialog_REProductSettings", "Add new"))
        self.delete_btn.setText(_translate("Dialog_REProductSettings", "Delete"))
