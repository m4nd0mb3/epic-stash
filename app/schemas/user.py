"""
User Schemas
"""

# pylint: disable=R0903,W0107,E0611
from typing import Optional, List, Any
from uuid import UUID
from pydantic import UUID1, BaseModel, EmailStr


class UserSchemaBase(BaseModel):
    """
    Base User Schema
    """

    name: str
    email: EmailStr
    phone_number: str
    avatar: Optional[str]


class UserCreate(UserSchemaBase):
    """
    Create User Schema extend UserSchemaBase
    """

    password: str

class UserChangePassword(BaseModel):
    """
    Create User Schema extend UserSchemaBase
    """

    current_password: str
    new_password: str


class UserLogin(BaseModel):
    """
    Login  User Schema
    """

    email: EmailStr
    password: str


class User(UserSchemaBase):
    """
    User Schema
    """

    uuid: UUID
    is_active: bool = True
    is_staff: bool = False

    class Config:
        """
        Config User Schema
        """

        orm_mode = True


class RoleBase(BaseModel):
    """
    Base Role Schema
    """

    role_type: str
    user_uuid: UUID
    company_uuid: UUID


class RoleUserAddBase(BaseModel):
    """
    Base Role Schema
    """

    role_type: str
    user_uuid: UUID
    company_uuid: UUID


class RoleCreate(RoleBase):
    """
    Create Role Schema
    """

    pass


class Role(RoleBase):
    """
    Role Schema
    """

    uuid: UUID

    class Config:
        """
        Config
        """

        orm_mode = True


class UserWithRoles(User):
    """
    User Schema with Roles
    """

    roles: List[Role] = []
    store_uuid: Optional[Any]
    documents: Optional[Any]

    class Config:
        """
        Config
        """

        orm_mode = True
