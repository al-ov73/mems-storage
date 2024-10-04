from .fixtures.test_data import TEST_LABEL, TEST_FILE, TEST_USER


def test_labels(
    test_client,
    signup_user,
    add_test_meme,
):
    # add meme
    access_token = signup_user(TEST_USER)
    meme = add_test_meme(TEST_FILE, access_token)
    init_meme_id = meme["id"]
    # create label
    label_data = {
        'title': TEST_LABEL['title'],
        'meme_id': init_meme_id,
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post(
        "/labels",
        data=label_data,
        headers=headers
    )
    # check label create
    meme = response.json()
    assert meme['id'] == init_meme_id
    meme_labels = meme['meme_labels']
    assert len(meme_labels) == 1
    assert meme_labels[0]['title'] == TEST_LABEL['title']
