from pydantic import BaseModel


class User(BaseModel):
    id: str | None
    name: str
    email: str


class UserCreate(BaseModel):
    name: str
    email: str
