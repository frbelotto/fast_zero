from contextlib import contextmanager
from datetime import datetime
from typing import Generator, Type

import pytest
from fastapi.testclient import TestClient
from pydantic import validate_call
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture
def user(session: Session) -> User:
    password = 'testtest'

    user = User(username='Teste', email='teste@test.com', password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password  # type: ignore
    return user


@pytest.fixture
def client(session) -> Generator[TestClient]:
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()  # Fecha todas as conexões


@validate_call(validate_return=True)
@contextmanager
def _mock_db_time(*, model: Type, time: datetime):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def token(client, user):
    response = client.post('/token', data={'username': user.email, 'password': user.clean_password})
    token = response.json()
    return token['access_token']
