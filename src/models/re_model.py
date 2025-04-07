# src/models/re_model.py
from PyQt6.QtSql import QSqlRelationalTableModel, QSqlRelation, QSqlTableModel
from PyQt6.QtCore import Qt
from src import constants


class REProductRelationalModel(QSqlRelationalTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTable(constants.RE_PRODUCT_TABLE)
        self.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnManualSubmit)

        self._set_relations()
        self._column_headers = {
            self.fieldIndex("pid"): "pid".title(),
            self.fieldIndex("ward_id"): "ward".title(),
            "relation-ward_id": "ward".title(),
            self.fieldIndex("street"): "street".title(),
            self.fieldIndex("status_id"): "status".title(),
            self.fieldIndex("province_id"): "province".title(),
            self.fieldIndex("district_id"): "district".title(),
            self.fieldIndex("option_id"): "option".title(),
            self.fieldIndex("category_id"): "category".title(),
            self.fieldIndex("building_line_id"): "building_line".title(),
            self.fieldIndex("furniture_id"): "furniture".title(),
            self.fieldIndex("legal_id"): "legal".title(),
            self.fieldIndex("area"): "area".title(),
            self.fieldIndex("structure"): "structure".title(),
            self.fieldIndex("function"): "function".title(),
            self.fieldIndex("description"): "description".title(),
            self.fieldIndex("price"): "price".title(),
            "relation-status_id": "status".title(),
            "relation-province_id": "province".title(),
            "relation-district_id": "district".title(),
            "relation-option_id": "option".title(),
            "relation-category_id": "category".title(),
            "relation-building_line_id": "building_line".title(),
            "relation-legal_id": "legal".title(),
            "relation-furniture_id": "furniture".title(),
        }
        self.select()

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

    def _set_relations(self):
        self.setRelation(
            self.fieldIndex("status_id"),
            QSqlRelation(constants.RE_SETTING_STATUS_TABLE, "id", "label_vi"),
        )
        self.setRelation(
            self.fieldIndex("province_id"),
            QSqlRelation(constants.RE_SETTING_PROVINCES_TABLE, "id", "label_vi"),
        )
        self.setRelation(
            self.fieldIndex("district_id"),
            QSqlRelation(constants.RE_SETTING_DISTRICTS_TABLE, "id", "label_vi"),
        )
        self.setRelation(
            self.fieldIndex("ward_id"),
            QSqlRelation(constants.RE_SETTING_WARDS_TABLE, "id", "label_vi"),
        )
        self.setRelation(
            self.fieldIndex("option_id"),
            QSqlRelation(constants.RE_SETTING_OPTIONS_TABLE, "id", "label_vi"),
        )
        self.setRelation(
            self.fieldIndex("category_id"),
            QSqlRelation(constants.RE_SETTING_CATEGORIES_TABLE, "id", "label_vi"),
        )
        self.setRelation(
            self.fieldIndex("building_line_id"),
            QSqlRelation(constants.RE_SETTING_BUILDING_LINES_TABLE, "id", "label_vi"),
        )
        self.setRelation(
            self.fieldIndex("legal_id"),
            QSqlRelation(constants.RE_SETTING_LEGALS_TABLE, "id", "label_vi"),
        )
        self.setRelation(
            self.fieldIndex("furniture_id"),
            QSqlRelation(constants.RE_SETTING_FURNITURES_TABLE, "id", "label_vi"),
        )

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            # Tiêu đề cho các cột dữ liệu trực tiếp từ bảng re_products
            if section in self._column_headers:
                return self._column_headers[section]

            # Tiêu đề cho các cột quan hệ (hiển thị giá trị từ bảng liên kết)
            for field_name in [
                "status_id",
                "province_id",
                "district_id",
                "ward_id",
                "option_id",
                "category_id",
                "building_line_id",
                "legal_id",
                "furniture_id",
            ]:
                relation_index = self.fieldIndex(field_name)
                if self.relation(relation_index).isValid():
                    if (
                        self.relation(relation_index).displayColumn() == 2
                        and self.relation(relation_index).indexInRelatedTable()
                        == section - self.columnCount()
                    ):
                        return self._column_headers.get(
                            f"relation-{field_name}",
                            field_name.replace("_id", "").title(),
                        )

            # Nếu không tìm thấy, gọi headerData mặc định của lớp cha
            return super().headerData(section, orientation, role)
        return super().headerData(section, orientation, role)

    def get_record_id(self, row):
        if 0 <= row < self.rowCount():
            index = self.index(row, self.fieldIndex("id"))
            return self.data(index)
        return None


class BaseSettingModel(QSqlTableModel):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.setTable(table_name)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.select()

    def flags(self, index):
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsEditable
        )


# class RETemplateTitleModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_TEMPLATE_TITLE_TABLE, parent)


# class RETemplateDescriptionModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_TEMPLATE_DESCRIPTION_TABLE, parent)


# class RESettingStatusesModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_SETTING_STATUS_TABLE, parent)


# class RESettingProvincesModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_SETTING_PROVINCES_TABLE, parent)


# class RESettingDistrictsModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_SETTING_DISTRICTS_TABLE, parent)


# class RESettingWardsModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_SETTING_WARDS_TABLE, parent)


# class RESettingOptionsModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_SETTING_OPTIONS_TABLE, parent)


# class RESettingCategoriesModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_SETTING_CATEGORIES_TABLE, parent)


# class RESettingBuildingLinesModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_SETTING_BUILDING_LINES_TABLE, parent)


# class RESettingLegalsModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_SETTING_LEGALS_TABLE, parent)


# class RESettingFurnituresModel(BaseSettingModel):
#     def __init__(self, parent=None):
#         super().__init__(constants.RE_SETTING_FURNITURES_TABLE, parent)
