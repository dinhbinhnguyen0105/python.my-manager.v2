# service_product.py
from typing import Optional
from src.my_types import REProductType, RETemplateType, MiscProductType
from src import constants
from src.services.base_service import BaseService
from src.models.model_product import ProductMiscModel, ProductREModel, TemplateREModel


class ProductREService(BaseService):
    """
    Service for managing REProductType records using ProductREModel (QSqlTableModel).
    """

    DATA_TYPE = REProductType

    def __init__(self, model: ProductREModel):
        if not isinstance(model, ProductREModel):
            raise TypeError(
                "model must be an instance of ProductREModel or its subclass."
            )
        super().__init__(model)

    # Implement specific find methods using the model's find methods
    def find_by_pid(self, pid: str) -> Optional[REProductType]:
        """
        Finds a RE product record by PID using the model's find_row_by_pid method.
        Returns a REProductType object or None if not found.
        """
        # Use the helper _find_one_by_model_index from BaseService
        # Pass the name of the find method in ProductREModel ('find_row_by_pid') and the value
        return self._find_one_by_model_index(
            find_method_name="find_row_by_pid", value=pid
        )

    # Add other specific find methods if needed


class ProductMiscService(BaseService):
    """
    Service for managing MiscProductType records using ProductMiscModel (QSqlTableModel).
    """

    DATA_TYPE = MiscProductType

    def __init__(self, model: ProductMiscModel):
        if not isinstance(model, ProductMiscModel):
            raise TypeError(
                "model must be an instance of ProductMiscModel or its subclass."
            )
        super().__init__(model)

    # Implement specific find methods using the model's find methods
    def find_by_pid(self, pid: str) -> Optional[MiscProductType]:
        """
        Finds a Misc product record by PID using the model's find_row_by_pid method.
        Returns a MiscProductType object or None if not found.
        """
        # Use the helper _find_one_by_model_index from BaseService
        # Pass the name of the find method in ProductMiscModel ('find_row_by_pid') and the value
        return self._find_one_by_model_index(
            find_method_name="find_row_by_pid", value=pid
        )

    # Add other specific find methods if needed


# src/services/service_template_re.py
# Assuming this is in a separate file or combined appropriately
# from typing import List, Dict, Any, Optional
# from src.services.base_service import BaseService
# from src.my_types import RETemplateType
# from src.models.model_product import TemplateREModel # TemplateREModel is in model_product.py
# from src import constants # If needed


class TemplateREService(BaseService):
    """
    Service for managing RETemplateType records using TemplateREModel (QSqlTableModel).
    """

    DATA_TYPE = RETemplateType

    def __init__(self, model: TemplateREModel):
        if not isinstance(model, TemplateREModel):
            raise TypeError(
                "model must be an instance of TemplateREModel or its subclass."
            )
        super().__init__(model)

    # Implement specific find methods using the model's find methods
    def find_by_tid(self, tid: str) -> Optional[RETemplateType]:
        """
        Finds a RE template record by TID using the model's find_row_by_tid method.
        Returns a RETemplateType object or None if not found.
        """
        # Use the helper _find_one_by_model_index from BaseService
        # Pass the name of the find method in TemplateREModel ('find_row_by_tid') and the value
        return self._find_one_by_model_index(
            find_method_name="find_row_by_tid", value=tid
        )

    # Add other specific find methods if needed
