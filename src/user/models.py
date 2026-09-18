from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from src.utils.db import Base

class UserModel(Base): # Define the Task model from SQLAlchemy Base 
    __tablename__ = "User_table"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String)
    