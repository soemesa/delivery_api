from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import UserSchema, DefaultOut, UserList, UserPublic

router = APIRouter(
    prefix='/users',
    tags=['users']
)

Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=DefaultOut, status_code=201)
def create_user(user: UserSchema, session: Session):
    db_user = session.scalar(
        select(User).where(User.username == user.username))
    if db_user:
        raise HTTPException(status_code=400, detail='Usuário já registrado!')

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return DefaultOut(message='Usuário registrado com sucesso!')


@router.get('/', response_model=None, status_code=200)
def read_users(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User). offset(skip).limit(limit)).all()

    return {'users': users}


@router.put('/{user_id}', response_model=DefaultOut, status_code=200)
def update_user(user_id: int, user: UserSchema, session: Session):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail='Usuário não encontardo!')

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    session.commit()
    session.refresh(db_user)

    return DefaultOut(message='Usuário atualizado com sucesso!')

