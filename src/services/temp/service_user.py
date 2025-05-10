# src/services/service_user.py
from typing import List, Dict, Any, Optional

# Import BaseService
from src.services.base_service import (
    BaseService,
)  # Assuming BaseService is in base_service.py

# Import UserType dataclass
from src.my_types import UserType, ListedProductType

# Import UserModel
from src.models.model_user import UserModel, ListedProductModel


class UserService(BaseService):
    """
    Service for managing UserType records using UserModel (QSqlTableModel).
    """

    # Define the specific data type (dataclass)
    DATA_TYPE = UserType

    def __init__(self, model: UserModel):
        """
        Initializes the UserService with a UserModel instance.
        """
        # Ensure the model is an instance of UserModel (or its subclass)
        if not isinstance(model, UserModel):
            raise TypeError("model must be an instance of UserModel or its subclass.")
        # Call the base class constructor, passing the model
        super().__init__(model)
        # The base class will now handle getting column names, DB connection, etc.

    # =========================================================================
    # Specific Find Methods using BaseModel's find methods
    # =========================================================================

    def find_by_uid(self, uid: str) -> Optional[UserType]:
        """
        Finds a user record by UID using the model's find_row_by_uid method.
        Returns a UserType object or None if not found.
        """
        # Use the helper _find_one_by_model_index from BaseService
        # Pass the name of the find method in UserModel ('find_row_by_uid') and the value
        return self._find_one_by_model_index(
            find_method_name="find_row_by_uid", value=uid
        )

    # Add other specific find methods here if needed, using _find_one_by_model_index
    # or _find_many_by_model_index (if implemented) or direct model interaction if complex.
    # Example:
    # def find_by_username(self, username: str) -> Optional[UserType]:
    #     return self._find_one_by_model_index(find_method_name='find_row_by_username', value=username)
    # (Requires adding find_row_by_username method to UserModel)

    # You can override base CRUD methods if you need custom logic before/after calling super().method()
    # Example:
    # def create(self, payload: UserType) -> bool:
    #     print(f"[{self.__class__.__name__}.create] Custom logic before creating user: {payload.username}")
    #     success = super().create(payload)
    #     if success:
    #         print(f"[{self.__class__.__name__}.create] Custom logic after successful creation.")
    #     return success


# src/services/service_listed_product.py
# Assuming this is in a separate file or combined appropriately
# from typing import List, Dict, Any, Optional
# from src.services.base_service import BaseService
# from src.my_types import ListedProductType
# from src.models.model_user import ListedProductModel # ListedProductModel is in model_user.py
# from src import constants # If needed


class ListedProductService(BaseService):
    """
    Service for managing ListedProductType records using ListedProductModel (QSqlTableModel).
    """

    DATA_TYPE = ListedProductType

    def __init__(self, model: ListedProductModel):
        if not isinstance(model, ListedProductModel):
            raise TypeError(
                "model must be an instance of ListedProductModel or its subclass."
            )
        super().__init__(model)

    # No specific find methods needed based on the provided ListedProductModel methods
    # If ListedProductModel had find_row_by_pid, you would add:
    # def find_by_pid(self, pid: str) -> Optional[ListedProductType]:
    #     return self._find_one_by_model_index(find_method_name='find_row_by_pid', value=pid)
