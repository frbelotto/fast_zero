from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ConfigDict, validate_call
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fast_zero.database import SessionDep
from fast_zero.models import User
from fast_zero.schemas import JWTToken, Message, UserList, UserPublic, UserSchema
from fast_zero.security import create_access_token, get_current_user, get_password_hash, verify_password

app = FastAPI(title='FastAPI Zero to Hero')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
@validate_call(validate_return=True)
def read_root() -> Message:
    return Message(message='Olá Mundo!')


validate_call(validate_return=True)


@app.get('/html', response_class=HTMLResponse)
def read_root_html() -> str:
    return """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
def create_user(user: UserSchema, session: SessionDep) -> User:
    """Create a new user."""

    db_user: User | None = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email already exists')

    db_user = User(username=user.username, email=user.email, password=get_password_hash(user.password))
    # Poderia usar o unpacking se quiser também! **user.model_dump()

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/{user_id}', response_model=UserPublic)
@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
def read_user(user_id: int, session: SessionDep) -> User:
    user = session.scalars(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return user


@app.get('/users/', response_model=UserList)
@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
def read_users(session: SessionDep, limit: int = 10, offset: int = 0, current_user=Depends(get_current_user)) -> UserList:
    db_users = session.scalars(select(User).limit(limit).offset(offset)).all()
    users = [UserPublic.model_validate(user) for user in db_users]
    return UserList(users=users)


@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: SessionDep, current_user: User = Depends(get_current_user)) -> User:
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: SessionDep, current_user: User = Depends(get_current_user)) -> Message:
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return Message(message='User deleted')


@app.post('/token')
def login_for_acess_token(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends(), response_model=JWTToken):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Incorrect email or password')

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Incorrect email or password')
    access_token = create_access_token({'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


# Parei em https://www.youtube.com/live/wGZzEoO7e9s?si=sQmyHpkaqE8fVEA3&t=7253
# na hora de fazer os exercícios do curso
