from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.deps import get_current_user
from app.users.models import User
from .schemas import ResponseCost, CreateCost 
from . import crud  

router  = APIRouter(prefix="/costs", tags=["costs"])


@router.post("/", response_model=ResponseCost ,status_code=status.HTTP_201_CREATED)
def creat_cost(cost: CreateCost, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    cost = crud.add_cost(cost, user=user,db=db)
    return cost


@router.get("/", response_model=list[ResponseCost])
def get_costs(
    limit: int = Query(10, ge=1, le=50),
    skip: int = Query(0),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)):

    costs = crud.get_costs_by_user(user, db)
    return costs


@router.get("/{id}", response_model=ResponseCost)
def get_cost(
    id: int = Path(gt=0, description="Cost id"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)):

    cost = crud.get_cost(id, user, db)
    if cost is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cost with this {id} not found."
        )
        
    return cost


    


@router.put("/{id}", response_model=ResponseCost)
def edit_cost(
    now_cost: CreateCost,
    db: Session = Depends(get_db),
    id:int = Path(gt=0, description="Cost id"),
    user: User = Depends(get_current_user)):

    cost = crud.edit_cost(id, now_cost, user, db)
    if not cost:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cost with this {id}  not found.")
    
    return cost
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cost(
    id:int = Path(gt=0, description="Cost id"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)):

    cost = crud.delete_cost(id, user, db)

    if not cost:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cost with this {id}  not found.")