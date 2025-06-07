from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_root_deve_retornar_42():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': '42'}
