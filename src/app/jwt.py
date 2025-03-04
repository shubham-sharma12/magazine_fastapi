from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status

# Secret key to encode the JWT
SECRET_KEY = "d182fca46969ecb52609f0afe699294bb664430eb754ef311228e972dc457651"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 1  # Set to 1 second for testing
REFRESH_TOKEN_EXPIRE_DAYS = 30  # Set to 30 days for refresh token


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def token_expiry(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(status_code=401, detail="Token has no expiry time")
        expiry_time = datetime.utcfromtimestamp(exp)
        if expiry_time < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token has expired")
        return True
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(status_code=401, detail="Token has no expiry time")
        expiry_time = datetime.utcfromtimestamp(exp)
        if expiry_time < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token has expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
