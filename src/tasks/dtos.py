from pydantic import BaseModel

class TaskSchema(BaseModel): # Define the Pydantic model for task data validation from the request body
    title: str
    description: str
    is_completed: bool = False

class TaskResponseSchema(BaseModel): # Define the Pydantic model for task data validation from the request body
    id: int
    title: str
    description: str
    is_completed: bool 
    user_id: int | None = 0