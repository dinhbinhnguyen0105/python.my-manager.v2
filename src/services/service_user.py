# service_product.py
from typing import Optional, List
from src.my_types import REProductType, RETemplateType, MiscProductType
from src import constants
from src.services.base_service import BaseService
from src.models.model_product import ProductMiscModel, ProductREModel, TemplateREModel

from src.my_types import UserType


class UserService(BaseService):
    DATA_TYPE = UserType

    def __init__(self, model):
        super().__init__(model)

    def create(self, payload: UserType) -> bool:
        return super().create(payload)

    def read(self, record_id: int) -> Optional[UserType]:
        return super().read(record_id)

    def read_all(self) -> List[UserType]:
        return super().read_all()

    def update(self, record_id: int, payload: UserType) -> bool:
        return super().update(record_id, payload)

    def delete(self, record_id: int) -> bool:
        return super().delete(record_id)

    def delete_multiple(self, record_ids):
        return super().delete_multiple(record_ids)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from src.database.db_user import initialize_db_user
    from src.database.db_product import initialize_db_product
    from src.models.model_user import UserModel
    from src.models.model_product import ProductREModel
    from src.my_types import UserType

    app = QApplication([])
    if initialize_db_user() and initialize_db_product():
        user_model = UserModel()
        user_service = UserService(user_model)

        # user_service.create(
        #     UserType(
        #         id=None,
        #         uid="uid_test_user_03",
        #         username="username_test_user_03",
        #         password="password_test_user_03",
        #         two_fa="two_fa_test_user_03",
        #         email="email_test_user_03",
        #         email_password="email_password_test_user_03",
        #         phone_number="phone_number_test_user_03",
        #         note="note_test_user_03",
        #         type="type_test_user_03",
        #         user_group=1,
        #         mobile_ua="mobile_ua_test_user_03",
        #         desktop_ua="desktop_ua_test_user_03",
        #         status=1,
        #         created_at=None,
        #         updated_at=None,
        #     )
        # )
        print(
            user_service.update(
                4,
                UserType(
                    id=None,
                    uid="uid_test_user_00",
                    username="username_test_user_00",
                    password="password_test_user_00",
                    two_fa="two_fa_test_user_00",
                    email="email_test_user_00",
                    email_password="email_password_test_user_00",
                    phone_number="phone_number_test_user_00",
                    note="note_test_user_00",
                    type="type_test_user_00",
                    user_group=1,
                    mobile_ua="mobile_ua_test_user_00",
                    desktop_ua="desktop_ua_test_user_00",
                    status=1,
                    created_at=None,
                    updated_at=None,
                ),
            )
        )

        # user_service.delete_multiple([2, 3])

        _all = user_service.read_all()
        for user in _all:
            print(user)
