from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class MagazineBase(BaseModel):
    title: str
    description: str


class MagazineCreate(MagazineBase):
    base_price: float


class Magazine(MagazineBase):
    id: int

    class Config:
        orm_mode = True


class PlanBase(BaseModel):
    name: str
    price: int


class PlanCreate(PlanBase):
    magazine_id: int


class Plan(PlanBase):
    id: int
    magazine_id: int

    class Config:
        orm_mode = True


class SubscriptionBase(BaseModel):
    user_id: int
    plan_id: int
    price: float
    next_renewal_date: date


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(SubscriptionBase):
    is_active: bool


class Subscription(SubscriptionBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
