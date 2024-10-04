from .fixtures.test_data import TEST_COMMENT, TEST_FILE, TEST_USER


def test_comments(
    test_client,
    signup_user,
    add_test_meme,
):
    # add meme
    access_token = signup_user(TEST_USER)
    meme = add_test_meme(TEST_FILE, access_token)
    init_meme_id = meme["id"]
    # create comment
    comment_data = {
        'text': TEST_COMMENT['text'],
        'meme_id': init_meme_id,
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post(
        "/comments",
        data=comment_data,
        headers=headers
    )
    # check comment create
    meme = response.json()
    assert meme['id'] == init_meme_id
    meme_comments = meme['comments']
    assert len(meme_comments) == 1
    assert meme_comments[0]['text'] == TEST_COMMENT['text']
