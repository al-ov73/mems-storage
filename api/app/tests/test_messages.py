from api.app.config.app_config import ALGORITHM, JWT_TOKEN_SECRET_KEY
import jwt
import json
from .fixtures.test_data import TEST_MESSAGE, TEST_USER

WS_URL = 'ws://127.0.0.1:8000/chat/ws'


def test_messages(
    test_client,
    signup_user,
):
    access_token = signup_user(TEST_USER)
    user = jwt.decode(
        access_token,
        JWT_TOKEN_SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    user_id = user['id']

    # create message
    message_data = {
        'text': TEST_MESSAGE['text'],
        'author': user_id,
    }
    with test_client.websocket_connect(WS_URL) as websocket:
        websocket.send_text(json.dumps(message_data))
        new_message = websocket.receive_json()
        assert new_message['text'] == TEST_MESSAGE['text']
        assert new_message['author']['id'] == user_id
