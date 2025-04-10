# src/services/re_service.py
import datetime
import os
import shutil
from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from src import constants


def copy_files(sources, destination, id):
    os.makedirs(destination, exist_ok=True)
    destination_img_num = len(get_images_in_directory(destination))

    for index, file in enumerate(sources):
        _, extension = os.path.splitext(file)
        file_name = f"{id}_{index + destination_img_num}{extension}"
        destination_path = os.path.join(destination, file_name)
        try:
            shutil.copy2(file, destination_path)
        except FileNotFoundError:
            print(f"Error: File not found: {file}")
            return False
        except Exception as e:
            print(f"Error copying {file}: {e}")
            return False
    return True


def get_images_in_directory(image_dir):
    if not os.path.exists(image_dir):
        return []
    images = []
    for file in os.listdir(image_dir):
        if file.endswith((".png", ".jpg", ".jpeg")):
            images.append(os.path.join(image_dir, file))
    return images


def validate_foreign_keys(data):
    validations = [
        ("province_id", constants.RE_SETTING_PROVINCES_TABLE),
        ("district_id", constants.RE_SETTING_DISTRICTS_TABLE),
        ("ward_id", constants.RE_SETTING_WARDS_TABLE),
        ("option_id", constants.RE_SETTING_OPTIONS_TABLE),
        ("category_id", constants.RE_SETTING_CATEGORIES_TABLE),
        ("building_line_id", constants.RE_SETTING_BUILDING_LINES_TABLE),
        ("furniture_id", constants.RE_SETTING_FURNITURES_TABLE),
        ("legal_id", constants.RE_SETTING_LEGALS_TABLE),
    ]
    for field, table in validations:
        value = data.get(field)
        if value is not None:
            query = QSqlQuery()
            query.prepare(f"SELECT COUNT(*) FROM {table} WHERE id=:id")
            query.bindValue(":id", value)
            if not query.exec():
                raise Exception(
                    f"Error executing validation query for {field}: {query.lastError().text()}"
                )
            if query.next():
                count = query.value(0)
                if count == 0:
                    raise Exception(
                        f"Validation failed: {field} value '{value}' does not exist in the table '{table}'"
                    )
            else:
                raise Exception(
                    f"Error retrieving result for validation of {field}.")
    return True


class REProductService:
    @staticmethod
    def create(data):
        db = QSqlDatabase.database()
        if not db.transaction():
            raise Exception("Failed to start transaction.")
        try:
            try:
                if not validate_foreign_keys(data):
                    return False
            except Exception as e_validate:
                db.rollback()
                raise e_validate
            query = QSqlQuery()
            query.prepare(
                f"""
            INSERT INTO {constants.RE_PRODUCT_TABLE} (
                pid, province_id, district_id, ward_id, street,
                option_id, category_id, building_line_id, 
                furniture_id, legal_id, area, structure,
                function, description, price, status_id, image_dir, updated_at
            ) VALUES (
                :pid, :province_id, :district_id, :ward_id, :street,
                :option_id, :category_id, :building_line_id,
                :furniture_id, :legal_id, :area, :structure,
                :function, :description, :price, :status_id, :image_dir, :updated_at
            )
        """
            )
            now = datetime.datetime.now()
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            data.setdefault("updated_at", formatted_time)
            img_dir_default = os.path.join(
                "repositories",
                "images",
                "re",
            )
            if not data.get("image_dir"):
                data["image_dir"] = img_dir_default
            for key in REProductService.get_columns():
                if key != "id":
                    query.bindValue(f":{key}", data.get(key))

            if not query.exec():
                db.rollback()
                raise Exception(
                    f"Error inserting record: {query.lastError().text()}")
            id = None
            last_id_query = QSqlQuery(db)
            if last_id_query.exec("SELECT last_insert_rowid();"):
                if last_id_query.next():
                    id = last_id_query.value(0)
            else:
                db.rollback()
                raise Exception(
                    f"Error get the ID of the latest record: {last_id_query.lastError().text()}"
                )
            if not id:
                db.rollback()
                return False
            image_dir = os.path.join(data.get("image_dir"), str(id))

            update_query = QSqlQuery(db)
            update_query.prepare(
                f"""
                UPDATE {constants.RE_PRODUCT_TABLE}
                SET image_dir = :image_dir
                WHERE id = :id
                """
            )
            update_query.bindValue(":image_dir", image_dir)
            update_query.bindValue(":id", id)
            if not update_query.exec():
                db.rollback()
                raise Exception(
                    f"Error updating image_dir: {update_query.lastError().text()}"
                )
            if not data.get("image_paths"):
                raise Exception("Invalid images.")
            if not copy_files(data["image_paths"], image_dir, str(id)):
                db.rollback()
                raise Exception("Failed to copy all image files.")

            if not db.commit():
                db.rollback()
                raise Exception("Failed to commit transaction.")
            return True

        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def read(record_id):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(
            f"""
                   SELECT
                    tp.id,
                    tp.pid,
                    tp.street,
                    tp.area,
                    tp.structure,
                    tp.function,
                    tp.description,
                    tp.price,
                    tp.image_dir,
                    tp.updated_at,
                    ts_status.label_vi as status,
                    ts_province.label_vi AS province,
                    ts_district.label_vi AS district,
                    ts_ward.label_vi AS ward,
                    ts_option.label_vi AS option,
                    ts_category.label_vi AS category,
                    ts_building_line.label_vi AS building_line,
                    ts_furniture.label_vi AS furniture,
                    ts_legal.label_vi AS legal
                FROM {constants.RE_PRODUCT_TABLE} tp
                JOIN {constants.RE_SETTING_STATUS_TABLE} ts_status ON tp.status_id = ts_status.id
                LEFT JOIN {constants.RE_SETTING_PROVINCES_TABLE} ts_province ON tp.province_id = ts_province.id
                LEFT JOIN {constants.RE_SETTING_DISTRICTS_TABLE} ts_district ON tp.district_id = ts_district.id
                LEFT JOIN {constants.RE_SETTING_WARDS_TABLE} ts_ward ON tp.ward_id = ts_ward.id
                LEFT JOIN {constants.RE_SETTING_OPTIONS_TABLE} ts_option ON tp.option_id = ts_option.id
                LEFT JOIN {constants.RE_SETTING_CATEGORIES_TABLE} ts_category ON tp.category_id = ts_category.id
                LEFT JOIN {constants.RE_SETTING_BUILDING_LINES_TABLE} ts_building_line ON tp.building_line_id = ts_building_line.id
                LEFT JOIN {constants.RE_SETTING_FURNITURES_TABLE} ts_furniture ON tp.furniture_id = ts_furniture.id
                LEFT JOIN {constants.RE_SETTING_LEGALS_TABLE} ts_legal ON tp.legal_id = ts_legal.id
                   WHERE tp.id=:id
                   """
        )
        query.bindValue(":id", record_id)
        if not query.exec():
            raise Exception(
                f"Error fetching real estate product with id [{record_id}]: {query.lastError().text()}"
            )
        if query.next():
            record = query.record()
            data = {}
            for i in range(record.count()):
                field_name = record.fieldName(i)
                field_value = record.value(i)
                data[field_name] = field_value
            data.setdefault(
                "image_paths", get_images_in_directory(data.get("image_dir"))
            )
            return data
        return {}

    @staticmethod
    def read_all():
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(
            f"""
                SELECT
                    tp.id,
                    tp.pid,
                    tp.street,
                    tp.area,
                    tp.structure,
                    tp.function,
                    tp.description,
                    tp.price,
                    tp.image_dir,
                    tp.updated_at,
                    ts_status.label_vi as status,
                    ts_province.label_vi AS province,
                    ts_district.label_vi AS district,
                    ts_ward.label_vi AS ward,
                    ts_option.label_vi AS option,
                    ts_category.label_vi AS category,
                    ts_building_line.label_vi AS building_line,
                    ts_furniture.label_vi AS furniture,
                    ts_legal.label_vi AS legal
                FROM {constants.RE_PRODUCT_TABLE} tp
                JOIN {constants.RE_SETTING_STATUS_TABLE} ts_status ON tp.status_id = ts_status.id
                LEFT JOIN {constants.RE_SETTING_PROVINCES_TABLE} ts_province ON tp.province_id = ts_province.id
                LEFT JOIN {constants.RE_SETTING_DISTRICTS_TABLE} ts_district ON tp.district_id = ts_district.id
                LEFT JOIN {constants.RE_SETTING_WARDS_TABLE} ts_ward ON tp.ward_id = ts_ward.id
                LEFT JOIN {constants.RE_SETTING_OPTIONS_TABLE} ts_option ON tp.option_id = ts_option.id
                LEFT JOIN {constants.RE_SETTING_CATEGORIES_TABLE} ts_category ON tp.category_id = ts_category.id
                LEFT JOIN {constants.RE_SETTING_BUILDING_LINES_TABLE} ts_building_line ON tp.building_line_id = ts_building_line.id
                LEFT JOIN {constants.RE_SETTING_FURNITURES_TABLE} ts_furniture ON tp.furniture_id = ts_furniture.id
                LEFT JOIN {constants.RE_SETTING_LEGALS_TABLE} ts_legal ON tp.legal_id = ts_legal.id
                """
        )
        if not query.exec():
            raise Exception(
                f"Error fetching all real estate products: {query.lastError().text()}"
            )

        results = []
        while query.next():
            record = query.record()
            data = {}
            for i in range(record.count()):
                field_name = record.fieldName(i)
                field_value = query.value(i)
                data[field_name] = field_value
            data.setdefault(
                "image_paths", get_images_in_directory(data.get("image_dir"))
            )
            results.append(data)

        return results

    @staticmethod
    def update(record_id, data):
        db = QSqlDatabase.database()
        if not db.transaction():
            raise Exception("Failed to start transaction.")
        try:
            if not validate_foreign_keys(data):
                db.rollback()
                return False
            query = QSqlQuery()
            sql_parts = []
            columns = REProductService.get_columns()
            for key in columns:
                if key != "id" and key != "created_at":
                    sql_parts.append(f"{key}=:{key}")
            sql = f"""
            UPDATE {constants.RE_PRODUCT_TABLE}
            SET {", ".join(sql_parts)}
            WHERE id=:id
            """
            query.prepare(sql)
            now = datetime.datetime.now()
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            data["updated_at"] = formatted_time
            for key in columns:
                if key != "id":
                    query.bindValue(f":{key}", data.get(key))
            query.bindValue(":id", record_id)
            if not query.exec():
                db.rollback()
                raise Exception(
                    f"Error updating record with id [{record_id}]: {query.lastError().text()}"
                )

            if not db.commit():
                db.rollback()
                raise Exception("Failed to commit transaction.")
            return True

        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def delete(record_id):
        db = QSqlDatabase.database()
        if not db.transaction():
            raise Exception("Failed to start transaction.")
        try:
            product_data = REProductService.read(record_id)
            image_dir = product_data.get("image_dir")
            query = QSqlQuery()
            query.prepare(
                f"""
                DELETE FROM {constants.RE_PRODUCT_TABLE}
                WHERE id=:id
            """
            )
            query.bindValue(":id", record_id)

            if not query.exec():
                db.rollback()
                raise Exception(
                    f"Error deleting record with id [{record_id}]: {query.lastError().text()}"
                )

            if image_dir and os.path.exists(image_dir):
                try:
                    shutil.rmtree(image_dir)
                    # print(
                    #     f"Deleted associated image directory for id [{record_id}]: {image_dir}")
                except Exception as e:
                    print(
                        f"Error deleting image directory {image_dir} for id [{record_id}]: {e}"
                    )

            if not db.commit():
                db.rollback()
                raise Exception("Failed to commit transaction.")
            return True

        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def check_unique_pid(pid: int) -> bool:
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(
            f"""
            SELECT pid FROM {constants.RE_PRODUCT_TABLE} WHERE pid = :pid
            """
        )
        query.bindValue(":pid", pid)
        if not query.exec():
            raise Exception(
                f"Error checking unique pid [{pid}]: {query.lastError().text()}"
            )
        if query.next():
            return True
        return False

    @staticmethod
    def get_images_in_directory(id):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(
            f"SELECT image_dir FROM {constants.RE_PRODUCT_TABLE} WHERE id = :id"
        )
        query.bindValue(":id", id)
        if not query.exec():
            print(
                f"Error executing query to fetch image directory for product ID [{id}]: {query.lastError().text()}")
            raise Exception(
                f"Error executing query to fetch image directory for product ID [{id}]: {query.lastError().text()}"
            )

        if query.next():
            image_dir = query.value(0)
            if not os.path.exists(image_dir):
                return []
            images = []
            for file in os.listdir(image_dir):
                if file.endswith((".png", ".jpg", ".jpeg")):
                    images.append(os.path.abspath(
                        os.path.join(image_dir, file)))
            return images
        else:
            print("Invalid 'image_dir'")
            return []

    @staticmethod
    def get_columns() -> list[str]:
        database = QSqlDatabase.database()
        if not database.isValid() or not database.isOpen():
            raise Exception("Database is not open or valid.")
        table_record = database.record(constants.RE_PRODUCT_TABLE)
        if table_record.isEmpty():
            raise Exception(
                f"Table {constants.RE_PRODUCT_TABLE} does not exist.")
        columns = []
        for i in range(table_record.count()):
            field_name = table_record.fieldName(i)
            columns.append(field_name)
        return columns


class RESettingService:
    @staticmethod
    def create(table_name, data):
        db = QSqlDatabase.database()
        print(db.transaction())
        if not db.transaction():
            raise Exception("Failed to start transaction.")
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join([f":{key}" for key in data.keys()])
            query = QSqlQuery()
            sql = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({placeholders})
            """
            query.prepare(sql)
            print(data)
            print(sql)
            # now = datetime.datetime.now()
            # formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            # data.setdefault("updated_at", formatted_time)
            for key, value in data.items():
                query.bindValue(f":{key}", value)
            if not query.exec():
                db.rollback()
                raise Exception(
                    f"Error inserting into {table_name}: {query.lastError().text()}"
                )
            if not db.commit():
                db.rollback()
                raise Exception("Failed to commit transaction.")
            return True
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def read(table_name, record_id):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(
            f"""
            SELECT * FROM {table_name}
            WHERE id=:id
        """
        )
        query.bindValue(":id", record_id)
        if not query.exec():
            raise Exception(
                f"Error fetching from {table_name} with id [{record_id}]: {query.lastError().text()}"
            )
        if query.next():
            record = query.record()
            data = {}
            for i in range(record.count()):
                field_name = record.fieldName(i)
                field_value = query.value(i)
                data[field_name] = field_value
            return data
        return {}

    @staticmethod
    def read_all(table_name):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(
            f"""
            SELECT * FROM {table_name}
        """
        )
        if not query.exec():
            raise Exception(
                f"Error fetching all from {table_name}: {query.lastError().text()}"
            )
        results = []
        while query.next():
            record = query.record()
            data = {}
            for i in range(record.count()):
                field_name = record.fieldName(i)
                field_value = query.value(i)
                data[field_name] = field_value
            results.append(data)
        return results

    @staticmethod
    def update(table_name, record_id, data):
        db = QSqlDatabase.database()
        if not db.transaction():
            raise Exception("Failed to start transaction.")
        try:
            sql_parts = []
            for key, value in data.items():
                if key != "id":
                    sql_parts.append(f"{key}=:{key}")
            sql = f"""
                UPDATE {table_name}
                SET {", ".join(sql_parts)}
                WHERE id=:id
            """
            query = QSqlQuery()
            query.prepare(sql)
            data["id"] = record_id  # Ensure ID is in data for binding
            for key, value in data.items():
                query.bindValue(f":{key}", value)
            if not query.exec():
                db.rollback()
                raise Exception(
                    f"Error updating {table_name} with id [{record_id}]: {query.lastError().text()}"
                )
            if not db.commit():
                db.rollback()
                raise Exception("Failed to commit transaction.")
            return True
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def delete(table_name, record_id):
        db = QSqlDatabase.database()
        if not db.transaction():
            raise Exception("Failed to start transaction.")
        try:
            query = QSqlQuery()
            query.prepare(
                f"""
                DELETE FROM {table_name}
                WHERE id=:id
            """
            )
            query.bindValue(":id", record_id)
            if not query.exec():
                db.rollback()
                raise Exception(
                    f"Error deleting from {table_name} with id [{record_id}]: {query.lastError().text()}"
                )
            if not db.commit():
                db.rollback()
                raise Exception("Failed to commit transaction.")
            return True
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def check_exist_id(table_name, record_id):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(
            f"""
            SELECT COUNT(*) FROM {table_name}
            WHERE id=:id
        """
        )
        query.bindValue(":id", record_id)
        if not query.exec():
            raise Exception(
                f"Error checking existence in {table_name} for id [{record_id}]: {query.lastError().text()}"
            )
        if query.next():
            count = query.value(0)
            return count > 0
        return False

    @staticmethod
    def get_id_by_value(table_name, value):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(
            f"""
            SELECT id FROM {table_name}
            WHERE value=:value
        """
        )
        query.bindValue(":value", value)
        if not query.exec():
            raise Exception(
                f"Error fetching from {table_name} with value [{value}]: {query.lastError().text()}"
            )
        if query.next():
            return query.value(0)
        return None


# class RETemplateService:
#     @staticmethod
#     def read(table_name, id):
#         db = QSqlDatabase.database()
#         query = QSqlQuery(db)
#         query.prepare(f"SELECT * FROM {table_name} WHERE id = :id")
#         query.bindValue(":id", id)
#         if not query.exec():
#             print(
#                 f"Error reading from {table_name} with id [{id}]: {query.lastError().text()}"
#             )
#             return None
#         if query.next():
#             row = {}
#             for i in range(query.record().count()):
#                 row[query.record().fieldName(i)] = query.value(i)
#             return row
#         return None

#     @staticmethod
#     def read_all(table_name):
#         db = QSqlDatabase.database()
#         query = QSqlQuery(db)
#         query.prepare(f"SELECT * FROM {table_name}")
#         if not query.exec():
#             print(
#                 f"Error reading all from {table_name}: {query.lastError().text()}")
#             return []
#         results = []
#         while query.next():
#             row = {}
#             for i in range(query.record().count()):
#                 row[query.record().fieldName(i)] = query.value(i)
#             results.append(row)
#         return results

#     @staticmethod
#     def create(table_name, data):
#         db = QSqlDatabase.database()
#         if not db.transaction():
#             raise Exception("Failed to start transaction.")
#         columns = ", ".join(data.keys())
#         placeholders = ", ".join([f":{key}" for key in data.keys()])
#         sql = f"""
# INSERT INTO {table_name} ({columns})
# VALUES ({placeholders})
#                 """
#         try:
#             query = QSqlQuery(db)
#             query.prepare(sql)
#             for key, value in data.items():
#                 query.bindValue(f":{key}", value)
#             if not query.exec():
#                 db.rollback()
#                 print(
#                     f"Error inserting into {table_name}: {query.lastError().text()}")
#                 return False
#             if not db.commit():
#                 print("Failed to commit transaction.")
#                 return False
#             return True
#         except Exception as e:
#             db.rollback()
#             print("ERROR: ", e)
#             return False

