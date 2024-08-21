import os
from dotenv import load_dotenv

from .test_config import test_client, add_test_meme, db_session, login_user

load_dotenv()

API_URL = os.getenv('API_URL')

TEST_FILENAME = 'test_filename'
TEST_USER = {
    'username': 'test_username',
    'password': 'test_password'
}


def test_protected_routes(test_client, login_user):
    response = test_client.get("/memes")
    assert response.status_code == 401
    access_token = login_user(TEST_USER)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = test_client.get("/memes", headers=headers)
    assert response.status_code == 200


def test_new_meme_post(test_client, login_user, add_test_meme):
    meme = add_test_meme(TEST_FILENAME, TEST_USER)
    init_meme_id = meme['id']
    assert meme['name'] == TEST_FILENAME
    access_token = login_user(TEST_USER)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = test_client.get("/memes", headers=headers)
    memes_list = response.json()
    new_meme = memes_list[0]
    assert new_meme['id'] == init_meme_id
    assert new_meme['name'] == TEST_FILENAME


def test_new_meme_without_file(test_client, login_user):
    access_token = login_user(TEST_USER)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = test_client.post(
        "/memes/",
        data={'filename': TEST_FILENAME},
        headers=headers,
    )
    assert response.status_code == 422


def test_new_meme_without_name(test_client, login_user):
    access_token = login_user(TEST_USER)
    headers = {'Authorization': f'Bearer {access_token}'}
    with open("app/tests/fixtures/test_meme.jpg", "rb") as image_file:
        response = test_client.post(
            "/memes/",
            files={'file': ('init_filename', image_file)},
            headers=headers,
        )
        assert response.status_code == 422


def test_meme_update(test_client, login_user, add_test_meme):
    # add meme
    meme = add_test_meme(TEST_FILENAME, TEST_USER)
    init_meme_id = meme['id']
    # update meme
    access_token = login_user(TEST_USER)
    headers = {'Authorization': f'Bearer {access_token}'}
    with open("app/tests/fixtures/test_meme.jpg", "rb") as image_file:
        response = test_client.put(
            f"/memes/{init_meme_id}",
            files={'file': ('init_filename', image_file)},
            data={'filename': 'updated_filename'},
            headers=headers,
        )
        assert response.status_code == 200
        updated_meme = response.json()
        assert updated_meme['id'] == init_meme_id
        assert updated_meme['name'] == 'updated_filename'


def test_meme_delete(test_client, login_user, add_test_meme):
    access_token = login_user(TEST_USER)
    headers = {'Authorization': f'Bearer {access_token}'}
    # add meme
    meme = add_test_meme(TEST_FILENAME, TEST_USER)
    init_meme_id = meme['id']
    # check add
    response = test_client.get("/memes", headers=headers)
    memes_list = response.json()
    assert len(memes_list) == 1

    # delete meme
    response = test_client.delete(f"/memes/{init_meme_id}", headers=headers)
    deleted_meme = response.json()
    deleted_meme_filename = deleted_meme['name']
    assert deleted_meme_filename == TEST_FILENAME
    # check delete
    response = test_client.get("/memes", headers=headers)
    memes_list = response.json()
    assert len(memes_list) == 0
