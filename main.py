from flask import Flask, Blueprint, request, jsonify
import json
import os
import tempfile
import logging

app = Flask(__name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Use path relative to this file so running from another cwd still works
JSON_FILE = os.path.join(os.path.dirname(__file__), 'api.json')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def get_json_data():
    """Read the JSON file and return the parsed object or None if missing/invalid."""
    if not os.path.exists(JSON_FILE):
        logging.error('JSON file not found: %s', JSON_FILE)
        return None
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.exception('Failed to read JSON file')
        return None


def save_json_data(json_data):
    """Atomically save the JSON file to avoid corruption from concurrent writers."""
    dirpath = os.path.dirname(JSON_FILE) or '.'
    try:
        with tempfile.NamedTemporaryFile('w', dir=dirpath, delete=False, encoding='utf-8') as tmp:
            json.dump(json_data, tmp, indent=4, ensure_ascii=False)
            tmp_path = tmp.name
        os.replace(tmp_path, JSON_FILE)
        logging.info('Saved JSON data to %s', JSON_FILE)
    except Exception:
        logging.exception('Failed to write JSON file')
        raise


def require_token():
    """Simple API token check. If API_TOKEN env is set, require header X-API-Token to match.
    Returns tuple (ok: bool, response: (json, status) | None)
    """
    token = os.environ.get('API_TOKEN')
    if not token:
        return True, None
    header = request.headers.get('X-API-Token')
    if header == token:
        return True, None
    return False, (jsonify({'error': 'Unauthorized'}), 401)


@api_bp.route('/', methods=['GET'])
def api_json():
    json_data = get_json_data()
    if json_data is None:
        return jsonify({'error': 'JSON file not found'}), 500
    return jsonify(json_data)


@api_bp.route('/update_state', methods=['POST'])
def update_state():
    ok, resp = require_token()
    if not ok:
        return resp
    json_data = get_json_data()
    if json_data is None:
        return jsonify({'error': 'JSON file not found'}), 500
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({'error': 'expected JSON body'}), 400

    if 'message' in payload:
        json_data.setdefault('state', {})['message'] = str(payload['message'])
    if 'open' in payload:
        # accept booleans or strings
        v = payload['open']
        if isinstance(v, bool):
            json_data.setdefault('state', {})['open'] = v
        else:
            json_data.setdefault('state', {})['open'] = str(v).lower() in ['true', '1', 'yes']
    save_json_data(json_data)
    return jsonify({'success': True, 'data': json_data.get('state', {})})


def get_int_from_payload(payload, key):
    if key not in payload:
        return None, (jsonify({'error': f'missing {key}'}), 400)
    try:
        return int(payload[key]), None
    except (TypeError, ValueError):
        return None, (jsonify({'error': f'{key} must be an integer'}), 400)


@api_bp.route('/update_temperature', methods=['POST'])
def update_temperature():
    ok, resp = require_token()
    if not ok:
        return resp
    json_data = get_json_data()
    if json_data is None:
        return jsonify({'error': 'JSON file not found'}), 500
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({'error': 'expected JSON body'}), 400
    value, err = get_int_from_payload(payload, 'value')
    if err:
        return err
    json_data.setdefault('sensors', {}).setdefault('temperature', [{'unit': '°C', 'location': 'Im Space', 'value': 0}])[0]['value'] = value
    save_json_data(json_data)
    return jsonify({'success': True, 'data': json_data['sensors']['temperature'][0]})


@api_bp.route('/update_humidity', methods=['POST'])
def update_humidity():
    ok, resp = require_token()
    if not ok:
        return resp
    json_data = get_json_data()
    if json_data is None:
        return jsonify({'error': 'JSON file not found'}), 500
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({'error': 'expected JSON body'}), 400
    value, err = get_int_from_payload(payload, 'value')
    if err:
        return err
    json_data.setdefault('sensors', {}).setdefault('humidity', [{'unit': '%', 'location': 'Im Space', 'value': 0}])[0]['value'] = value
    save_json_data(json_data)
    return jsonify({'success': True, 'data': json_data['sensors']['humidity'][0]})


@api_bp.route('/update_power_consumption', methods=['POST'])
def update_power_consumption():
    ok, resp = require_token()
    if not ok:
        return resp
    json_data = get_json_data()
    if json_data is None:
        return jsonify({'error': 'JSON file not found'}), 500
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({'error': 'expected JSON body'}), 400
    value, err = get_int_from_payload(payload, 'value')
    if err:
        return err
    json_data.setdefault('sensors', {}).setdefault('power_consumption', [{'unit': 'W', 'location': 'Im Space', 'value': 0}])[0]['value'] = value
    save_json_data(json_data)
    return jsonify({'success': True, 'data': json_data['sensors']['power_consumption'][0]})


@api_bp.route('/update_network_connections', methods=['POST'])
def update_network_connections():
    ok, resp = require_token()
    if not ok:
        return resp
    json_data = get_json_data()
    if json_data is None:
        return jsonify({'error': 'JSON file not found'}), 500
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({'error': 'expected JSON body'}), 400
    value, err = get_int_from_payload(payload, 'value')
    if err:
        return err
    json_data.setdefault('sensors', {}).setdefault('network_connections', [{'location': 'Im Odenwilusenz_WLAN / Odenwilusenz_LAN', 'value': 0}])[0]['value'] = value
    save_json_data(json_data)
    return jsonify({'success': True, 'data': json_data['sensors']['network_connections'][0]})


@api_bp.route('/update_network_traffic', methods=['POST'])
def update_network_traffic():
    ok, resp = require_token()
    if not ok:
        return resp
    json_data = get_json_data()
    if json_data is None:
        return jsonify({'error': 'JSON file not found'}), 500
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({'error': 'expected JSON body'}), 400
    value, err = get_int_from_payload(payload, 'value')
    if err:
        return err
    traffic = json_data.setdefault('sensors', {}).setdefault('network_traffic', [{'properties': {'bits_per_second': {'name': 'Durchschnittswert Upstream und Downstream', 'value': 0}}}])[0]
    traffic.setdefault('properties', {}).setdefault('bits_per_second', {})['value'] = value
    save_json_data(json_data)
    return jsonify({'success': True, 'data': traffic['properties']['bits_per_second']})


@api_bp.route('/update_people_now_present', methods=['POST'])
def update_people_now_present():
    ok, resp = require_token()
    if not ok:
        return resp
    json_data = get_json_data()
    if json_data is None:
        return jsonify({'error': 'JSON file not found'}), 500
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({'error': 'expected JSON body'}), 400
    value, err = get_int_from_payload(payload, 'value')
    if err:
        return err
    json_data.setdefault('sensors', {}).setdefault('people_now_present', [{'value': 0}])[0]['value'] = value
    save_json_data(json_data)
    return jsonify({'success': True, 'data': json_data['sensors']['people_now_present'][0]})


# Register blueprint
app.register_blueprint(api_bp)


if __name__ == '__main__':
    # Don't enable debug by default. Use FLASK_DEBUG=1 to enable during development.
    debug_flag = os.environ.get('FLASK_DEBUG') == '1'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_flag)
