from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

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

    user = session.scalar(
        select(User).where(User.username == new_user.username)
    )
    assert asdict(user) == {
        'id': 1,
        'username': 'testuser',
        'email': 'testuser@example',
        'password': 'nonsecurepassword',
        'created_at': time,
        'updated_at': time,
    }

    # parei aqui https://www.youtube.com/watch?v=I7IrmN7jMqE&t=4321s
