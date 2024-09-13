import os
from dotenv import load_dotenv

from .fake.fake_storage_repository import FakeStorageRepository
from .test_config import test_client, add_test_meme, db_session, login_user, signup_user

load_dotenv()


TEST_FILE = {
    'name': 'test_filename',
    'category': 'OTHER',
}
TEST_USER = {
    'username': 'test_username',
    'password': 'test_password',
}


def test_protected_routes(test_client, signup_user):
    response = test_client.get("/memes")
    assert response.status_code == 401
    access_token = signup_user(TEST_USER)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = test_client.get("/memes", headers=headers)
    assert response.status_code == 200


def test_new_meme_post(test_client, signup_user, login_user, add_test_meme):
    access_token = signup_user(TEST_USER)
    meme = add_test_meme(TEST_FILE, access_token)
    init_meme_id = meme['id']
    assert meme['name'] == TEST_FILE['name']
    headers = {'Authorization': f'Bearer {access_token}'}
    response = test_client.get("/memes", headers=headers)
    memes_list = response.json()
    new_meme = memes_list[0]
    assert new_meme['id'] == init_meme_id
    assert new_meme['name'] == TEST_FILE['name']


def test_new_meme_without_file(test_client, signup_user):
    access_token = signup_user(TEST_USER)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = test_client.post(
        "/memes/",
        data={
            'filename': TEST_FILE['name'],
            'category': TEST_FILE['category'],
        },
        headers=headers,
    )
    assert response.status_code == 422


def test_new_meme_without_name(test_client, signup_user):
    access_token = signup_user(TEST_USER)
    headers = {'Authorization': f'Bearer {access_token}'}
    with open("app/tests/fixtures/test_meme.jpg", "rb") as image_file:
        response = test_client.post(
            "/memes/",
            files={'file': ('init_filename', image_file)},
            headers=headers,
        )
        assert response.status_code == 422


def test_meme_update(test_client, signup_user, login_user, add_test_meme):
    access_token = signup_user(TEST_USER)
    # add meme
    meme = add_test_meme(TEST_FILE, access_token)
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


def test_meme_delete(test_client, signup_user, login_user, add_test_meme):
    access_token = signup_user(TEST_USER)
    # add meme  
    meme = add_test_meme(TEST_FILE, access_token)
    init_meme_id = meme['id']
    # check add
    headers = {'Authorization': f'Bearer {access_token}'}
    response = test_client.get("/memes", headers=headers)
    memes_list = response.json()
    assert len(memes_list) == 1

    # delete meme
    response = test_client.delete(f"/memes/{init_meme_id}", headers=headers)
    deleted_meme = response.json()
    deleted_meme_filename = deleted_meme['name']
    assert deleted_meme_filename == TEST_FILE['name']
    # check delete
    response = test_client.get("/memes", headers=headers)
    memes_list = response.json()
    assert len(memes_list) == 0
