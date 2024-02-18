from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

M = TypeVar('M')

class PaginatedResponse(GenericModel, Generic[M]):
    total: int = Field(description='Number of total items')
    page: int = Field(description='Number of current page returned in the response')
    count: int = Field(description='Number of items returned in the response')
    items: List[M] = Field(description='List of items returned in the response following given criteria')