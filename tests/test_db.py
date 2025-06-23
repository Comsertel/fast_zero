from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(
            username='alice', email='teste@teste.com', password='secret'
        )
        session.add(user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))
    assert asdict(user) == {
        'username': 'alice',
        'email': 'teste@teste.com',
        'id': 1,
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }
