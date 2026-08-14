# 🚀 Space-API Server - Odenwilusenz

Ein vollständiger **Space-API Server** nach dem [SpaceAPI Standard](https://spaceapi.io/) für Hackerspaces und Makerspaces. Dieses Projekt stellt den Status und die Sensordaten eines Spaces über eine standardisierte REST-API bereit.

Derzeit in Einsatz beim **Odenwilusenz** in Beringen, Schweiz.

## 📋 Inhaltsverzeichnis

- [Features](#features)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [Keep-Alive System](#keep-alive-system)
- [Verwendungsbeispiele](#verwendungsbeispiele)
- [Für deinen Space konfigurieren](#für-deinen-space-konfigurieren)
- [Manual Override Interface](#manual-override-interface)
- [Sensoren](#sensoren)

---

## Was ist das?

Dieses Projekt stellt eine **REST-API nach dem SpaceAPI Standard** bereit, mit der der Zustand und die Sensordaten eines Hackerspaces oder Makerspaces abgefragt werden können.

### Features:

✅ **SpaceAPI Standard konform** - Kompatibel mit allen SpaceAPI-kompatiblen Anwendungen
✅ **Einfache Konfiguration** - Alle statischen Daten in `api.json`
✅ **Dynamische Sensordaten** - Echtzeit-Aktualisierung von Temperatur, Luftfeuchtigkeit, Stromverbrauch, etc.
✅ **API-Key Authentisierung** - Schreibzugriffe erfordern API-Key Header
✅ **State Management** - Einfaches An/Aus-Schalten des Spaces mit Nachricht
✅ **Keep-Alive System** - Automatisches Schließen des Spaces nach 30 Sekunden ohne Signal
✅ **Manual Override Interface** - Passwort-geschützte HTML Seite zur manuellen Bearbeitung

### Typische Anwendungen:

- Hackerspaces können ihren aktuellen Status veröffentlichen
- Integrationen mit Websites und Chatbots
- Monitoring und Visualisierung von Space-Daten
- Integration mit anderen Spaces durch SpaceAPI-Verzeichnisse

---

## Installation

### Voraussetzungen

- Python 3.7 oder höher
- pip (Python Package Manager)

### Schritt-für-Schritt Installation

1. **Repository klonen oder herunterladen:**
   ```bash
   git clone <repository-url>
   cd Space-API
   ```

2. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Erforderliche Umgebungsvariablen setzen:**
   ```bash
   # Linux/Mac - in ~/.bashrc oder ~/.zshrc
   export FLASK_SECRET_KEY="eine-lange-zufallszeichenkette-mindestens-32-zeichen"
   export SPACE_API_PASSWORD="dein-sicheres-admin-passwort"
   export SPACE_API_ADMIN_KEY="dein-eindeutiger-api-key-fuer-aenderungen"
   
   # Windows (PowerShell)
   $env:FLASK_SECRET_KEY="eine-lange-zufallszeichenkette-mindestens-32-zeichen"
   $env:SPACE_API_PASSWORD="dein-sicheres-admin-passwort"
   $env:SPACE_API_ADMIN_KEY="dein-eindeutiger-api-key-fuer-aenderungen"
   ```

4. **Server starten:**
   ```bash
   python main.py
   ```

5. **Server ist aktiv:**
   Der Server läuft jetzt auf `http://localhost:8000`

---

## Konfiguration

### api.json - Die Konfigurationsdatei

Die `api.json` enthält alle **statischen Informationen** über deinen Space nach dem SpaceAPI Standard. Diese Datei wird **nicht verändert** vom Script und sollte angepasst werden, um deinen Space zu beschreiben.

#### Wichtige Felder in api.json:

```json
{
  "api_compatibility": ["14", "15"],           // SpaceAPI Versionen
  "space": "Odenwilusenz",                     // Name des Spaces
  "logo": "https://...",                       // Logo URL
  "url": "https://...",                        // Website des Spaces
  "location": {
    "address": "Hardmorgenweg 21, ...",        // Physische Adresse
    "lon": 8.57171860,                         // Longitude
    "lat": 47.69790250,                        // Latitude
    "timezone": "Europe/Zurich",               // Zeitzone
    "country_code": "CH",                      // Ländercode
    "hint": "Immer am Mittwoch ab 19:00..."    // Öffnungszeiten/Hinweis
  },
  "contact": {
    "email": "mail@example.ch",                // Kontakt-E-Mail
    "issue_mail": "spaceapi@example.ch"        // Problem-Reports
  },
  "sensors": {                                 // Alle Sensoren die dein Space anbietet
  }
}
```

### Veränderbare Werte

Im `main.py` werden die folgenden Werte **dynamisch aktualisiert**:

#### 1. **State (Offen/Geschlossen)**
- `state.open` - `true` oder `false` (ob der Space offen ist)
- `state.message` - Text-Nachricht (z.B. "Space offen!", "Temporär geschlossen")
- `state.lastchange` - Zeitstempel der letzten Änderung (wird automatisch aktualisiert)

#### 2. **Sensoren - Alle `value` Felder:**

**Temperatur:**
- `sensors.temperature[0].value` - Temperatur Innen
- `sensors.temperature[1].value` - Temperatur Außen

**Luftfeuchtigkeit:**
- `sensors.humidity[0].value` - Luftfeuchtigkeit Innen
- `sensors.humidity[1].value` - Luftfeuchtigkeit Außen

**Stromverbrauch:**
- `sensors.power_consumption[0].value` - Gesamtstromverbrauch in Watt

**Netzwerk:**
- `sensors.network_connections[0].value` - Anzahl aktiver Verbindungen
- `sensors.network_traffic[0].properties.bits_per_second.value` - Download Traffic
- `sensors.network_traffic[1].properties.bits_per_second.value` - Upload Traffic

---

## Verwendung

### Server starten

```bash
python main.py
```

Ausgabe:
```
============================================================
Odenwilusenz Space-API Server
============================================================
Starting auf http://localhost:8000

Wichtige Endpoints:
  - Hauptendpoint (SpaceAPI Standard): GET http://localhost:8000/api.json
  - Admin State: GET/POST http://localhost:8000/admin/state
  - Alle Sensoren: GET http://localhost:8000/admin/all_sensors
  - Hilfe: GET http://localhost:8000/help
============================================================
```

### Endpoints testen

Mit `curl` oder einem REST-Client (z.B. Postman, Insomnia):

```bash
# Komplette API abrufen (SpaceAPI Standard)
curl http://localhost:8000/api.json

# State auslesen
curl http://localhost:8000/api/get/state/open

# Wert ändern (mit API-Key Header)
curl -X POST http://localhost:8000/api/post/state/open \
  -H "X-API-Key: dein-api-key-fuer-schreibzugriffe" \
  -H "Content-Type: application/json" \
  -d '{"value": true}'
```

---

## API Endpoints

### 📤 Haupt-Endpoint (SpaceAPI Standard)

#### `GET /api.json`
Gibt die komplette api.json mit allen aktuellen Sensordaten und State nach SpaceAPI Standard zurück.

**Beispiel Response:**
```json
{
  "api_compatibility": ["14", "15"],
  "space": "Odenwilusenz",
  "state": {
    "open": false,
    "message": "Space ist geschlossen",
    "lastchange": 1704067200
  },
  "sensors": { ... },
  ...
}
```

---

### 🎛️ Lesen von Werten (GET)

#### `GET /api/get/<path>`
Liest beliebige Werte aus der API aus. Keine Authentisierung erforderlich.

**Beispiele:**
```bash
# State auslesen
GET /api/get/state/open
Response: {"value": true}

# Temperatur auslesen
GET /api/get/sensors/temperature/0/value
Response: {"value": 22.5}
```

---

### 📝 Ändern von Werten (POST/PUT - mit Authentisierung)

#### `POST /api/post/<path>` oder `PUT /api/post/<path>`
Ändert Werte in der API. **Erforderlich: X-API-Key Header**

**Request Header:**
```
X-API-Key: dein-api-key-fuer-schreibzugriffe
Content-Type: application/json
```

**Request Body:**
```json
{
  "value": <beliebiger-wert>
}
```

**Beispiele:**

```bash
# Space öffnen
curl -X POST http://localhost:8000/api/post/state/open \
  -H "X-API-Key: dein-api-key" \
  -H "Content-Type: application/json" \
  -d '{"value": true}'

# Nachricht setzen
curl -X POST http://localhost:8000/api/post/state/message \
  -H "X-API-Key: dein-api-key" \
  -H "Content-Type: application/json" \
  -d '{"value": "Space ist offen!"}'

# Temperatur aktualisieren
curl -X POST http://localhost:8000/api/post/sensors/temperature/0/value \
  -H "X-API-Key: dein-api-key" \
  -H "Content-Type: application/json" \
  -d '{"value": 23.5}'
```

**Response (erfolgreich):**
```json
{
  "success": true,
  "path": "state/open",
  "new_value": true,
  "message": "Wert erfolgreich aktualisiert"
}
```

**Response (Fehler - fehlender API-Key):**
```json
{
  "error": "Unauthorized - X-API-Key Header erforderlich"
}
```

---

### 🔐 Manual Override (Passwort-geschützte Web-Interface)

#### `GET /manual-override`
Zeigt ein passwort-geschütztes HTML-Interface zum manuellen Bearbeiten der api.json.

**Verwendung:**
1. Browser zu `http://localhost:8000/manual-override` navigieren
2. Mit SPACE_API_PASSWORD anmelden
3. JSON editieren und speichern

#### `POST /manual-override/login`
Login für Manual Override Session.

**Request:**
```json
{
  "password": "dein-admin-passwort"
}
```

**Response (erfolgreich):**
```json
{
  "success": true,
  "csrf_token": "..."
}
```

#### `POST /manual-override/save`
Speichert die editierte JSON (mit CSRF-Schutz).

**Request Header:**
```
X-CSRF-Token: <csrf-token-von-login>
Content-Type: application/json
```

**Request Body:** Die komplette api.json mit Änderungen

---

### ℹ️ Info Endpoints

#### `GET /`
Zeigt "Kein Command".

#### `GET /api/`
Zeigt "Kein Command".

---

## Beispiele

### Beispiel 1: Space-Status auf der Website anzeigen

**JavaScript/HTML:**
```javascript
fetch('http://localhost:8000/api.json')
  .then(response => response.json())
  .then(data => {
    const statusDiv = document.getElementById('space-status');
    if (data.state.open) {
      statusDiv.innerHTML = `<h2 style="color: green;">✓ Space ist offen!</h2>`;
    } else {
      statusDiv.innerHTML = `<h2 style="color: red;">✗ Space ist geschlossen</h2>
        <p>${data.state.message}</p>`;
    }
  });
```

---

### Beispiel 2: Space-Status über einen Bot ändern

**Python Script:**
```python
import requests
import json

# Space öffnen
response = requests.post(
    'http://localhost:8000/admin/state',
    json={
        'open': True,
        'message': 'Space geöffnet durch Bot!'
    }
)
print(response.json())

# Temperatur aktualisieren
response = requests.post(
    'http://localhost:8000/admin/sensors/temperature/indoor',
    json={'value': 22.5}
)
print(response.json())
```

---

### Beispiel 3: Alle Daten abrufen und anzeigen

**Python Script:**
```python
import requests

# Komplette API abrufen
response = requests.get('http://localhost:8000/api.json')
data = response.json()

print(f"Space: {data['space']}")
print(f"Status: {'Offen' if data['state']['open'] else 'Geschlossen'}")
print(f"Nachricht: {data['state']['message']}")
print(f"\nSensoren:")
print(f"  Innentemp: {data['sensors']['temperature'][0]['value']}°C")
print(f"  Luftfeuchtigkeit: {data['sensors']['humidity'][0]['value']}%")
print(f"  Stromverbrauch: {data['sensors']['power_consumption'][0]['value']}W")
```

---

## Für den eigenen Space anpassen

### Schritt 1: api.json konfigurieren

Bearbeite die `api.json` und passe folgende Werte an:

```json
{
  "space": "Dein Space Name",
  "logo": "https://example.com/logo.png",
  "url": "https://example.com",
  "location": {
    "address": "Deine Adresse",
    "lon": 8.5,              // Deine Longitude
    "lat": 47.5,             // Deine Latitude
    "timezone": "Europe/Zurich",  // Deine Zeitzone
    "country_code": "CH",    // Ländercode
    "hint": "Öffnungszeiten..."
  },
  "contact": {
    "email": "dein-email@example.com",
    "issue_mail": "probleme@example.com"
  }
}
```

### Schritt 2: Sensoren anpassen

Wenn dein Space andere Sensoren hat, bearbeite die `sensors` Section in der `api.json`:
- Entferne nicht benötigte Sensoren
- Füge neue Sensoren hinzu
- Passe Namen, Beschreibungen und Einheiten an

### Schritt 3: main.py anpassen

Wenn neue Sensoren hinzugefügt werden, müssen auch neue `POST/GET` Endpoints in `main.py` hinzugefügt werden:

```python
@app.route('/admin/sensors/my_custom_sensor', methods=['GET', 'POST'])
def manage_custom_sensor():
    """Mein Custom Sensor"""
    if request.method == 'GET':
        return jsonify({
            'value': sensor_data['my_sensor'],
            'unit': 'MY_UNIT'
        }), 200
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if 'value' in data:
                sensor_data['my_sensor'] = float(data['value'])
            return jsonify({
                'success': True,
                'new_value': sensor_data['my_sensor']
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
```

---

## Sicherheitshinweise

⚠️ **Wichtig für Produktivbetrieb:**

1. **Authentifizierung hinzufügen** - Der aktuelle Admin-Endpoints haben keine Authentifizierung. Für Produktivbetrieb sollte eine API-Key oder OAuth2 hinzugefügt werden.

2. **HTTPS verwenden** - In Produktion sollte HTTPS über einen Reverse-Proxy (z.B. Nginx) verwendet werden.

3. **Port ändern** - Standard ist `localhost:8000`, für externe Zugriffe auf einen anderen Port mappen.

4. **CORS konfigurieren** - Bei Bedarf können CORS-Header konfiguriert werden.

Beispiel für Authentifizierung:
```python
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != 'dein-geheimschluessel':
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/admin/state', methods=['POST'])
@require_api_key
def manage_state():
    # ... Code hier
```

---

## Weitere Ressourcen

- **SpaceAPI Dokumentation:** https://spaceapi.io/
- **SpaceAPI Directory:** https://directory.spaceapi.io/
- **Flask Dokumentation:** https://flask.palletsprojects.com/

---

## License & Kontakt

Entwickelt für **Odenwilusenz** (https://odenwilusenz.ch)

Fragen oder Probleme? Kontaktiere: spaceapi@justsomeone.ch