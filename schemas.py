from pydantic import BaseModel
from datetime import datetime

# Schema para crear una tarea (datos que debe enviar el cliente)-----
class TaskCreate(BaseModel):
    titulo: str
    descripcion: str
    estado: str
    prioridad: int
    fecha_vencimiento: datetime | None = None
    board_id: int

# Schema para actualizar tareas.
from typing import Optional # Importante para campos opcionales (asi no pide todos para modificar 1 o 2)

class TaskUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    prioridad: Optional[int] = None
    fecha_vencimiento: Optional[datetime] = None

# Schema de salida (lo que devuelve la API).
# Incluye los campos de creación + datos generados por la DB.
# Se podría llamar TaskResponse
class TaskOut(TaskCreate):
    id:int
    fecha_creacion: datetime

    class Config:
        from_attributes = True


# Schema para crear un tablero---------
class BoardCreate(BaseModel):
    name: str
    color: str | None = None

# Schema board completo
class BoardOut(BoardCreate):
    id: int
    created_at:datetime | None = None
    user_id: int
    class Config:
        from_attributes = True

class BoardUpdate(BaseModel):
    name: Optional[str] | None 
    color: Optional[str] | None 


# Schema para crear un usuario---------------
class UserCreate(BaseModel):
    email: str 
    username: str
    password: str

# Schema para login
class UserLogin(BaseModel):
    email:str
    password:str

# Schema usuario completo (sin contraseña)
class UserOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True


#Hereda todo de BoardOut pero con el listado de tareas
class BoardWithTasks(BoardOut):
    tasks: list[TaskOut] = [] #SQLAlchemy rellena esto
    
    class Config:
        from_attributes = True
