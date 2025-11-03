import os
import shutil
import tempfile
import json
import pytest

import ___PROD.main as main

TMP_JSON = None

def setup_module(module):
    global TMP_JSON
    src = os.path.join(os.path.dirname(__file__), '..', 'api.json')
    fd, tmp = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    shutil.copyfile(src, tmp)
    TMP_JSON = tmp
    # point the app to the temp copy
    main.JSON_FILE = tmp


def teardown_module(module):
    global TMP_JSON
    try:
        if TMP_JSON and os.path.exists(TMP_JSON):
            os.remove(TMP_JSON)
    except Exception:
        pass


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as c:
        yield c


def test_get_api(client):
    r = client.get('/api/')
    assert r.status_code == 200
    data = r.get_json()
    assert 'space' in data
    assert 'sensors' in data


def test_update_temperature(client):
    r = client.post('/api/update_temperature', json={'value': 25})
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('success') is True
    # verify file was updated
    with open(main.JSON_FILE, 'r', encoding='utf-8') as f:
        j = json.load(f)
    assert j['sensors']['temperature'][0]['value'] == 25


def test_update_state(client):
    r = client.post('/api/update_state', json={'message': 'pytest', 'open': True})
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('success') is True
    with open(main.JSON_FILE, 'r', encoding='utf-8') as f:
        j = json.load(f)
    assert j['state']['message'] == 'pytest'
    assert j['state']['open'] is True


def test_invalid_temperature(client):
    r = client.post('/api/update_temperature', json={'value': 'not-an-int'})
    assert r.status_code == 400
    data = r.get_json()
    assert 'error' in data
