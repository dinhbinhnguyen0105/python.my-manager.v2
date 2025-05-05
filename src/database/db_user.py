# db_user.py
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
    user_id  INTEGER PRIMARY KEY REFERENCES {constants.TABLE_USER}(id),
    pid TEXT,
    created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
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
            for sql in [SQL_CREATE_LISTED_PRODUCT_TABLE, SQL_CREATE_USER_TABLE]:
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
