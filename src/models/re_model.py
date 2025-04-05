# src/models/re_model.py
from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtCore import Qt
from src import constants


class BaseSettingModel(QSqlTableModel):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.setTable(table_name)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.select()

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable


class REProductModel(BaseSettingModel):
    def __init__(self, parent=None):
        super().__init__(constants.RE_PRODUCT_TABLE, parent)


class RESettingProvincesModel(BaseSettingModel):
    def __init__(self, parent=None):
        super().__init__(constants.RE_SETTING_PROVINCES_TABLE, parent)


class RESettingDistrictsModel(BaseSettingModel):
    def __init__(self, parent=None):
        super().__init__(constants.RE_SETTING_DISTRICTS_TABLE, parent)


class RESettingWardsModel(BaseSettingModel):
    def __init__(self, parent=None):
        super().__init__(constants.RE_SETTING_WARDS_TABLE, parent)


class RESettingOptionsModel(BaseSettingModel):
    def __init__(self, parent=None):
        super().__init__(constants.RE_SETTING_OPTIONS_TABLE, parent)


class RESettingCategoriesModel(BaseSettingModel):
    def __init__(self, parent=None):
        super().__init__(constants.RE_SETTING_CATEGORIES_TABLE, parent)


class RESettingBuildingLinesModel(BaseSettingModel):
    def __init__(self, parent=None):
        super().__init__(constants.RE_SETTING_BUILDING_LINES_TABLE, parent)


class RESettingLegalsModel(BaseSettingModel):
    def __init__(self, parent=None):
        super().__init__(constants.RE_SETTING_LEGALS_TABLE, parent)


class RESettingFurnituresModel(BaseSettingModel):
    def __init__(self, parent=None):
        super().__init__(constants.RE_SETTING_FURNITURES_TABLE, parent)
