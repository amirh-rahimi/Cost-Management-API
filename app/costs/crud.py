from sqlalchemy.orm import Session

from app.users.models import User
from .models import Cost as CostModel
from .schemas import CreateCost


def add_cost(cost: CreateCost, user: User, db: Session) -> CostModel:

    db_cost = CostModel(**cost.model_dump(), user_id=user.id)
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)

    return db_cost

def get_cost(id: int, user: User, db: Session) -> CostModel | None:

    db_cost = db.query(CostModel).filter_by(id=id, user_id=user.id).one_or_none()
    return db_cost


def get_costs(db: Session, user: User, limit:int, skip:int) -> list[CostModel]:
    return db.query(CostModel).filter_by(user_id=user.id).offset(skip).limit(limit).all()

def edit_cost(id: int, now_cost: CreateCost, user: User, db: Session) -> CostModel | bool:
    db_cost = get_cost(id, user, db)
    if db_cost is None:
        return False

    for key, value in now_cost.model_dump().items():
        setattr(db_cost, key, value)
    
    db.commit()
    db.refresh(db_cost)
    return db_cost


def delete_cost(id: int, user: User, db: Session) -> bool:
    db_cost = get_cost(id, user, db)
    if db_cost is None:
        return False

    db.delete(db_cost)
    db.commit()
    return True