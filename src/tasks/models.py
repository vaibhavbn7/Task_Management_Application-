from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from src.utils.db import Base

class TaskModel(Base): # Define the Task model from SQLAlchemy Base 
    __tablename__ = "User_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("User_table.id", ondelete="CASCADE")) 
    # Define a foreign key relationship to the UserModel table and ondelete cascade to delete tasks when the associated user is deleted

    