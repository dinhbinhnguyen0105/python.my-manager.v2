# src/database/db_user.py
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from src import constants

SQL_CREATE_USER_TABLE = f"""
CREATE TABLE IF NOT EXISTS {constants.TABLE_USER} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status INTEGER,
    uid TEXT UNIQUE,
    username TEXT,
    password TEXT,
    two_fa TEXT,
    email TEXT,
    email_password TEXT,
    phone_number TEXT,
    note TEXT,
    type TEXT,
    user_group INTEGER,
    mobile_ua TEXT,
    desktop_ua TEXT,
    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
SQL_CREATE_LISTED_PRODUCT_TABLE = f"""
CREATE TABLE IF NOT EXISTS {constants.TABLE_LISTED_PRODUCT} (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES {constants.TABLE_USER}(id),
    pid TEXT,
    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
SQL_CREATE_ACTION_TABLE = f"""
CREATE TABLE IF NOT EXISTS {constants.TABLE_ROBOT_ACTION} (
    id INTEGER PRIMARY KEY,
    uid INTEGER REFERENCES {constants.TABLE_USER}(uid),
    action_name TEXT,
    action_payload TEXT,
    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
SQL_CREATE_USER_SETTING_UDD_TABLE = f"""
CREATE TABLE IF NOT EXISTS {constants.TABLE_USER_SETTING_UDD} (
id INTEGER PRIMARY KEY AUTOINCREMENT,
value TEXT UNIQUE NOT NULL,
is_selected INTEGER,
updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""
SQL_CREATE_USER_SETTING_PROXY_TABLE = f"""
CREATE TABLE IF NOT EXISTS {constants.TABLE_USER_SETTING_PROXY} (
id INTEGER PRIMARY KEY AUTOINCREMENT,
value TEXT UNIQUE NOT NULL,
updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""


def initialize_db_user():
    if QSqlDatabase.contains(constants.CONNECTION_DB_USER):
        db = QSqlDatabase.database(constants.CONNECTION_DB_USER)
    else:
        db = QSqlDatabase.addDatabase("QSQLITE", constants.CONNECTION_DB_USER)
    db.setDatabaseName(constants.PATH_DB_USER)
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
                SQL_CREATE_LISTED_PRODUCT_TABLE,
                SQL_CREATE_USER_TABLE,
                SQL_CREATE_USER_SETTING_UDD_TABLE,
                SQL_CREATE_USER_SETTING_PROXY_TABLE,
                SQL_CREATE_ACTION_TABLE,
            ]:
                if not query.exec(sql):
                    error_msg = f"[initialize_db_user] An error occurred while creating table: {query.lastError().text()}"
                    db.rollback()
                    raise Exception(error_msg)
            if not db.commit():
                error_msg = f"[initialize_db_user] Cannot commit transaction: {db.lastError().text()}"
                db.rollback()
                raise Exception(error_msg)
            return True
        else:
            return False
    except Exception as e:
        raise e
