#IMPORTO FASTAPI
from fastapi import FastAPI
from database import get_db, engine
from models import Base, Task, User, Board

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
from security import hash_password, verify_password, create_access_token
from deps import get_current_user

from fastapi.security import OAuth2PasswordRequestForm

#Creá todas las tablas definidas en models.py en la base
Base.metadata.create_all(bind=engine)


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permite cualquier frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#ENDPOINTS INICIALES
@app.get("/")
def root():
    return {"mensaje": "API funcionando"}

@app.get("/health")
def health():
    return {"Status":"ok"}



#--------------------ENDPOINTS TAREAS---------------------------------------------


@app.post("/tasks", response_model=schemas.TaskOut)
def create_Task(
    task:schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    board = db.query(Board).filter(
        Board.id == task.board_id,
        Board.user_id == current_user.id
        ).first()
    
    if not board:
        raise HTTPException(status_code=404, detail="El tablero no existe o no te pertenece")

    nueva = Task(**task.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@app.get("/tasks", response_model = list[schemas.TaskOut])
def list_tasks(
    board_id: int,            
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tareas = db.query(Task).join(Board).filter(
        Task.board_id == board_id,
        Board.user_id == current_user.id
    ).all()

    return tareas


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id:int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    t = db.query(Task).join(Board).filter(
        Task.id == task_id, 
        Board.user_id == current_user.id
    ).first()
    
    if not t:
        raise HTTPException(status_code=404, detail="Tarea no encontrada o no tienes permiso")
    return t


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int, 
    data: schemas.TaskUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    t = db.query(Task).join(Board).filter(
        Task.id == task_id, 
        Board.user_id == current_user.id
    ).first()

    if not t:
        raise HTTPException(404,"No puedes editar esta tarea")
    
    for k, v in data.dict(exclude_unset=True).items():
        setattr(t,k,v)
    
    db.commit()
    db.refresh(t)
    return t


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id:int, 
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    t = db.query(Task).join(Board).filter(
        Task.id == task_id, 
        Board.user_id == current_user.id
    ).first()

    if not t:
        raise HTTPException(404)
    
    db.delete(t)
    db.commit()
    return {"ok":True}




#--------------------ENDPOINTS BOARD---------------------------------------------
@app.post("/boards", response_model=schemas.BoardOut)
def create_board(
    board: schemas.BoardCreate, 
    db:Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
  
    nuevo = Board(**board.dict())
    nuevo.user_id = current_user.id
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.delete("/boards/{board_id}")
def delete_board(
    board_id:int, 
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.user_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(404)
    
    db.delete(board)
    db.commit()
    return {"ok":True}


@app.put("/boards/{board_id}")
def update_board(
    data: schemas.BoardUpdate,
    board_id:int, 
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.user_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(404,"Tablero no encontrado")

    update_data = data.dict(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(board, key, value)

    db.commit()
    db.refresh(board)
    return board

@app.get("/boards", response_model = list[schemas.BoardOut])
def list_boards(         
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    boards = db.query(Board).filter(
        Board.user_id == current_user.id
    ).all()

    return boards





#--------------------ENDPOINTS USER---------------------------------------------
@app.post("/users/register", response_model=schemas.UserOut)
def register_user(
    user:schemas.UserCreate,
    db:Session = Depends(get_db)):
   
    #verificams que no exista previamente el mail 
    user_exists = db.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # generar hash de la contraseña
    hashed = hash_password(user.password)
    
    nuevo = User(
        email=user.email,
        username=user.username,
        password_hash=hashed
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@app.post("/users/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), # Esto habilita el cuadrito
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
        ).first()

    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = create_access_token({"sub": str(db_user.id)})

    return {"access_token": token, "token_type": "bearer"}
    

@app.get("/me")
def me(user = Depends(get_current_user)):
    return user



#------------------------ENDPOINT PARA TRAER UNA TABLA CON TODAS SUS TAREAS----------------------
@app.get("/boards/{id_board}", response_model=schemas.BoardWithTasks)
def get_board_detail(       
    id_board: int,  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    board = db.query(Board).filter(
        Board.user_id == current_user.id, 
        Board.id == id_board
    ).first()

    if not board:
        raise HTTPException(status_code=404, detail="Tablero no encontrado")
    
    return board








#Puedo chequearlos con http://127.0.0.1:8000/health o http://127.0.0.1:8000/docs


