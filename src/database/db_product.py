# db_product.py
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from src import constants

SQL_CREATE_RE_PRODUCT = f"""
CREATE TABLE IF NOT EXISTS {constants.TABLE_RE_PRODUCT} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pid TEXT UNIQUE,
    status INTEGER,
    action INTEGER,
    province INTEGER,
    district INTEGER,
    ward INTEGER,
    street TEXT,
    category INTEGER,
    area REAL,
    price REAL,
    legal INTEGER,
    structure REAL,
    function TEXT,
    building_line INTEGER,
    furniture TEXT,
    description TEXT,
    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
SQL_CREATE_MISC_PRODUCT = f"""
CREATE TABLE IF NOT EXISTS {constants.TABLE_MISC_PRODUCT} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pid TEXT UNIQUE,
    category INTEGER,
    title TEXT,
    description TEXT,
    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
SQL_CREATE_RE_TEMPLATE = f"""
CREATE TABLE IF NOT EXISTS {constants.TABLE_RE_TEMPLATE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tid TEXT UNIQUE,
    action INTEGER,
    part INTEGER,
    content TEXT,
    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""


def initialize_db_product():
    if QSqlDatabase.contains(constants.CONNECTION_DB_PRODUCT):
        db = QSqlDatabase.database(constants.CONNECTION_DB_PRODUCT)
    else:
        db = QSqlDatabase.addDatabase("QSQLITE", constants.CONNECTION_DB_PRODUCT)
    db.setDatabaseName(constants.PATH_DB_PRODUCT)
    if not db.open():
        raise Exception(
            f"An error occurred while opening the database: {db.lastError().text()}"
        )
    query = QSqlQuery(db)
    query.exec("PRAGMA foreign_keys = ON;")
    query.exec("PRAGMA journal_mode = WAL;")

    try:
        if db.transaction():
            for sql in [
                SQL_CREATE_RE_PRODUCT,
                SQL_CREATE_RE_TEMPLATE,
                SQL_CREATE_MISC_PRODUCT,
            ]:
                if not query.exec(sql):
                    error_msg = f"An error occurred while creating table: {query.lastError().text()}"
                    db.rollback()
                    raise Exception(error_msg)
            if not db.commit():
                error_msg = f"Cannot commit transaction: {db.lastError().text()}"
                db.rollback()
                raise Exception(error_msg)
            return True
        else:
            return False
    except Exception as e:
        raise e
