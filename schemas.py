"""
from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    age: int
    password: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None


"""

from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    age: int
    password: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None


class LoginSchema(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    age: int

    class Config:
        from_attributes = True
