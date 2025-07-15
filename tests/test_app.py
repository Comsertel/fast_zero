from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_42(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': '42'}


def test_create_user_deve_retornar_usuario_criado(client):
    user_data = {
        'username': 'Emerson',
        'email': 'emerson@example.com',
        'password': 'bananaphone',
    }
    response = client.post('/user/', json=user_data)

    del user_data['password']
    user_data['id'] = 1

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == user_data


def test_create_user_deve_retornar_422_quando_dados_invalidos(client):
    user_data = {'username': 'Emerson', 'email': ''}
    response = client.post('/user/', json=user_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_read_users_without_user(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [],
        'size': 0,
    }


def test_read_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            user_schema,
        ],
        'size': 1,
    }


def test_read_user_1(client, user):
    response = client.get('/user/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_update_user(client, user):
    response = client.put(
        f'/user/{user.id}',
        json={
            'username': 'Gabriel',
            'email': 'gabriel@example.com',
            'password': 'lotr',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Gabriel',
        'email': 'gabriel@example.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/user/1',
        json={
            'username': 'Gabriel',
            'email': 'gabriel@example.com',
            'password': 'lotr',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete(f'/user/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/user/{user.id}',
        json={
            'username': 'fausto',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'User with this email or username already exists'
    }


def test_delete_user_not_found(client):
    response = client.delete('/user/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user_1_not_found(client):
    response = client.get('/user/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_create_integrity_error(client, user):
    response = client.post(
        '/user/',
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


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
