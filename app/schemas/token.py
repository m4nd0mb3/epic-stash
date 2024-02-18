"""
Token Schemas
"""

# pylint: disable=E0611,R0903
from pydantic import BaseModel


class Token(BaseModel):
    """
    Token Schema Class
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    TokenData Schema Class
    """

    email: str
