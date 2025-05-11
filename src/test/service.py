from PyQt6.QtWidgets import QApplication

from src.my_types import REProductType, UserType
from src.database.db_product import initialize_db_product
from src.database.db_user import initialize_db_user
from src.models.base_model import BaseModel
from src.models.model_product import MiscProductModel, REProductModel, RETemplateModel
from src.models.model_user import UserModel, ListedProductModel
from src.services.service_product import (
    ProductMiscService,
    ProductREService,
    TemplateREService,
)
from src.services.service_user import UserService, ListedProductService

if __name__ == "__main__":
    app = QApplication([])
    if initialize_db_user() and initialize_db_product():
        # payload = [
        #     REProductType(
        #         id=None,
        #         pid="re_product_01",
        #         status="1",
        #         action="1",
        #         province="1",
        #         district="1",
        #         ward="1",
        #         street="re_product_01",
        #         category="1",
        #         area="1.1",
        #         price="1.1",
        #         legal="1",
        #         structure="2",
        #         function="re_product_01",
        #         building_line="1",
        #         furniture="re_product_01",
        #         description="re_product_01",
        #         created_at=None,
        #         updated_at=None,
        #     ),
        #     REProductType(
        #         id=None,
        #         pid="re_product_02",
        #         status="1",
        #         action="1",
        #         province="1",
        #         district="1",
        #         ward="1",
        #         street="re_product_02",
        #         category="1",
        #         area="1.1",
        #         price="1.1",
        #         legal="1",
        #         structure="2",
        #         function="re_product_02",
        #         building_line="1",
        #         furniture="re_product_02",
        #         description="re_product_02",
        #         created_at=None,
        #         updated_at=None,
        #     ),
        #     REProductType(
        #         id=None,
        #         pid="re_product_03",
        #         status="1",
        #         action="1",
        #         province="1",
        #         district="1",
        #         ward="1",
        #         street="re_product_03",
        #         category="1",
        #         area="1.1",
        #         price="1.1",
        #         legal="1",
        #         structure="2",
        #         function="re_product_03",
        #         building_line="1",
        #         furniture="re_product_03",
        #         description="re_product_03",
        #         created_at=None,
        #         updated_at=None,
        #     ),
        #     REProductType(
        #         id=None,
        #         pid="re_product_04",
        #         status="1",
        #         action="1",
        #         province="1",
        #         district="1",
        #         ward="1",
        #         street="re_product_04",
        #         category="1",
        #         area="1.1",
        #         price="1.1",
        #         legal="1",
        #         structure="2",
        #         function="re_product_04",
        #         building_line="1",
        #         furniture="re_product_04",
        #         description="re_product_04",
        #         created_at=None,
        #         updated_at=None,
        #     ),
        #     REProductType(
        #         id=None,
        #         pid="re_product_05",
        #         status="1",
        #         action="1",
        #         province="1",
        #         district="1",
        #         ward="1",
        #         street="re_product_05",
        #         category="1",
        #         area="1.1",
        #         price="1.1",
        #         legal="1",
        #         structure="2",
        #         function="re_product_05",
        #         building_line="1",
        #         furniture="re_product_05",
        #         description="re_product_05",
        #         created_at=None,
        #         updated_at=None,
        #     ),
        #     REProductType(
        #         id=None,
        #         pid="re_product_06",
        #         status="1",
        #         action="1",
        #         province="1",
        #         district="1",
        #         ward="1",
        #         street="re_product_06",
        #         category="1",
        #         area="1.1",
        #         price="1.1",
        #         legal="1",
        #         structure="2",
        #         function="re_product_06",
        #         building_line="1",
        #         furniture="re_product_06",
        #         description="re_product_06",
        #         created_at=None,
        #         updated_at=None,
        #     ),
        #     REProductType(
        #         id=None,
        #         pid="re_product_07",
        #         status="1",
        #         action="1",
        #         province="1",
        #         district="1",
        #         ward="1",
        #         street="re_product_07",
        #         category="1",
        #         area="1.1",
        #         price="1.1",
        #         legal="1",
        #         structure="2",
        #         function="re_product_07",
        #         building_line="1",
        #         furniture="re_product_07",
        #         description="re_product_07",
        #         created_at=None,
        #         updated_at=None,
        #     ),
        #     REProductType(
        #         id=None,
        #         pid="re_product_08",
        #         status="1",
        #         action="1",
        #         province="1",
        #         district="1",
        #         ward="1",
        #         street="re_product_08",
        #         category="1",
        #         area="1.1",
        #         price="1.1",
        #         legal="1",
        #         structure="2",
        #         function="re_product_08",
        #         building_line="1",
        #         furniture="re_product_08",
        #         description="re_product_08",
        #         created_at=None,
        #         updated_at=None,
        #     ),
        # ]
        # product_re_model = REProductModel()
        # product_re_service = ProductREService(product_re_model)
        # # product_re_service.create(payload[6])
        # product_re_service.update(13, payload[0])
        # # product_re_service.delete_multiple([6, 7, 8, 9, 10, 11, 12])
        # # product_re_service.import_data(payload)
        # # product_re_service.read_all()
        # for p in product_re_service.read_all():
        #     print(p)
        #     print()
        user_model = UserModel()
        user_service = UserService(user_model)
        payload = [
            UserType(
                id=None,
                status=1,
                uid="user_01",
                username="user_01",
                password="user_01",
                two_fa="user_01",
                email="user_01",
                email_password="user_01",
                phone_number="user_01",
                note="user_01",
                type="user_01",
                user_group="user_01",
                mobile_ua="user_01",
                desktop_ua="user_01",
                created_at=None,
                updated_at=None,
            )
        ]
        user_service.create(payload=payload[0])
        for u in user_service.read_all():
            print(u)
            print()

    else:
        print("Failed to init db.")
