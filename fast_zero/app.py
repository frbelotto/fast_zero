from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import ConfigDict, validate_call
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fast_zero.database import SessionDep
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

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

    db_user = User(username=user.username, email=user.email, password=user.password)  # Poderia usar o unpacking se quiser também! **user.model_dump()

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
def read_users(session: SessionDep, limit: int = 10, offset: int = 0) -> UserList:
    db_users = session.scalars(select(User).limit(limit).offset(offset)).all()
    users = [UserPublic.model_validate(user) for user in db_users]
    return UserList(users=users)


@app.put('/users/{user_id}', response_model=UserPublic)
@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
def update_user(user_id: int, user: UserSchema, session: SessionDep) -> User:
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@app.delete('/users/{user_id}', response_model=Message)
@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
def delete_user(user_id: int, session: SessionDep) -> Message:
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    session.delete(user_db)
    session.commit()

    return Message(message='User deleted')
