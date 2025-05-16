# my_types.py

from dataclasses import dataclass
from typing import Optional

from PyQt6.QtCore import QRunnable


@dataclass
class UserType:
    id: Optional[int]
    uid: Optional[str]
    username: Optional[str]
    password: Optional[str]
    two_fa: Optional[str]
    email: Optional[str]
    email_password: Optional[str]
    phone_number: Optional[str]
    note: Optional[str]
    type: Optional[str]
    user_group: Optional[int]
    mobile_ua: Optional[str]
    desktop_ua: Optional[str]
    status: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]


@dataclass
class ListedProductType:
    id: Optional[int]
    user_id: int
    pid: str
    created_at: Optional[str]
    updated_at: Optional[str]


@dataclass
class UserSettingProxyType:
    id: Optional[int]
    value: str
    created_at: Optional[str]
    updated_at: Optional[str]


@dataclass
class UserSettingUDDType:
    id: Optional[int]
    value: str
    is_selected: int
    created_at: Optional[str]
    updated_at: Optional[str]


@dataclass
class REProductType:
    id: Optional[int]
    pid: Optional[str]
    status: Optional[int]
    action: Optional[int]
    province: Optional[int]
    district: Optional[int]
    ward: Optional[int]
    street: Optional[str]
    category: Optional[int]
    area: Optional[float]
    price: Optional[float]
    legal: Optional[int]
    structure: Optional[float]
    function: Optional[str]
    building_line: Optional[int]
    furniture: Optional[int]
    description: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


@dataclass
class RETemplateType:
    id: Optional[int]
    tid: Optional[str]
    action: Optional[int]
    part: Optional[int]
    content: Optional[str]


@dataclass
class MiscProductType:
    id: Optional[int]
    pid: Optional[str]
    category: Optional[int]
    title: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[int]


@dataclass
class RobotTaskType:
    user_info: UserType
    udd: str
    headless: bool
    action_name: str


@dataclass
class InProgressType(RobotTaskType):
    worker: Optional[QRunnable]
    proxy_url: str


@dataclass
class FailedType(RobotTaskType):
    error_message: str


@dataclass
class SucceededType(RobotTaskType):
    is_success: bool
