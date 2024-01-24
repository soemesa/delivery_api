from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.database import get_session
from src.models import User
from src.schemas import Token
from src.security import verify_password, create_access_token, get_current_user

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token, status_code=200)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(status_code=400, detail='Usuário inválido')

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail='Senha inválida')

    access_token = create_access_token(data={'sub': user.username})

    return Token(access_token=access_token, token_type='bearer')


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: User = Depends(get_current_user)):
    new_access_token = create_access_token(data={'sub': user.username})

    return Token(access_token=new_access_token, token_type='bearer')
