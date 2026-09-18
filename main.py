from fastapi import FastAPI
from src.utils.db import get_db, Base, engine
from src.tasks.models import TaskModel
from src.tasks.router import task_routes
from src.user.router import user_routes

Base.metadata.create_all(bind=engine) # Create all tables
app = FastAPI(title= "This is my Task Management App") # Create the FastAPI application
app.include_router(task_routes) # Include the task routes in the FastAPI application
app.include_router(user_routes) # Include the user routes in the FastAPI application
