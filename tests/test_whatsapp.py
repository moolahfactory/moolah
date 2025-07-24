import os
from datetime import datetime


def test_get_config_returns_phone_number_id(client, db_setup, auth_headers):
    os.environ['PHONE_NUMBER_ID'] = '12345'
    headers = auth_headers()
    resp = client.get('/config', headers=headers)
    assert resp.status_code == 200
    assert resp.json()['phone_number_id'] == '12345'
    os.environ.pop('PHONE_NUMBER_ID')


def test_store_and_retrieve_messages(client, db_setup, auth_headers):
    payload = {
        'entry': [
            {
                'changes': [
                    {
                        'value': {
                            'messages': [
                                {
                                    'id': 'wamid.ID1',
                                    'from': '1111',
                                    'timestamp': str(int(datetime.now().timestamp())),
                                    'text': {'body': 'hello'},
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

    resp = client.post('/whatsapp', json=payload)
    assert resp.status_code == 204

    headers = auth_headers()
    list_resp = client.get('/whatsapp/', headers=headers)
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert len(data) == 1
    assert data[0]['body'] == 'hello'
    assert data[0]['from'] == '1111'


def test_duplicate_webhook_idempotent(client, db_setup, auth_headers):
    payload = {
        'entry': [
            {
                'changes': [
                    {
                        'value': {
                            'messages': [
                                {
                                    'id': 'wamid.DUP',
                                    'from': '2222',
                                    'timestamp': str(int(datetime.now().timestamp())),
                                    'text': {'body': 'hi'},
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

    first = client.post('/whatsapp', json=payload)
    assert first.status_code == 204

    second = client.post('/whatsapp', json=payload)
    assert second.status_code == 204

    headers = auth_headers()
    resp = client.get('/whatsapp/', headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1


def test_auth_token_reuse(client, db_setup, auth_headers):
    headers = auth_headers()
    me_resp = client.get('/users/me/', headers=headers)
    assert me_resp.status_code == 200
    wa_resp = client.get('/whatsapp/', headers=headers)
    assert wa_resp.status_code == 200
    assert wa_resp.json() == []
