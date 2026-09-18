from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from src.user.models import UserModel
from fastapi import HTTPException


def create_task(body: TaskSchema, db: Session, user: UserModel): # Function to create a new task in the database based on the request body and database session
    print(body.model_dump())
    data = body.model_dump() # Convert the Pydantic model to a dictionary
    # Here you can add logic to save the task to the database using SQLAlchemy
    new_task = TaskModel(
        title=data["title"],
        description=data["description"],
        is_completed=data["is_completed"],
        user_id=user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def get_task(db: Session, user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all() # Query all tasks from the database for the current user
    return tasks

def get_one_task(task_id: int, db: Session):
    one_task = db.query(TaskModel).get(task_id) # Query a single task by its ID from the database
    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found") # Raise an HTTP exception if the task is not found
    return one_task

def update_task(body: TaskSchema, task_id: int, db: Session, user: UserModel):
    task = db.query(TaskModel).get(task_id) # Query the task to be updated by its ID from the database
    if not task:
        raise HTTPException(status_code=404, detail="Task not found") # Raise an HTTP exception if the task is not found
    if task.user_id != user.id:
        raise HTTPException(status_code=401, detail="You are not authorized to update this task") # Raise an HTTP exception if the user is not authorized to update the task    
    data = body.model_dump() # Convert the Pydantic model to a dictionary
    for key, value in data.items():
        setattr(task, key, value) # Update the task attributes with the new values

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def delete_task(task_id: int, db: Session,  user: UserModel):
    task = db.query(TaskModel).get(task_id) # Query the task to be deleted by its ID from the database
    if not task:
        raise HTTPException(status_code=404, detail="Task not found") # Raise an HTTP exception if the task is not found
    if task.user_id != user.id:
        raise HTTPException(status_code=401, detail="You are not authorized to delete this task") # Raise an HTTP exception if the user is not authorized to delete the task
    db.delete(task)
    db.commit()

    return None