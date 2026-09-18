from fastapi import APIRouter, Depends, status, Request
from src.tasks import controller
from src.tasks.dtos import TaskSchema, TaskResponseSchema
from src.utils.db import get_db
from src.utils.helpers import is_authenticated
from src.user.models import UserModel
from typing import List

task_routes = APIRouter(prefix="/tasks")

@task_routes.post("/create", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED) # Define a POST endpoint to create a new task in the database
def create_task(body: TaskSchema, db = Depends(get_db), user: UserModel = Depends(is_authenticated)): # Define a POST endpoint to create a new task in the database
    return controller.create_task(body , db, user) # Call the controller function to create the task

@task_routes.get("/get_alltasks", response_model=list[TaskResponseSchema], status_code=status.HTTP_200_OK) # Define a GET endpoint to retrieve all tasks from the database
def get_task(db = Depends(get_db),  user: UserModel = Depends(is_authenticated)): # Define a GET endpoint to retrieve all tasks from the database using the controller function
    return controller.get_task(db, user) # Call the controller function to retrieve the tasks

@task_routes.get("/one_task/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponseSchema)
def get_one_task(task_id: int, db = Depends(get_db), user: UserModel = Depends(is_authenticated)): # Define a GET endpoint to retrieve a single task by its ID from the database using the controller function
    return controller.get_one_task(task_id, db) # Call the controller function to retrieve the task

@task_routes.put("/update_task/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponseSchema) # Define a PUT endpoint to update a task by its ID in the database
def update_task(body: TaskSchema, task_id: int, db = Depends(get_db), user: UserModel = Depends(is_authenticated)): # Define a PUT endpoint to update a task by its ID in the database using the controller function
    return controller.update_task(body, task_id, db, user)

@task_routes.delete("/delete_task/{task_id}", status_code=status.HTTP_200_OK, response_model= None) # Define a DELETE endpoint to delete a task by its ID from the database
def delete_task(task_id: int, db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.delete_task(task_id, db, user) # Call the controller function to delete the task