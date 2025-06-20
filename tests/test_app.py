from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'id': 1, 'username': 'Emerson', 'email': 'emerson@example.com'},
        ],
        'size': 1,
    }


def test_read_user_1(client):
    response = client.get('/user/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Emerson',
        'email': 'emerson@example.com',
    }


def test_update_user(client):
    response = client.put(
        '/user/1',
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
        '/user/666',
        json={
            'username': 'Gabriel',
            'email': 'gabriel@example.com',
            'password': 'lotr',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/user/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Gabriel',
        'email': 'gabriel@example.com',
    }
