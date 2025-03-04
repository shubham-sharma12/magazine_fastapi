from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . import models, schemas, crud
from .db import SessionLocal, engine
from .jwt import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    token_expiry,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = verify_access_token(token)
    print(f"Token: {token}----")
    print(f"Payload: {payload}=====")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/users/login", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    new_refresh_token = create_refresh_token(data={"sub": db_user.username})
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@app.post("/users/reset-password")
def reset_password(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Implement your password reset logic here
    return {"msg": "Password reset link sent"}


@app.delete("/users/deactivate/{username}")
def deactivate_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"msg": "User deactivated"}


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.post("/magazines/", response_model=schemas.Magazine)
def create_magazine(magazine: schemas.MagazineCreate, db: Session = Depends(get_db)):
    return crud.create_magazine(db=db, magazine=magazine)


@app.post("/users/token/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = verify_access_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    db_user = crud.get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_refresh_token(data={"sub": db_user.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.get("/magazines/", response_model=list[schemas.Magazine])
def read_magazines(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_magazines(db, skip=skip, limit=limit)


@app.get("/magazines/{magazine_id}", response_model=schemas.Magazine)
def get_magazine_by_id(magazine_id: int, db: Session = Depends(get_db)):
    db_magazine = crud.get_magazine(db, magazine_id)
    if not db_magazine:
        raise HTTPException(status_code=404, detail="Magazine not found")
    return db_magazine


@app.put("/magazines/{magazine_id}", response_model=schemas.Magazine)
def update_magazine(
    magazine_id: int, magazine: schemas.MagazineCreate, db: Session = Depends(get_db)
):
    db_magazine = crud.get_magazine(db, magazine_id)
    if not db_magazine:
        raise HTTPException(status_code=404, detail="Magazine not found")
    db_magazine.title = magazine.title
    db_magazine.description = magazine.description
    db_magazine.base_price = magazine.base_price
    db.commit()
    db.refresh(db_magazine)
    return db_magazine


@app.delete("/magazines/{magazine_id}", response_model=schemas.Magazine)
def delete_magazine(magazine_id: int, db: Session = Depends(get_db)):
    db_magazine = crud.get_magazine(db, magazine_id)
    if not db_magazine:
        raise HTTPException(status_code=404, detail="Magazine not found")
    crud.delete_magazine(db, magazine_id)
    return db_magazine


@app.post("/plans/", response_model=schemas.Plan)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    return crud.create_plan(db=db, plan=plan)


@app.get("/plans/", response_model=list[schemas.Plan])
def read_plans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_plans(db, skip=skip, limit=limit)


@app.get("/plans/{plan_id}", response_model=schemas.Plan)
def get_plan_by_id(plan_id: int, db: Session = Depends(get_db)):
    db_plan = crud.get_plan(db, plan_id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return db_plan


@app.put("/plans/{plan_id}", response_model=schemas.Plan)
def update_plan(plan_id: int, plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    db_plan = crud.get_plan(db, plan_id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return crud.update_plan(db=db, plan_id=plan_id, plan=plan)


@app.delete("/plans/{plan_id}", response_model=schemas.Plan)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = crud.get_plan(db, plan_id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    crud.delete_plan(db, plan_id)
    return db_plan


@app.post("/subscriptions/", response_model=schemas.Subscription)
def create_subscription(
    subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)
):
    return crud.create_subscription(db=db, subscription=subscription)


@app.put("/subscriptions/{subscription_id}", response_model=schemas.Subscription)
def update_subscription(
    subscription_id: int,
    subscription: schemas.SubscriptionUpdate,
    db: Session = Depends(get_db),
):
    db_subscription = crud.get_subscription(db, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return crud.update_subscription(
        db=db, subscription_id=subscription_id, subscription=subscription
    )


@app.get("/subscriptions/", response_model=list[schemas.Subscription])
def read_subscriptions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_subscriptions(db, skip=skip, limit=limit)


@app.get("/subscriptions/{subscription_id}", response_model=schemas.Subscription)
def get_subscription_by_id(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = crud.get_subscription(db, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription


@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    token = current_user.token
    token_expiry(token)
    return current_user


@app.delete("/subscriptions/{subscription_id}", response_model=schemas.Subscription)
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = crud.get_subscription(db, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return crud.delete_subscription(db, subscription_id)
