import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from src.user.dtos import UserSchema, UserLoginSchema 
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException, status, Request
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime, timedelta, timezone
import time
from src.utils.mail import send_email

password_hash = PasswordHash.recommended()
def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

async def register(body: UserSchema, db: Session):
    print(body.model_dump())
    # Here you can add logic to save the user to the database using SQLAlchemy
    is_user_exists = db.query(UserModel).filter(UserModel.username == body.username).first() # Check if the user already exists in the database
    if is_user_exists:
       raise HTTPException(status_code=400, detail="User already exists")
    is_email_exists = db.query(UserModel).filter(UserModel.email == body.email).first() # Check if the email already exists in the database
    if is_email_exists:
       raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = get_password_hash(body.password) # Hash the password before saving it to the database
    new_user = UserModel(
        name=body.name,
        username=body.username, 
        email=body.email, 
        hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Send a confirmation email to the user after successful registration
    
    res = await send_email([new_user.email])
    print(res)

    return new_user


def login(body: UserLoginSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first() # Check if the user exists in the database
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=30) #
    token = jwt.encode({"_id": user.id, "exp": exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM) # Generate a JWT token with the user's id and expiration time
    print("Current UTC:", datetime.now(timezone.utc))
    print("Expiry UTC:", exp_time)
    print("Expiry timestamp:", exp_time.timestamp())
    return {"token": token}


def is_authenticated(request: Request, db: Session):
    try:
        token = request.headers.get("Authorization")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorized, Please login again")
        scheme, token = token.split(" ", 1)
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme")

        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = data.get("_id")
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorized, Please login again"
            )
        return user

    except InvalidTokenError as e:
        print("JWT ERROR:", type(e).__name__, str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorized, Please login again")