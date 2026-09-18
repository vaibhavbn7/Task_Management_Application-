from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.utils.settings import settings
from src.user.models import UserModel
from src.utils.db import get_db
import jwt
from jwt import InvalidTokenError


def is_authenticated(request: Request, db: Session = Depends(get_db)):
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