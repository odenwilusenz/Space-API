"""
Space-API Server für Odenwilusenz
Implementierung nach Space-API Standard
Das Script lädt die api.json und aktualisiert sie mit dynamischen Daten
"""

from flask import Flask, jsonify, request, session
import json
import time
from functools import wraps
import threading
import os

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'space-api-secret-key-change-in-production')

# Keep-Alive Configuration
KEEP_ALIVE_TIMEOUT = 30  # Sekunden
keep_alive_timestamp = None
keep_alive_lock = threading.Lock()

# Manual Override Password
MANUAL_OVERRIDE_PASSWORD = os.environ.get('SPACE_API_PASSWORD', 'admin123')
sessions = {}  # Simple session storage

# Store for sensor data and state (in-memory, könnte erweitert werden mit Datenbank)
sensor_data = {
    'temperature': {
        'indoor': {'value': 20.5, 'lastchange': int(time.time())},
        'outdoor': {'value': 15.2, 'lastchange': int(time.time())}
    },
    'humidity': {
        'indoor': {'value': 45, 'lastchange': int(time.time())},
        'outdoor': {'value': 60, 'lastchange': int(time.time())}
    },
    'power_consumption': {'value': 2500, 'lastchange': int(time.time())},
    'network_connections': {'value': 8, 'lastchange': int(time.time())},
    'network_traffic': {
        'download': {'value': 125000, 'lastchange': int(time.time())},
        'upload': {'value': 45000, 'lastchange': int(time.time())}
    }
}

space_state = {
    'open': False,
    'message': 'Space ist geschlossen',
    'lastchange': int(time.time())
}

# ============================================================
# Hilfsfunktionen
# ============================================================

