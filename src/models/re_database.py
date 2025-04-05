# src/models/re_database.py
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from src import constants


def initialize_re_products():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("./src/data/real_estate.db")
    if not db.open():
        print(f"Error opening database: {db.lastError().text()}")
        return False
    query = QSqlQuery(db)
    query.exec("PRAGMA foreign_keys = ON;")
    if not _init_re(query):
        db.close()
        return False
    provinces = [{"label_vi": "lâm đồng",
                  "label_en": "lam dong", "value": "lam_dong"}]
    districts = [
        {"label_vi": "đà lạt", "label_en": "da lat", "value": "da_lat"},
    ]
    wards = [
        {"label_vi": "phường 1", "label_en": "ward 1", "value": "1"},
        {"label_vi": "phường 2", "label_en": "ward 2", "value": "2"},
        {"label_vi": "phường 3", "label_en": "ward 3", "value": "3"},
        {"label_vi": "phường 4", "label_en": "ward 4", "value": "4"},
        {"label_vi": "phường 5", "label_en": "ward 5", "value": "5"},
        {"label_vi": "phường 6", "label_en": "ward 6", "value": "6"},
        {"label_vi": "phường 7", "label_en": "ward 7", "value": "7"},
        {"label_vi": "phường 8", "label_en": "ward 8", "value": "8"},
        {"label_vi": "phường 9", "label_en": "ward 9", "value": "9"},
        {"label_vi": "phường 10", "label_en": "ward 10", "value": "10"},
        {"label_vi": "phường 11", "label_en": "ward 11", "value": "11"},
        {"label_vi": "phường 12", "label_en": "ward 12", "value": "12"},
        {"label_vi": "xã trạm hành", "label_en": "ward tram hanh", "value": "tram_hanh"},
        {"label_vi": "xã tà nung", "label_en": "ward ta nung", "value": "ta_nung"},
        {"label_vi": "xã xuân trường",
            "label_en": "ward xuan truong", "value": "xuan_truong"},
        {"label_vi": "xã xuân thọ", "label_en": "ward xuan tho", "value": "xuan_tho"},
    ]
    options = [
        {"label_vi": "bán", "label_en": "sell", "value": "sell"},
        {"label_vi": "cho thuê", "label_en": "rent", "value": "rent"},
        {"label_vi": "sang nhượng", "label_en": "assignment", "value": "assignment"},
    ]
    categories = [
        {"label_vi": "nhà phố", "label_en": "private house", "value": "private_house"},
        {"label_vi": "nhà mặt tiền", "label_en": "shop house", "value": "shop_house"},
        {"label_vi": "biệt thự", "label_en": "villa", "value": "villa"},
        {"label_vi": "đất nền", "label_en": "land", "value": "land"},
        {"label_vi": "căn hộ/ chung cư",
            "label_en": "apartment", "value": "apartment"},
        {"label_vi": "homestay", "label_en": "homestay", "value": "homestay"},
        {"label_vi": "khách sạn", "label_en": "hotel", "value": "hotel"},
        {"label_vi": "kho/bãi", "label_en": "workshop", "value": "workshop"},
        {"label_vi": "MBKD", "label_en": "retail space", "value": "retail_space"},
        {"label_vi": "coffee house", "label_en": "coffee house",
            "value": "coffee_house"},
        {"label_vi": "nhà hàng", "label_en": "restaurant", "value": "restaurant"},
    ]
    building_lines = [
        {"label_vi": "đường xe hơi", "label_en": "big road", "value": "big_road"},
        {"label_vi": "đường xe máy", "label_en": "small road", "value": "small_road"},
    ]
    legals = [
        {"label_vi": "giấy tờ tay", "label_en": "none", "value": "none"},
        {"label_vi": "sổ nông nghiệp chung", "label_en": "snnc", "value": "snnc"},
        {"label_vi": "sổ nông nghiệp phân quyền",
            "label_en": "snnpq", "value": "snnpq"},
        {"label_vi": "sổ nông nghiệp riêng", "label_en": "snnr", "value": "snnr"},
        {"label_vi": "sổ xây dựng chung", "label_en": "sxdc", "value": "sxdc"},
        {"label_vi": "sổ xây dựng phân quyền",
            "label_en": "sxdpq", "value": "sxdpq"},
        {"label_vi": "sổ xây dựng riêng", "label_en": "sxdr", "value": "sxdr"},
    ]
    furnitures = [
        {"label_vi": "không nội thất", "label_en": "none", "value": "none"},
        {"label_vi": "nội thất cơ bản", "label_en": "basic", "value": "basic"},
        {"label_vi": "đầy đủ nội thất", "label_en": "full", "value": "full"},
    ]

    if not _init_deps(query, constants.RE_SETTING_PROVINCES_TABLE, provinces):
        db.close()
        return False
    if not _init_deps(query, constants.RE_SETTING_DISTRICTS_TABLE, districts):
        db.close()
        return False
    if not _init_deps(query, constants.RE_SETTING_WARDS_TABLE, wards):
        db.close()
        return False
    if not _init_deps(query, constants.RE_SETTING_OPTIONS_TABLE, options):
        db.close()
        return False
    if not _init_deps(query, constants.RE_SETTING_CATEGORIES_TABLE, categories):
        db.close()
        return False
    if not _init_deps(query, constants.RE_SETTING_BUILDING_LINES_TABLE, building_lines):
        db.close()
        return False
    if not _init_deps(query, constants.RE_SETTING_LEGALS_TABLE, legals):
        db.close()
        return False
    if not _init_deps(query, constants.RE_SETTING_FURNITURES_TABLE, furnitures):
        db.close()
        return False

    db.close()
    return True


