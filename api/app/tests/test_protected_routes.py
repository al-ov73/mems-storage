import pytest

from .fixtures.test_data import TEST_USER

protectes_rotes_list = [
    '/memes',
    '/labels',
    '/comments',
    '/likes',
    'chat/messages',
]


@pytest.mark.parametrize('route', protectes_rotes_list)
def test_protected_route_memes(route, test_client, signup_user):
    response = test_client.get(route)
    assert response.status_code == 401
    access_token = signup_user(TEST_USER)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = test_client.get(route, headers=headers)
    assert response.status_code == 200
