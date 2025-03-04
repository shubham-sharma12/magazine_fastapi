from sqlalchemy.orm import Session
from . import models, schemas
from .models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    return user


def get_magazine(db: Session, magazine_id: int):
    return db.query(models.Magazine).filter(models.Magazine.id == magazine_id).first()


def get_magazines(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Magazine).offset(skip).limit(limit).all()


def create_magazine(db: Session, magazine: schemas.MagazineCreate):
    db_magazine = models.Magazine(
        title=magazine.title,
        description=magazine.description,
        base_price=magazine.base_price,
    )
    db.add(db_magazine)
    db.commit()
    db.refresh(db_magazine)
    return db_magazine


def delete_magazine(db: Session, magazine_id: int):
    db_magazine = (
        db.query(models.Magazine).filter(models.Magazine.id == magazine_id).first()
    )
    if db_magazine:
        db.delete(db_magazine)
        db.commit()
    return db_magazine


def get_plan(db: Session, plan_id: int):
    return db.query(models.Plan).filter(models.Plan.id == plan_id).first()


def get_plans(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Plan).offset(skip).limit(limit).all()


def create_plan(db: Session, plan: schemas.PlanCreate):
    db_plan = models.Plan(
        name=plan.name, price=plan.price, magazine_id=plan.magazine_id
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def update_plan(db: Session, plan_id: int, plan: schemas.PlanCreate):
    db_plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if db_plan:
        db_plan.name = plan.name
        db_plan.price = plan.price
        db_plan.magazine_id = plan.magazine_id
        db.commit()
        db.refresh(db_plan)
    return db_plan


def delete_plan(db: Session, plan_id: int):
    db_plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if db_plan:
        db.delete(db_plan)
        db.commit()
    return db_plan


def get_subscription(db: Session, subscription_id: int):
    return (
        db.query(models.Subscription)
        .filter(models.Subscription.id == subscription_id)
        .first()
    )


def get_subscriptions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Subscription).offset(skip).limit(limit).all()


def create_subscription(db: Session, subscription: schemas.SubscriptionCreate):
    db_subscription = models.Subscription(
        user_id=subscription.user_id,
        plan_id=subscription.plan_id,
        price=subscription.price,
        next_renewal_date=subscription.next_renewal_date,
        is_active=True,
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def update_subscription(
    db: Session, subscription_id: int, subscription: schemas.SubscriptionUpdate
):
    db_subscription = (
        db.query(models.Subscription)
        .filter(models.Subscription.id == subscription_id)
        .first()
    )
    if db_subscription:
        db_subscription.user_id = subscription.user_id
        db_subscription.plan_id = subscription.plan_id
        db_subscription.price = subscription.price
        db_subscription.next_renewal_date = subscription.next_renewal_date
        db_subscription.is_active = subscription.is_active
        db.commit()
        db.refresh(db_subscription)
    return db_subscription


def delete_subscription(db: Session, subscription_id: int):
    db_subscription = (
        db.query(models.Subscription)
        .filter(models.Subscription.id == subscription_id)
        .first()
    )
    if db_subscription:
        db_subscription.is_active = False
        db.commit()
        db.refresh(db_subscription)
    return db_subscription
