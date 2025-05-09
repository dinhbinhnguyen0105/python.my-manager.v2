# my_types.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserType:
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
    id: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]


@dataclass
class ListedProductType:
    pid: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    id: Optional[int]


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
    tid: Optional[str]
    action: Optional[int]
    part: Optional[int]
    content: Optional[str]
    id: Optional[int]


@dataclass
class MiscProductType:
    pid: Optional[str]
    category: Optional[int]
    title: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[int]
    id: Optional[int]
