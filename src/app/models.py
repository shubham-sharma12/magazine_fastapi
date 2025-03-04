from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import relationship
from .db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    subscriptions = relationship("Subscription", back_populates="user")


class Magazine(Base):
    __tablename__ = "magazines"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    plans = relationship("Plan", back_populates="magazine")
    base_price = Column(Float, index=True)


class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    magazine_id = Column(Integer, ForeignKey("magazines.id"))
    magazine = relationship("Magazine", back_populates="plans")
    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    user = relationship("User", back_populates="subscriptions")
    price = Column(Float)
    next_renewal_date = Column(Date)
    is_active = Column(Boolean, default=True)
    plan = relationship("Plan", back_populates="subscriptions")
