from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user_deve_retornar_usuario_criado(client):
    user_data = {
        'username': 'Emerson',
        'email': 'emerson@example.com',
        'password': 'bananaphone',
    }
    response = client.post('/users/', json=user_data)

    del user_data['password']
    user_data['id'] = 1

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == user_data


def test_create_user_deve_retornar_422_quando_dados_invalidos(client):
    user_data = {'username': 'Emerson', 'email': ''}
    response = client.post('/users/', json=user_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            user_schema,
        ],
        'size': 1,
    }


def test_read_user_1(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'Gabriel',
            'email': 'gabriel@example.com',
            'password': 'lotr',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Gabriel',
        'email': 'gabriel@example.com',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_integrity_error(client, user, token):
    response = client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': user.email,
            'password': 'secret',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_read_user_1_not_found(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_create_integrity_error(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'User with this email or username already exists'
    }
