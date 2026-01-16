# Space-API - Odenwilusenz

Ein vollständiger **Space-API Server** nach dem [SpaceAPI Standard](https://spaceapi.io/) für Hackerspaces und Makerspaces. Dieses Projekt ermöglicht es, den Status und die Sensordaten eines Spaces über eine standardisierte REST-API bereitzustellen. Zurzeit in Einsatz beim Odenwilusenz in Beringen.

## 📋 Inhaltsverzeichnis

- [Was ist das?](#was-ist-das)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Verwendung](#verwendung)
- [API Endpoints](#api-endpoints)
- [Beispiele](#beispiele)
- [Für den eigenen Space anpassen](#für-den-eigenen-space-anpassen)

---

## Was ist das?

Dieses Projekt stellt eine **REST-API nach dem SpaceAPI Standard** bereit, mit der der Zustand und die Sensordaten eines Hackerspaces oder Makerspaces abgefragt werden können.

### Features:

✅ **SpaceAPI Standard konform** - Kompatibel mit allen SpaceAPI-kompatiblen Anwendungen
✅ **Einfache Konfiguration** - Alle statischen Daten in `api.json`
✅ **Dynamische Sensordaten** - Echtzeit-Aktualisierung von Temperatur, Luftfeuchtigkeit, Stromverbrauch, etc.
✅ **Admin-Interface** - Einfache Endpoints zum Aktualisieren von Sensordaten
✅ **State Management** - Einfaches An/Aus-Schalten des Spaces mit Nachricht
✅ **Keine Datenbankabhängigkeit** - Läuft mit reiner Flask-Anwendung

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

2. **Flask installieren:**
   ```bash
   pip install flask
   ```

3. **Server starten:**
   ```bash
   python main.py
   ```

4. **Server ist aktiv:**
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
# Komplette API abrufen
curl http://localhost:8000/api.json

# Aktuellen State abrufen
curl http://localhost:8000/admin/state

# Alle Sensoren abrufen
curl http://localhost:8000/admin/all_sensors

# Hilfe anzeigen
curl http://localhost:8000/help
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

### 🎛️ State Management

#### `GET /admin/state`
Gibt den aktuellen State des Spaces zurück.

**Response:**
```json
{
  "open": false,
  "message": "Space ist geschlossen",
  "lastchange": 1704067200
}
```

#### `POST /admin/state`
Aktualisiert den State (offen/geschlossen) und die Nachricht.

**Request Body:**
```json
{
  "open": true,
  "message": "Space offen!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "State erfolgreich aktualisiert",
  "new_state": {
    "open": true,
    "message": "Space offen!",
    "lastchange": 1704067200
  }
}
```

---

### 🌡️ Sensor Endpoints

#### Temperature

**`GET /admin/sensors/temperature/indoor`** - Innentemperatur auslesen
**`POST /admin/sensors/temperature/indoor`** - Innentemperatur setzen

**`GET /admin/sensors/temperature/outdoor`** - Außentemperatur auslesen
**`POST /admin/sensors/temperature/outdoor`** - Außentemperatur setzen

**Request Body für POST:**
```json
{ "value": 22.5 }
```

---

#### Humidity (Luftfeuchtigkeit)

**`GET /admin/sensors/humidity/indoor`** - Innenluftfeuchtigkeit auslesen
**`POST /admin/sensors/humidity/indoor`** - Innenluftfeuchtigkeit setzen

**`GET /admin/sensors/humidity/outdoor`** - Außenluftfeuchtigkeit auslesen
**`POST /admin/sensors/humidity/outdoor`** - Außenluftfeuchtigkeit setzen

**Request Body für POST:**
```json
{ "value": 55 }
```

---

#### Power (Stromverbrauch)

**`GET /admin/sensors/power`** - Stromverbrauch auslesen
**`POST /admin/sensors/power`** - Stromverbrauch setzen

**Request Body für POST:**
```json
{ "value": 3000 }
```

---

#### Network Connections

**`GET /admin/sensors/network/connections`** - Anzahl Netzwerkverbindungen auslesen
**`POST /admin/sensors/network/connections`** - Anzahl setzen

**Request Body für POST:**
```json
{ "value": 12 }
```

---

#### Network Traffic

**`GET /admin/sensors/network/traffic/download`** - Download-Traffic auslesen
**`POST /admin/sensors/network/traffic/download`** - Download-Traffic setzen

**`GET /admin/sensors/network/traffic/upload`** - Upload-Traffic auslesen
**`POST /admin/sensors/network/traffic/upload`** - Upload-Traffic setzen

**Request Body für POST:**
```json
{ "value": 150000 }
```

---

#### Alle Sensoren

**`GET /admin/all_sensors`** - Gibt alle Sensordaten auf einmal zurück

**Response:**
```json
{
  "temperature": {
    "indoor": 20.5,
    "outdoor": 15.2
  },
  "humidity": {
    "indoor": 45,
    "outdoor": 60
  },
  "power_consumption": 2500,
  "network_connections": 8,
  "network_traffic": {
    "download": 125000,
    "upload": 45000
  }
}
```

---

### ℹ️ Info Endpoints

#### `GET /`
Zeigt eine Übersicht der verfügbaren Endpoints.

#### `GET /help`
Zeigt eine detaillierte Dokumentation aller Endpoints.

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