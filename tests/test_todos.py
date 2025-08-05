from http import HTTPStatus

import factory
import factory.fuzzy
import pytest

from fast_zero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, token):
    data = {'title': 'string', 'description': 'string', 'state': 'draft'}

    response = client.post(
        '/todos/', headers={'Authorization': f'Bearer {token}'}, json=data
    )
    data['id'] = 1
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == data


@pytest.mark.asyncio
async def test_list_todos_should_return_5(session, client, user, token):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(expected_todos, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_pagination_should_return_2(
    session, client, user, token
):
    expected_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/?offset=3&limit=3',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title_should_return_1(
    session, client, user, token
):
    expected_todos = 1
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title='teste')
    )
    session.add_all(
        TodoFactory.create_batch(1, user_id=user.id, title='dormir')
    )
    await session.commit()

    response = client.get(
        '/todos/?title=dormir', headers={'Authorization': f'Bearer {token}'}
    )
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description_should_return_1(
    session, client, user, token
):
    expected_todos = 1
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, description='teste')
    )
    session.add_all(
        TodoFactory.create_batch(1, user_id=user.id, description='resposta')
    )
    await session.commit()

    response = client.get(
        '/todos/?description=resposta',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_todo_state_should_return_2(
    session, client, user, token
):
    expected_todos = 2
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, state='doing')
    )
    session.add_all(
        TodoFactory.create_batch(2, user_id=user.id, state='trash')
    )
    await session.commit()

    response = client.get(
        '/todos/?state=trash',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()
    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Todo deleted'}


@pytest.mark.asyncio
async def test_delete_todo_not_found(session, client, user, token):
    session.add_all(TodoFactory.create_batch(1, user_id=user.id))
    await session.commit()

    response = client.delete(
        '/todos/42', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}


@pytest.mark.asyncio
async def test_delete_todo_other_user(session, client, token, other_user):
    todo_other_user = TodoFactory(user_id=other_user.id)
    session.add(todo_other_user)
    await session.commit()

    response = client.delete(
        f'/todos/{todo_other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}


@pytest.mark.asyncio
async def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()

    data = {'title': 'Novo', 'description': 'Nova Ordem', 'state': 'doing'}
    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=data,
    )
    data['id'] = todo.id

    assert response.status_code == HTTPStatus.OK
    assert response.json() == data


@pytest.mark.asyncio
async def test_patch_todo_error(session, client, user, token):
    data = {'title': 'Novo', 'description': 'Nova Ordem', 'state': 'doing'}
    response = client.patch(
        '/todos/42',
        headers={'Authorization': f'Bearer {token}'},
        json=data,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}
