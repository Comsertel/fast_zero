from http import HTTPStatus


def test_root_deve_retornar_42(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': '42'}