#     @staticmethod
#     def update(table_name, id, data):
#         db = QSqlDatabase.database()
#         if not db.transaction():
#             raise Exception("Failed to start transaction.")
#         set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
#         try:
#             query = QSqlQuery(db)
#             query.prepare(
#                 f"""
# UPDATE {table_name}
# SET {set_clause}, updated_at = :updated_at
# WHERE id = :id
#                 """
#             )
#             now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             query.bindValue(":updated_at", now)
#             query.bindValue(":id", id)
#             for key, value in data.items():
#                 query.bindValue(f":{key}", value)
#             if not query.exec():
#                 db.rollback()
#                 print(
#                     f"Error updating {table_name} with id [{id}]: {query.lastError().text()}"
#                 )
#                 return False
#             if not db.commit():
#                 print("Failed to commit transaction.")
#                 return False
#             return True
#         except Exception as e:
#             db.rollback()
#             print("ERROR: ", e)
#             return False

#     @staticmethod
#     def delete(table_name, id):
#         db = QSqlDatabase.database()
#         if not db.transaction():
#             raise Exception("Failed to start transaction.")
#         try:
#             query = QSqlQuery(db)
#             query.prepare(f"DELETE FROM {table_name} WHERE id = :id")
#             query.bindValue(":id", id)
#             if not query.exec():
#                 db.rollback()
#                 print(
#                     f"Error deleting from {table_name} with id [{id}]: {query.lastError().text()}"
#                 )
#                 return False
#             if not db.commit():
#                 print("Failed to commit transaction.")
#                 return False
#             return True
#         except Exception as e:
#             db.rollback()
#             print("ERROR: ", e)
#             return False

