from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token


def test_token_expired_after_time(client, user):
    with freeze_time('1989-04-17 12:00:00'):
        response = client.post(
            'auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        token = response.json()['access_token']

    with freeze_time('1989-04-17 12:30:00'):
        response = client.get(
            '/users/', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
