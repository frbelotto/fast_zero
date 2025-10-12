from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'teste': 'teste'}
    token = create_access_token(data)
    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded.get('teste') == data.get('teste')
    assert 'exp' in decoded


def test_jwt_invalid(client):
    response = client.delete('/users/1', headers={'Authorization': 'Bearer token-invalido'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'could not validate credentials'}