#     @staticmethod
#     def is_tid_existed(table_name, tid):
#         db = QSqlDatabase.database()
#         query = QSqlQuery(db)
#         query.prepare(
#             f"""
#             SELECT COUNT(*) FROM {table_name}
#             WHERE tid = :tid
#         """
#         )
#         query.bindValue(":tid", tid)
#         if not query.exec():
#             raise Exception(
#                 f"Error checking existence in {table_name} for tid [{tid}]: {query.lastError().text()}"
#             )
#         if query.next():
#             return query.value(0) > 0  # Returns True if record exists
#         return False

#     @staticmethod
#     def get_columns(table_name):
#         db = QSqlDatabase.database()
#         if not db.isValid() or not db.isOpen():
#             print("Database is not open or valid.")
#             return False
#         record = db.record(table_name)
#         if record.isEmpty():
#             print((f"Table {table_name} does not exist."))
#             return False
#         columns = []
#         for i in range(record.count()):
#             field_name = record.fieldName(i)
#             columns.append(field_name)
#         return columns

#     @staticmethod
#     def get_ids(table_name, option_id=-1):
#         db = QSqlDatabase.database()
#         if not db.isValid() or not db.isOpen():
#             print("Database is not open or valid.")
#             return False
#         query = QSqlQuery(db)
#         if option_id == -1:
#             sql = f"SELECT id FROM {table_name}"
#             query.prepare(sql)
#         else:
#             sql = f"SELECT id FROM {table_name} WHERE option_id=:option_id"
#             query.prepare(sql)
#             query.bindValue(":option_id", option_id)
#         ids = []
#         if query.exec():
#             while query.next():
#                 ids.append(query.value(0))
#         else:
#             print(
#                 f"Error querying ID from '{table_name}': {query.lastError().text()}")
#             return None
#         return ids

