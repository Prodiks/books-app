from pydantic import BaseModel, Field


class SUserRegister(BaseModel):
    login: str = Field(...)
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class SUserAuth(BaseModel):
    login: str = Field(...)
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
