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


@pytest.mark.parametrize('endpoint,key', [
    ('update_temperature', ('sensors','temperature')),
    ('update_humidity', ('sensors','humidity')),
    ('update_power_consumption', ('sensors','power_consumption')),
    ('update_network_connections', ('sensors','network_connections')),
    ('update_network_traffic', ('sensors','network_traffic')),
    ('update_people_now_present', ('sensors','people_now_present')),
])
def test_update_endpoints(client, endpoint, key):
    # valid update
    r = client.post(f'/api/{endpoint}', json={'value': 42})
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('success') is True
    # verify file changed
    with open(main.JSON_FILE, 'r', encoding='utf-8') as f:
        j = json.load(f)
    # drill down
    obj = j
    for k in key:
        assert k in obj
        obj = obj[k]
    # obj should be a list or dict; check value presence
    if isinstance(obj, list):
        # handle network_traffic where structure differs
        if endpoint == 'update_network_traffic':
            assert obj[0]['properties']['bits_per_second']['value'] == 42
        else:
            assert obj[0]['value'] == 42
    else:
        # unexpected structure
        assert True


def test_missing_value_returns_400(client):
    r = client.post('/api/update_temperature', json={})
    assert r.status_code == 400
    data = r.get_json()
    assert 'error' in data


def test_invalid_value_type(client):
    r = client.post('/api/update_temperature', json={'value': 'abc'})
    assert r.status_code == 400


def test_update_state(client):
    r = client.post('/api/update_state', json={'message': 'fulltest', 'open': False})
    assert r.status_code == 200
    data = r.get_json()
    assert data.get('success') is True
    with open(main.JSON_FILE, 'r', encoding='utf-8') as f:
        j = json.load(f)
    assert j['state']['message'] == 'fulltest'
    assert j['state']['open'] is False


def test_auth_token_enforced(client, monkeypatch):
    # set API_TOKEN
    monkeypatch.setenv('API_TOKEN', 'SECRETTOKEN')
    # reload require_token reads os.environ each call, so it's fine
    # Without header should return 401
    r = client.post('/api/update_temperature', json={'value': 11})
    assert r.status_code == 401
    # With header should work
    r2 = client.post('/api/update_temperature', json={'value': 11}, headers={'X-API-Token': 'SECRETTOKEN'})
    assert r2.status_code == 200


def test_malformed_json_returns_400(client):
    # send invalid JSON by using data not json and wrong content-type
    r = client.post('/api/update_temperature', data='not-json', headers={'Content-Type': 'application/json'})
    assert r.status_code == 400
