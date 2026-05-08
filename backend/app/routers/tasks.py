# app/routers/tasks.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Task, User
from ..schemas import TaskCreate, TaskUpdate, TaskResponse
from ..auth import verify_token

# Le indica a FastAPI que los tokens JWT llegan en el header Authorization
# El frontend los manda así: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Equivalente a express.Router() — agrupa todas las rutas de tareas
# prefix="/tasks" hace que todas empiecen con /tasks automáticamente
router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependencia reutilizable que se inyecta en cada ruta protegida.
    
    1. Recibe el token JWT del header
    2. Lo verifica y extrae el email
    3. Busca el usuario en la DB
    4. Lo devuelve para usarlo en la ruta
    
    Si algo falla, lanza 401 automáticamente antes de ejecutar la ruta.
    """
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    return user


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    GET /tasks
    Devuelve todas las tareas del usuario autenticado.
    El filtro por owner_id asegura que cada usuario
    solo vea sus propias tareas, nunca las de otros.
    """
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    return tasks


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    POST /tasks
    Crea una nueva tarea para el usuario autenticado.
    
    FastAPI valida automáticamente el body contra TaskCreate.
    Si falta 'title', responde 422 sin llegar a esta función.
    El owner_id se toma del token, no del body — el usuario
    no puede crear tareas a nombre de otro.
    """
    db_task = Task(
        title=task.title,
        description=task.description,
        owner_id=current_user.id
    )
    db.add(db_task)       # prepara el INSERT
    db.commit()           # ejecuta el INSERT en la DB
    db.refresh(db_task)   # recarga para obtener id y created_at generados
    return db_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    PUT /tasks/{task_id}
    Actualiza una tarea existente.
    
    Filtra por task_id Y owner_id al mismo tiempo:
    si la tarea existe pero pertenece a otro usuario,
    devuelve 404 como si no existiera (no revela información).
    Solo actualiza los campos que llegaron en el body,
    los que no llegaron quedan igual (exclude_unset=True).
    """
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {task_id} no encontrada"
        )

    # model_dump(exclude_unset=True) solo incluye los campos
    # que el usuario mandó, ignora los que no mandó
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)  # equivalente a db_task.field = value

    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    DELETE /tasks/{task_id}
    Elimina una tarea del usuario autenticado.
    
    204 No Content significa éxito sin body de respuesta.
    Mismo patrón de seguridad que update: filtra por
    task_id y owner_id juntos.
    """
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {task_id} no encontrada"
        )

    db.delete(db_task)
    db.commit()