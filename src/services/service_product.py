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

    def delete_multiple(self, record_ids):
        return super().delete_multiple(record_ids)

    def import_data(self, payload: List[REProductType]):
        return super().import_data(payload)

    def find_by_pid(self, pid: str) -> Optional[REProductType]:
        return self._find_by_model_index(
            find_method_name="find_row_by_pid", value="pid"
        )


class MiscProductService(BaseService):
    DATA_TYPE = MiscProductType

    def __init__(self, model: MiscProductModel):
        if not isinstance(model, MiscProductModel):
            raise TypeError(
                "model must be an instance of MiscProductModel or its subclass."
            )
        super().__init__(model)


class RETemplateService(BaseService):
    DATA_TYPE = RETemplateType

    def __init__(self, model: RETemplateModel):
        if not isinstance(model, RETemplateModel):
            raise TypeError(
                "model must be an instance of RETemplateModel or its subclass."
            )
        super().__init__(model)
