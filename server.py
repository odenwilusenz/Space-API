# Import necessary libraries
import flask
import time
import threading
import json

# Initialize Flask application
last_keepalive = time.time()
keepalive_timeout = 60 # seconds
app = flask.Flask(__name__)
json_path = "api.json"
file_lock = threading.Lock()

#
# No Category App Routes
#

from functools import wraps
from flask import request, Response, send_file

def check_auth(username, password):
    return username == 'SpaceAPI-Testing' and password == 'Sp@c3Ap1'

def authenticate():
    return Response(
        'Authentication required', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/testing')
@requires_auth
def testing():
    return send_file('test.html')

@app.route('/api.json', methods=['GET'])
def get_json():
    return flask.send_file(json_path, mimetype='application/json')

@app.route('/')
def index():
    return flask.jsonify({'error': 'not found / invalid path'}), 404

# Website to give a api keepalive signal
@app.route('/api/keepalive', methods=['GET', 'POST', 'PUT'])
def keepalive():
    global last_keepalive
    last_keepalive = time.time()
    return flask.jsonify({'status': 'ok'})


# 
# Write
#

# Get Requests with REST API to change the values with the right key and value
@app.route('/api/change/get', methods=['GET'])
def change_get():
    key = flask.request.args.get('key')
    value = flask.request.args.get('value')
    if not key or value is None:
        return flask.jsonify({'error': 'missing key or value'}), 406
    return write_status(key, value)

# Post Requests to change the values with the right key and value
@app.route('/api/change/post', methods=['POST'])
def post():
    key = flask.request.form.get('key')
    value = flask.request.form.get('value')
    if not key or value is None:
        return flask.jsonify({'error': 'missing key or value'}), 406
    return write_status(key, value)

# Put Requests to change the values with the right key and value
@app.route('/api/change/put', methods=['PUT'])
def put():
    key = flask.request.form.get('key')
    value = flask.request.form.get('value')
    if not key or value is None:
        return flask.jsonify({'error': 'missing key or value'}), 406
    return write_status(key, value)


#
# Read
#

# Get Requests to read the values with the right key
@app.route('/api/get/<path:key>', methods=['GET'])
def get_api(key):
    return get_status(key)



#
# Other functions
#

# Background Thread to check for the keepalive signal
def monitor_keepalive():
    global last_keepalive
    while True:
        time.sleep(5)
        now = time.time()
        if now - last_keepalive > keepalive_timeout:
            print(f"{time.time()} - KeepAlive - Keepalive timeout reached, setting odw to closed")
            write_status("open", "false")


# Function to write status to the JSON file
def write_status(key, value):
    with file_lock:
        with open(json_path, 'r') as file:
            data = json.load(file)
        # Setting the Space closed (false) or open (true)
        if key == "open":
            if value == "true" or value == "false":
                data["state"]["open"] = value == "true"
                print(f"{time.time()} - Status - Writing status >open< to {value}")
            else:
                print(f"{time.time()} - Status - Invalid value for open: {value}")
                return flask.jsonify({'error': 'invalid value for open'}), 406
        # Setting the Open Message to a new Value
        elif key == "message":
            data["state"]["message"] = value
            print(f"{time.time()} - Status - Writing status >message< to {value}")
        # Setting the Temperature inside the Space in the API
        elif key == "temperature":
            try:
                data["sensors"]["temperature"][0]["value"] = int(value)
                print(f"{time.time()} - Status - Writing status >temperature< to {value}")
            except (ValueError, IndexError, KeyError, TypeError):
                print(f"{time.time()} - Status - Invalid value for temperature: {value}")
                return flask.jsonify({'error': 'invalid value for temperature'}), 406
        # Setting the Humidity inside the Space in the API
        elif key == "humidity":
            try:
                data["sensors"]["humidity"][0]["value"] = int(value)
                print(f"{time.time()} - Status - Writing status >humidity< to {value}")
            except (ValueError, IndexError, KeyError, TypeError):
                print(f"{time.time()} - Status - Invalid value for humidity: {value}")
                return flask.jsonify({'error': 'invalid value for humidity'}), 406
        # Setting the Total Power Consumption to the API
        elif key == "power":
            try:
                data["sensors"]["power_consumption"][0]["value"] = int(value)
                print(f"{time.time()} - Status - Writing status >power< to {value}")
            except (ValueError, IndexError, KeyError, TypeError):
                print(f"{time.time()} - Status - Invalid value for power: {value}")
                return flask.jsonify({'error': 'invalid value for power'}), 406
        # Setting the Total Network Connections to the API
        elif key == "net_conn":
            try:
                data["sensors"]["network_connections"][0]["value"] = int(value)
                print(f"{time.time()} - Status - Writing status >network_conn< to {value}")
            except (ValueError, IndexError, KeyError, TypeError):
                print(f"{time.time()} - Status - Invalid value for network_conn: {value}")
                return flask.jsonify({'error': 'invalid value for network_conn'}), 406
        # Setting the Total Network Traffic (in bits per seconds)
        elif key == "net_traffic":
            try:
                data["sensors"]["network_traffic"][0]["properties"]["bits_per_second"]["value"] = int(value)
                print(f"{time.time()} - Status - Writing status >network_traffic< to {value}")
            except (ValueError, IndexError, KeyError, TypeError):
                print(f"{time.time()} - Status - Invalid value for network_traffic: {value}")
                return flask.jsonify({'error': 'invalid value for network_traffic'}), 406
        else:
            print(f"{time.time()} - Status - Invalid key: {key}")
            return flask.jsonify({'error': 'invalid key was send'}), 406

        # Write changes back to file
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=2)
        return flask.jsonify({'status': 'ok'}), 200

# Function to read status from the JSON file
def get_status(key):
    try:
        with file_lock:
            with open(json_path, 'r') as file:
                data = json.load(file)
        if key == "open":
            return flask.jsonify({'open': data["state"]["open"]}), 200
        elif key == "message":
            return flask.jsonify({'message': data["state"]["message"]}), 200
        elif key == "temperature":
            return flask.jsonify({'temperature': data["sensors"]["temperature"][0]["value"]}), 200
        elif key == "humidity":
            return flask.jsonify({'humidity': data["sensors"]["humidity"][0]["value"]}), 200
        elif key == "power":
            return flask.jsonify({'power': data["sensors"]["power_consumption"][0]["value"]}), 200
        elif key == "net_conn":
            return flask.jsonify({'network_connections': data["sensors"]["network_connections"][0]["value"]}), 200
        elif key == "net_traffic":
            return flask.jsonify({'network_traffic': data["sensors"]["network_traffic"][0]["properties"]["bits_per_second"]["value"]}), 200
        else:
            return flask.jsonify({'error': 'invalid key'}), 406
    except Exception as e:
        return flask.jsonify({'error': f'Failed to read status: {str(e)}'}), 500


if __name__ == '__main__':
    monitor_thread = threading.Thread(target=monitor_keepalive, daemon=True)
    monitor_thread.start()
    app.run(host='0.0.0.0', port=5000)