def _init_re(query):
    query.exec(f"""
               CREATE TABLE IF NOT EXISTS {constants.RE_PRODUCT_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pid TEXT UNIQUE NOT NULL,
                province_id INTEGER,
                district_id INTEGER,
                ward_id INTEGER,
                option_id INTEGER,
                category_id INTEGER,
                building_line_id INTEGER,
                furniture_id INTEGER,
                legal_id INTEGER,
                area REAL,
                structure REAL,
                function TEXT,
                description TEXT,
                price REAL,
                status INTEGER DEFAULT 1,
                created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                updated_at TEXT,
                FOREIGN KEY (province_id) REFERENCES {constants.RE_SETTING_PROVINCES_TABLE}(id),
                FOREIGN KEY (district_id) REFERENCES {constants.RE_SETTING_DISTRICTS_TABLE}(id),
                FOREIGN KEY (ward_id) REFERENCES {constants.RE_SETTING_WARDS_TABLE}(id),
                FOREIGN KEY (option_id) REFERENCES {constants.RE_SETTING_OPTIONS_TABLE}(id),
                FOREIGN KEY (category_id) REFERENCES {constants.RE_SETTING_CATEGORIES_TABLE}(id),
                FOREIGN KEY (building_line_id) REFERENCES {constants.RE_SETTING_BUILDING_LINES_TABLE}(id),
                FOREIGN KEY (furniture_id) REFERENCES {constants.RE_SETTING_FURNITURES_TABLE}(id),
                FOREIGN KEY (legal_id) REFERENCES {constants.RE_SETTING_LEGALS_TABLE}(id)
               )
               """)
    if query.lastError().isValid():
        print(
            f"Error creating table '{constants.RE_PRODUCT_TABLE}': {query.lastError().text()}")
        return False
    return True


def _init_deps(query, table_name, fields):
    query.exec(f"""CREATE TABLE IF NOT EXISTS {table_name} (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               label_vi TEXT,
               label_en TEXT,
               value TEXT UNIQUE NOT NULL,
               created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
               updated_at TEXT,
               )""")
    if query.lastError().isValid():
        print(
            f"Error creating table '{table_name}': {query.lastError().text()}")
        return False
    query.prepare(f"""
                  INSERT OR IGNORE INTO {table_name}(label_vi, label_en, value)
                  VALUES (:label_vi, :label_en, :value)
                  """)
    for field in fields:
        query.bindValue(":label_vi", field.get("label_vi", ""))
        query.bindValue(":label_en", field.get("label_en", ""))
        query.bindValue(":value", field.get("value", ""))
        if not query.exec():
            print(
                f"Error inserting into '{table_name}': {query.lastError().text()}")
            return False

    return True
