from fastapi import APIRouter, Depends, status, Request
from src.user import controller
from src.user.dtos import UserSchema, UserResponseSchema, UserLoginSchema
from src.utils.db import get_db
from sqlalchemy.orm import Session

user_routes = APIRouter(prefix="/users")

@user_routes.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(body: UserSchema, db: Session = Depends(get_db)):
    return await controller.register(body, db)

@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login_user(body: UserLoginSchema, db: Session = Depends(get_db)):
    return controller.login(body, db)

@user_routes.get("/is_auth", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def is_authenticated(request: Request, db: Session = Depends(get_db)):
    return controller.is_authenticated(request, db)
