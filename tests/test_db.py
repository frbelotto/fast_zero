from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

from fast_zero.database import get_session
from fast_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User, time=datetime.now()) as time:
        new_user: User = User(
            username='testuser',
            email='testuser@example',
            password='nonsecurepassword',
        )

        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == new_user.username))
    assert asdict(user) == {
        'id': 1,
        'username': 'testuser',
        'email': 'testuser@example',
        'password': 'nonsecurepassword',
        'created_at': time,
        'updated_at': time,
    }


def test_get_session_cria_sessao():
    gen = get_session()  # retorna um generator
    session = next(gen)  # entra no with, cria a Session
    assert session is not None
    # encerra o generator para acionar o __exit__ do with
    try:
        next(gen)
    except StopIteration:
        pass
