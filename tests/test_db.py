from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(
            username='alice', email='teste@teste.com', password='secret'
        )
        session.add(user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))
    assert asdict(user) == {
        'username': 'alice',
        'email': 'teste@teste.com',
        'id': 1,
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }
