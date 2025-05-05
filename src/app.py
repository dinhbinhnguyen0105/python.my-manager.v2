# src/app.py

from src.database.db_user import initialize_db_user
from src.database.db_product import initialize_db_product
from src.models.model_product import ProductMiscModel, ProductREModel, TemplateREModel
from src.models.model_user import UserModel, ListedProductModel
from src.controllers.controller_user import UserController


class Application:
    def __init__(self):
        pass