def load_api_config():
    """Lädt die ursprüngliche api.json Konfiguration"""
    try:
        with open('api.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_api_config(data):
    """Speichert die aktualisierte api.json Konfiguration"""
    try:
        with open('api.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Fehler beim Speichern der api.json: {e}")
        return False

def check_keep_alive():
    """Überprüft, ob das Keep-Alive Timeout abgelaufen ist"""
    global keep_alive_timestamp, space_state
    
    if space_state['open']:
        with keep_alive_lock:
            if keep_alive_timestamp is None:
                # Keep-Alive wurde noch nicht gesendet
                return False
            
            current_time = time.time()
            elapsed = current_time - keep_alive_timestamp
            
            if elapsed > KEEP_ALIVE_TIMEOUT:
                # Timeout abgelaufen - Space automatisch schließen
                space_state['open'] = False
                space_state['message'] = f'Automatisch geschlossen durch Keep-Alive Timeout ({int(elapsed)}s)'
                space_state['lastchange'] = int(current_time)
                
                # api.json aktualisieren
                api_data = load_api_config()
                if api_data:
                    api_data['state'] = space_state
                    save_api_config(api_data)
                
                print(f"⏱️  Keep-Alive Timeout: Space wurde automatisch geschlossen")
                return False
    
    return True

def get_nested_value(obj, path):
    """
    Gibt einen verschachtelten Wert aus einem Dictionary basierend auf einem Pfad
    Beispiel: get_nested_value(data, 'sensors/temperature/indoor/value')
    """
    keys = path.split('/')
    current = obj
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list):
            try:
                index = int(key)
                current = current[index]
            except (ValueError, IndexError):
                return None
        else:
            return None
    
    return current

def set_nested_value(obj, path, value):
    """
    Setzt einen verschachtelten Wert in einem Dictionary basierend auf einem Pfad
    Beispiel: set_nested_value(data, 'sensors/temperature/indoor/value', 22.5)
    """
    keys = path.split('/')
    current = obj
    
    # Navigiere zu dem Elternelement
    for key in keys[:-1]:
        if isinstance(current, dict):
            if key not in current:
                current[key] = {}
            current = current[key]
        elif isinstance(current, list):
            try:
                index = int(key)
                current = current[index]
            except (ValueError, IndexError):
                return False
        else:
            return False
    
    # Setze den finalen Wert
    last_key = keys[-1]
    if isinstance(current, dict):
        current[last_key] = value
        return True
    elif isinstance(current, list):
        try:
            index = int(last_key)
            current[index] = value
            return True
        except (ValueError, IndexError):
            return False
    
    return False

def get_updated_api():
    """
    Gibt die komplette api.json mit aktualisierten Sensor- und State-Daten zurück
    Prüft auch das Keep-Alive Timeout
    """
    # Keep-Alive prüfen (falls space offen ist)
    check_keep_alive()
    
    api_data = load_api_config()
    if not api_data:
        return None
    
    # Update state (open/closed Status)
    api_data['state']['open'] = space_state['open']
    api_data['state']['message'] = space_state['message']
    api_data['state']['lastchange'] = space_state['lastchange']
    
    # Temperatursensoren
    if 'temperature' in api_data.get('sensors', {}):
        for sensor in api_data['sensors']['temperature']:
            if sensor['name'] == 'indoor_temperature':
                sensor['value'] = sensor_data['temperature']['indoor']['value']
                sensor['lastchange'] = sensor_data['temperature']['indoor']['lastchange']
            elif sensor['name'] == 'outdoor_temperature':
                sensor['value'] = sensor_data['temperature']['outdoor']['value']
                sensor['lastchange'] = sensor_data['temperature']['outdoor']['lastchange']
    
    # Luftfeuchtigkeitssensoren
    if 'humidity' in api_data.get('sensors', {}):
        for sensor in api_data['sensors']['humidity']:
            if sensor['name'] == 'indoor_humidity':
                sensor['value'] = sensor_data['humidity']['indoor']['value']
                sensor['lastchange'] = sensor_data['humidity']['indoor']['lastchange']
            elif sensor['name'] == 'outdoor_humidity':
                sensor['value'] = sensor_data['humidity']['outdoor']['value']
                sensor['lastchange'] = sensor_data['humidity']['outdoor']['lastchange']
    
    # Stromverbrauch
    if 'power_consumption' in api_data.get('sensors', {}):
        for sensor in api_data['sensors']['power_consumption']:
            sensor['value'] = sensor_data['power_consumption']['value']
            sensor['lastchange'] = sensor_data['power_consumption']['lastchange']
    
    # Netzwerkverbindungen
    if 'network_connections' in api_data.get('sensors', {}):
        for sensor in api_data['sensors']['network_connections']:
            sensor['value'] = sensor_data['network_connections']['value']
            sensor['lastchange'] = sensor_data['network_connections']['lastchange']
    
    # Netzwerk Traffic
    if 'network_traffic' in api_data.get('sensors', {}):
        for sensor in api_data['sensors']['network_traffic']:
            if sensor['name'] == 'download_traffic':
                sensor['properties']['bits_per_second']['value'] = sensor_data['network_traffic']['download']['value']
                sensor['lastchange'] = sensor_data['network_traffic']['download']['lastchange']
            elif sensor['name'] == 'upload_traffic':
                sensor['properties']['bits_per_second']['value'] = sensor_data['network_traffic']['upload']['value']
                sensor['lastchange'] = sensor_data['network_traffic']['upload']['lastchange']
    
    return api_data

# ============================================================
# SpaceAPI Standard Endpoints
# ============================================================

@app.route('/api.json', methods=['GET'])
def api_json():
    """
    Hauptendpoint: Gibt komplette api.json nach SpaceAPI Standard mit aktualisierten Daten
    """
    api_data = get_updated_api()
    if not api_data:
        return jsonify({'error': 'api.json not found'}), 500
    return jsonify(api_data), 200

# ============================================================
# Root Endpoints
# ============================================================

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({'message': 'Kein Command'}), 404

@app.route('/api/', methods=['GET'])
def api_root():
    """API Root endpoint"""
    return jsonify({'message': 'Kein Command'}), 404

# ============================================================
# /api/get/* Endpoints - GET Request
# ============================================================

@app.route('/api/get/<path:path>', methods=['GET'])
def api_get(path):
    """
    Gibt Werte aus der api.json zurück basierend auf dem Pfad
    Beispiel: /api/get/state/open -> gibt open-Status zurück
    Beispiel: /api/get/sensors/temperature/0/value -> gibt Temperatur-Wert zurück
    """
    api_data = get_updated_api()
    if not api_data:
        return jsonify({'error': 'api.json not found'}), 500
    
    value = get_nested_value(api_data, path)
    
    if value is None:
        return jsonify({'error': f'Pfad nicht gefunden: {path}'}), 404
    
    return jsonify({
        'path': path,
        'value': value
    }), 200

# ============================================================
# /api/change/* Endpoints - GET mit ?value Parameter
# ============================================================

@app.route('/api/change/<path:path>', methods=['GET'])
def api_change_get(path):
    """
    Ändert Werte über GET Parameter
    Beispiel: /api/change/state/open?value=true
    Beispiel: /api/change/sensors/temperature/0/value?value=22.5
    """
    value_param = request.args.get('value')
    
    if value_param is None:
        return jsonify({'error': 'value Parameter erforderlich'}), 400
    
    # Versuche, den Wert zu konvertieren
    try:
        if value_param.lower() in ['true', 'false']:
            final_value = value_param.lower() == 'true'
        elif '.' in value_param:
            final_value = float(value_param)
        else:
            try:
                final_value = int(value_param)
            except ValueError:
                final_value = value_param
    except:
        final_value = value_param
    
    api_data = get_updated_api()
    if not api_data:
        return jsonify({'error': 'api.json not found'}), 500
    
    if set_nested_value(api_data, path, final_value):
        # Update lastchange für State
        if path.startswith('state/'):
            api_data['state']['lastchange'] = int(time.time())
        
        save_api_config(api_data)
        
        return jsonify({
            'success': True,
            'path': path,
            'new_value': final_value,
            'message': 'Wert erfolgreich aktualisiert'
        }), 200
    else:
        return jsonify({'error': f'Konnte Wert nicht setzen: {path}'}), 400

# ============================================================
# /api/post/* Endpoints - POST/PUT mit Body
# ============================================================

@app.route('/api/post/<path:path>', methods=['POST', 'PUT'])
def api_post(path):
    """
    Ändert Werte über POST/PUT Request mit JSON Body
    Beispiel: POST /api/post/state/open mit {"value": true}
    """
    try:
        data = request.get_json()
        if 'value' not in data:
            return jsonify({'error': 'value im JSON Body erforderlich'}), 400
        
        final_value = data['value']
        
        api_data = get_updated_api()
        if not api_data:
            return jsonify({'error': 'api.json not found'}), 500
        
        # Special handling für State
        if path == 'state/open':
            global keep_alive_timestamp, space_state
            old_state = space_state['open']
            space_state['open'] = bool(final_value)
            
            # Keep-Alive handling
            if space_state['open'] and not old_state:
                with keep_alive_lock:
                    keep_alive_timestamp = time.time()
                print(f"🚪 Keep-Alive aktiviert")
            elif not space_state['open'] and old_state:
                with keep_alive_lock:
                    keep_alive_timestamp = None
                print(f"🔒 Keep-Alive deaktiviert")
            elif space_state['open'] and old_state:
                with keep_alive_lock:
                    keep_alive_timestamp = time.time()
                print(f"♥️  Keep-Alive erneuert")
            
            space_state['lastchange'] = int(time.time())
            api_data['state'] = space_state
        else:
            if not set_nested_value(api_data, path, final_value):
                return jsonify({'error': f'Konnte Wert nicht setzen: {path}'}), 400
        
        save_api_config(api_data)
        
        return jsonify({
            'success': True,
            'path': path,
            'new_value': final_value,
            'message': 'Wert erfolgreich aktualisiert'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================================
# Manual Override - HTML Interface
# ============================================================

def get_manual_override_html():
    """Generiert die HTML-Seite für Manual Override"""
    authenticated = 'authenticated' in session and session['authenticated']
    
    return f'''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Space-API Manual Override</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            padding: 40px;
            max-width: 900px;
            width: 100%;
        }}
        h1 {{ color: #333; margin-bottom: 30px; text-align: center; }}
        .login-section {{ display: {('none' if authenticated else 'block')}; max-width: 400px; margin: 0 auto; }}
        .login-form {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        .login-form h2 {{ font-size: 20px; margin-bottom: 15px; }}
        .login-form input {{
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }}
        .login-form button {{
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }}
        .login-form button:hover {{ background: #764ba2; }}
        .content-section {{ display: {('block' if authenticated else 'none')}; }}
        .json-editor {{
            background: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
        }}
        textarea {{
            width: 100%;
            height: 400px;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            border: 1px solid #ddd;
            border-radius: 5px;
            resize: vertical;
        }}
        .button-group {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        button {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }}
        .btn-save {{
            background: #27ae60;
            color: white;
        }}
        .btn-save:hover {{ background: #229954; }}
        .btn-reset {{
            background: #e74c3c;
            color: white;
        }}
        .btn-reset:hover {{ background: #c0392b; }}
        .btn-logout {{
            background: #95a5a6;
            color: white;
        }}
        .btn-logout:hover {{ background: #7f8c8d; }}
        .message {{
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            display: none;
        }}
        .message.success {{
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            display: block;
        }}
        .message.error {{
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            display: block;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Space-API Manual Override</h1>
        
        <div class="login-section">
            <form class="login-form" onsubmit="handleLogin(event)">
                <h2>Anmelden</h2>
                <input type="password" id="password" placeholder="Passwort eingeben" required>
                <button type="submit">Anmelden</button>
            </form>
        </div>
        
        <div class="content-section">
            <div id="message" class="message"></div>
            
            <div class="json-editor">
                <label><strong>api.json Editor:</strong></label>
                <textarea id="jsonEditor"></textarea>
            </div>
            
            <div class="button-group">
                <button class="btn-save" onclick="handleSave()">💾 Speichern</button>
                <button class="btn-reset" onclick="handleReset()">🔄 Zurücksetzen</button>
                <button class="btn-logout" onclick="handleLogout()">🚪 Abmelden</button>
            </div>
        </div>
    </div>
    
    <script>
        function handleLogin(event) {{
            event.preventDefault();
            const password = document.getElementById('password').value;
            
            fetch('/manual-override/login', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ password }})
            }})
            .then(r => r.json())
            .then(data => {{
                if (data.success) {{
                    location.reload();
                }} else {{
                    showMessage('Falsches Passwort', 'error');
                }}
            }});
        }}
        
        function handleSave() {{
            const json = document.getElementById('jsonEditor').value;
            try {{
                JSON.parse(json);
            }} catch (e) {{
                showMessage('Ungültiges JSON: ' + e.message, 'error');
                return;
            }}
            
            fetch('/manual-override/save', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: json
            }})
            .then(r => r.json())
            .then(data => {{
                if (data.success) {{
                    showMessage('✓ Änderungen gespeichert', 'success');
                    setTimeout(() => location.reload(), 1500);
                }} else {{
                    showMessage('Fehler: ' + data.error, 'error');
                }}
            }});
        }}
        
        function handleReset() {{
            if (confirm('Wirklich zurücksetzen?')) {{
                location.reload();
            }}
        }}
        
        function handleLogout() {{
            fetch('/manual-override/logout', {{ method: 'POST' }})
            .then(() => location.reload());
        }}
        
        function showMessage(text, type) {{
            const msg = document.getElementById('message');
            msg.textContent = text;
            msg.className = 'message ' + type;
        }}
        
        // Lade JSON beim Laden
        fetch('/api.json')
        .then(r => r.json())
        .then(data => {{
            document.getElementById('jsonEditor').value = JSON.stringify(data, null, 2);
        }});
    </script>
</body>
</html>
    '''

@app.route('/manual-override', methods=['GET'])
def manual_override_page():
    """Manual Override HTML Seite"""
    return get_manual_override_html()

@app.route('/manual-override/login', methods=['POST'])
def manual_override_login():
    """Login für Manual Override"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if password == MANUAL_OVERRIDE_PASSWORD:
            session['authenticated'] = True
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Falsches Passwort'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/manual-override/logout', methods=['POST'])
def manual_override_logout():
    """Logout für Manual Override"""
    session.clear()
    return jsonify({'success': True}), 200

@app.route('/manual-override/save', methods=['POST'])
def manual_override_save():
    """Speichert die bearbeitete JSON"""
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'Nicht authentifiziert'}), 401
    
    try:
        data = request.get_json() if request.is_json else json.loads(request.data)
        if save_api_config(data):
            return jsonify({'success': True, 'message': 'Datei gespeichert'}), 200
        else:
            return jsonify({'error': 'Fehler beim Speichern'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================================
# Keep-Alive Watchdog (Background Thread)
# ============================================================

def keep_alive_watchdog():
    """Background-Thread für Keep-Alive Überwachung"""
    while True:
        time.sleep(5)
        check_keep_alive()

# ============================================================
# Server Start
# ============================================================

if __name__ == '__main__':
    # Starte Keep-Alive Watchdog
    watchdog_thread = threading.Thread(target=keep_alive_watchdog, daemon=True)
    watchdog_thread.start()
    
    print('=' * 70)
    print('🚀 Odenwilusenz Space-API Server')
    print('=' * 70)
    print(f'Start: http://localhost:8000')
    print(f'Keep-Alive Timeout: {KEEP_ALIVE_TIMEOUT}s')
    print('')
    print('📋 Endpoints:')
    print('  GET    /                         - Root ("Kein Command")')
    print('  GET    /api.json                 - SpaceAPI Standard')
    print('  GET    /api/                     - Root API ("Kein Command")')
    print('  GET    /api/get/<path>           - Wert auslesen')
    print('  GET    /api/change/<path>?value= - Wert ändern (GET Parameter)')
    print('  POST   /api/post/<path>          - Wert ändern (POST Body)')
    print('  GET    /manual-override          - Passwort-geschützte HTML Seite')
    print('')
    print('🔐 Manual Override Passwort: ' + MANUAL_OVERRIDE_PASSWORD)
    print('   (änderbar via SPACE_API_PASSWORD Umgebungsvariable)')
    print('')
    print('📌 Beispiele:')
    print('  GET  /api/get/state/open')
    print('  GET  /api/change/state/open?value=true')
    print('  POST /api/post/state/open   with {"value": true}')
    print('=' * 70)
    
    app.run(host='localhost', port=8000, debug=False)