#     # @staticmethod
#     # def get_ids(table_name, option):
#     #     db = QSqlDatabase.database()
#     #     if not db.isValid() or not db.isOpen():
#     #         print("Database is not open or valid.")
#     #         return False
#     #     query = QSqlQuery(db)
#     #     sql = f"SELECT id FROM {table_name} WHERE option="
#     #     ids = []
#     #     if query.exec(sql):
#     #         while query.next():
#     #             ids.append(query.value(0))
#     #     else:
#     #         print(
#     #             f"Error querying ID from '{table_name}': {query.lastError().text()}")
#     #         return None
#     #     return ids


class RETemplateService:
    @staticmethod
    def read(table_name, id):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(f"""
SELECT 
                      main.id AS id,
                      main.tid AS tid,
                      options.id AS option_id,
                      options.label_vi AS option_label_vi,
                      options.label_en AS option_label_en,
                      options.value AS option_value,
                      main.updated_at as updated,
FROM {table_name} main
JOIN {constants.RE_SETTING_OPTIONS_TABLE} options ON main.option_id = options.id
WHERE main.id = :id
                      """)
        query.bindValue(":id", id)
        if not query.exec():
            print(
                f"Error reading from {table_name} with id [{id}]: {query.lastError().text()}"
            )
            return None
        if query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            return row
        return None

    @staticmethod
    def read_all(table_name, id):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(f"""
SELECT 
                      main.id AS id,
                      main.tid AS tid,
                      options.id AS option_id,
                      options.label_vi AS option_label_vi,
                      options.label_en AS option_label_en,
                      options.value AS option_value,
                      main.updated_at as updated,
FROM {table_name} main
JOIN {constants.RE_SETTING_OPTIONS_TABLE} options ON main.option_id = options.id
                      """)
        if not query.exec():
            print(
                f"Error reading all from {table_name}: {query.lastError().text()}")
            return []
        results = []
        while query.next():
            row = {}
            for i in range(query.record().count()):
                row[query.record().fieldName(i)] = query.value(i)
            results.append(row)
        return results

    @staticmethod
    def create(table_name, payload):
        db = QSqlDatabase.database()
        if not db.transaction():
            raise Exception("Failed to start transaction.")
        sql = f"""
INSERT INTO {table_name} (id, tid, option_id, value)
VALUES (id = :id, tid = :tid, option_id = :option_id, value = :value)
"""
        try:
            query = QSqlQuery(db)
            query.prepare(sql)
            for key, value in payload.items():
                query.bindValue(f":{key}", value)
            if not query.exec():
                db.rollback()
                print(
                    f"Error inserting into {table_name}: {query.lastError().text()}")
                return False
            if not db.commit():
                print("Failed to commit transaction.")
                return False
            return True
        except Exception as e:
            db.rollback()
            print("ERROR: ", e)
            return False

    @staticmethod
    def update(table_name, payload):
        db = QSqlDatabase.database()
        if not db.transaction():
            raise Exception("Failed to start transaction.")
        set_clause = ", ".join([f"{key} = :{key}" for key in payload.keys()])
        try:
            query = QSqlQuery(db)
            query.prepare(
                f"""
UPDATE {table_name}
SET {set_clause}, updated_at = (strftime('%Y-%m-%d %H:%M:%S', 'now'))
WHERE id = :id
                """
            )
            query.bindValue(":id", id)
            for key, value in payload.items():
                query.bindValue(f":{key}", value)
            if not query.exec():
                db.rollback()
                print(
                    f"Error updating {table_name} with id [{id}]: {query.lastError().text()}"
                )
                return False
            if not db.commit():
                print("Failed to commit transaction.")
                return False
            return True
        except Exception as e:
            db.rollback()
            print("ERROR: ", e)
            return False

    @staticmethod
    def delete(table_name, id):
        db = QSqlDatabase.database()
        if not db.transaction():
            raise Exception("Failed to start transaction.")
        try:
            query = QSqlQuery(db)
            query.prepare(f"DELETE FROM {table_name} WHERE id = :id")
            query.bindValue(":id", id)
            if not query.exec():
                db.rollback()
                print(
                    f"Error deleting from {table_name} with id [{id}]: {query.lastError().text()}"
                )
                return False
            if not db.commit():
                print("Failed to commit transaction.")
                return False
            return True
        except Exception as e:
            db.rollback()
            print("ERROR: ", e)
            return False

    @staticmethod
    def is_tid_existed(table_name, tid):
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.prepare(
            f"""
            SELECT COUNT(*) FROM {table_name}
            WHERE tid = :tid
        """
        )
        query.bindValue(":tid", tid)
        if not query.exec():
            raise Exception(
                f"Error checking existence in {table_name} for tid [{tid}]: {query.lastError().text()}"
            )
        if query.next():
            return query.value(0) > 0  # Returns True if record exists
        return False

    @staticmethod
    def get_columns(table_name):
        db = QSqlDatabase.database()
        if not db.isValid() or not db.isOpen():
            print("Database is not open or valid.")
            return False
        record = db.record(table_name)
        if record.isEmpty():
            print((f"Table {table_name} does not exist."))
            return False
        columns = []
        for i in range(record.count()):
            field_name = record.fieldName(i)
            columns.append(field_name)
        return columns

    @staticmethod
    def get_ids(table_name, option_id=-1):
        db = QSqlDatabase.database()
        if not db.isValid() or not db.isOpen():
            print("Database is not open or valid.")
            return False
        query = QSqlQuery(db)
        if option_id == -1:
            sql = f"SELECT id FROM {table_name}"
            query.prepare(sql)
        else:
            sql = f"SELECT id FROM {table_name} WHERE option_id=:option_id"
            query.prepare(sql)
            query.bindValue(":option_id", option_id)
        ids = []
        if query.exec():
            while query.next():
                ids.append(query.value(0))
        else:
            print(
                f"Error querying ID from '{table_name}': {query.lastError().text()}")
            return None
        return ids
