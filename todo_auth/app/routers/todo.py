from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import TodoCreate,TodoUpdate
from app.database.models import Todo, User
from app.database.database import get_db
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/todos")
def get_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(current_user.id)
    todos = db.query(Todo).filter(Todo.owner_id == current_user.id, Todo.is_active == True).all()
    
    if not todos:
        raise HTTPException(status_code=404, detail="No todos found")
    
    return todos

@router.post("/todos")
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    db_todo = Todo(**todo.dict(), owner_id=current_user.id)  
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/todos/{todo_id}")
def soft_delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db_todo.is_active = False # Soft delete
    db.commit()
    db.refresh(db_todo)
    return {"message": "Todo marked as inactive"}


@router.patch("/todos/{todo_id}")
def update_todo_partial(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in todo_update.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    todo_update: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in todo_update.dict().items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo





