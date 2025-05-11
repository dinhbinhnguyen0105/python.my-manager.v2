# src/services/service_product.py
from typing import Optional, List
from src.services.base_service import BaseService
from src.models.model_product import MiscProductModel, REProductModel, RETemplateModel
from src.my_types import MiscProductType, REProductType, RETemplateType


class REProductService(BaseService):
    DATA_TYPE = REProductType

    def __init__(self, model: REProductModel):
        if not isinstance(model, REProductModel):
            raise TypeError(
                "model must be an instance of REProductModel or its subclass."
            )
        super().__init__(model)

    def create(self, payload: REProductType) -> bool:
        return super().create(payload)

    def read(self, record_id: int) -> Optional[REProductType]:
        return super().read(record_id)

    def read_all(self) -> List[REProductType]:
        return super().read_all()

    def update(self, record_id: int, payload: REProductType) -> bool:
        return super().update(record_id, payload)

    def delete(self, record_id: int) -> bool:
        return super().delete(record_id)

    def delete_multiple(self, record_ids: List[int]):
        return super().delete_multiple(record_ids)

    def import_data(self, payload: List[REProductType]):
        return super().import_data(payload)

    def find_by_pid(self, pid: str) -> Optional[REProductType]:
        return self._find_by_model_index(find_method_name="find_row_by_pid", value=pid)

    def toggle_status(self, product_id: str) -> bool:
        """
        Toggles the status of a product between active (1) and inactive (0).

        Args:
            product_id (str): The unique identifier of the product whose status is to be toggled.

        Returns:
            bool: True if the status was successfully toggled and updated in the database,
                  False otherwise.
        """
        product = self.find_by_pid(product_id)
        if product is None:
            print(
                f"[{self.__class__.__name__}.toggle_status] Product with ID '{product_id}' not found."
            )
            return False

        current_status = product.status
        if current_status == 0:
            new_status = 1
        elif current_status == 1:
            new_status = 0
        else:
            print(
                f"[{self.__class__.__name__}.toggle_status] Unexpected status value for product ID '{product_id}': {current_status}. Cannot toggle."
            )
            return False

        product.status = new_status
        update_success = self.update(product.id, product)
        if update_success:
            print(
                f"[{self.__class__.__name__}.toggle_status] Successfully toggled status for product ID '{product_id}' to {new_status}."
            )
            return True
        else:
            print(
                f"[{self.__class__.__name__}.toggle_status] Failed to update status for product ID '{product_id}'."
            )
            return False


class MiscProductService(BaseService):
    DATA_TYPE = MiscProductType

    def __init__(self, model: MiscProductModel):
        if not isinstance(model, MiscProductModel):
            raise TypeError(
                "model must be an instance of MiscProductModel or its subclass."
            )
        super().__init__(model)

    def create(self, payload: MiscProductModel) -> bool:
        return super().create(payload)

    def read(self, record_id: int) -> Optional[MiscProductModel]:
        return super().read(record_id)

    def read_all(self) -> List[MiscProductModel]:
        return super().read_all()

    def update(self, record_id: int, payload: MiscProductModel) -> bool:
        return super().update(record_id, payload)

    def delete(self, record_id: int) -> bool:
        return super().delete(record_id)

    def delete_multiple(self, record_ids: List[int]):
        return super().delete_multiple(record_ids)

    def import_data(self, payload: List[MiscProductModel]):
        return super().import_data(payload)

    def find_by_pid(self, pid: str) -> Optional[MiscProductModel]:
        return self._find_by_model_index(find_method_name="find_row_by_pid", value=pid)

    def toggle_status(self, product_id: str) -> bool:
        """
        Toggles the status of a miscellaneous product between active (1) and inactive (0).

        Args:
            product_id (str): The unique identifier of the product whose status is to be toggled.

        Returns:
            bool: True if the status was successfully toggled and updated in the database,
                  False otherwise.
        """
        product = self.find_by_pid(product_id)
        if product is None:
            print(
                f"[{self.__class__.__name__}.toggle_status] Product with ID '{product_id}' not found."
            )
            return False

        current_status = product.status
        if current_status == 0:
            new_status = 1
        elif current_status == 1:
            new_status = 0
        else:
            print(
                f"[{self.__class__.__name__}.toggle_status] Unexpected status value for product ID '{product_id}': {current_status}. Cannot toggle."
            )
            return False

        product.status = new_status
        update_success = self.update(product.id, product)
        if update_success:
            print(
                f"[{self.__class__.__name__}.toggle_status] Successfully toggled status for product ID '{product_id}' to {new_status}."
            )
            return True
        else:
            print(
                f"[{self.__class__.__name__}.toggle_status] Failed to update status for product ID '{product_id}'."
            )
            return False


class RETemplateService(BaseService):
    DATA_TYPE = RETemplateType

    def __init__(self, model: RETemplateModel):
        if not isinstance(model, RETemplateModel):
            raise TypeError(
                "model must be an instance of RETemplateModel or its subclass."
            )
        super().__init__(model)

    def create(self, payload: RETemplateType) -> bool:
        return super().create(payload)

    def read(self, record_id: int) -> Optional[RETemplateType]:
        return super().read(record_id)

    def read_all(self) -> List[RETemplateType]:
        return super().read_all()

    def update(self, record_id: int, payload: RETemplateType) -> bool:
        return super().update(record_id, payload)

    def delete(self, record_id: int) -> bool:
        return super().delete(record_id)

    def delete_multiple(self, record_ids: List[int]):
        return super().delete_multiple(record_ids)

    def import_data(self, payload: List[RETemplateType]):
        return super().import_data(payload)
