from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    color = Column(String, default="azul")
    #Un User puede tener varios Board
    user_id = Column(Integer, ForeignKey("user.id"))

    #Cascade Delete, borra el tablero junto a sus tareas
    tasks = relationship("Task", back_populates="board", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    estado = Column(String, default="pendiente")
    prioridad = Column(Integer, default=1)
    fecha_vencimiento = Column(DateTime, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    #Un Board puede tener varios Task
    board_id = Column(Integer, ForeignKey("board.id"))
    board = relationship("Board", back_populates="tasks")

    

