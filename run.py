#!/usr/bin/env python
"""
Space-API Server Entry Point
"""

import threading
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.app import app, keep_alive_watchdog
from src.config import HOST, PORT, DEBUG, KEEP_ALIVE_TIMEOUT, SPACE_API_PASSWORD

def main():
    """Start the Space-API Server"""
    
    # Starte Keep-Alive Watchdog
    watchdog_thread = threading.Thread(target=keep_alive_watchdog, daemon=True)
    watchdog_thread.start()
    
    print('=' * 70)
    print('🚀 Odenwilusenz Space-API Server')
    print('=' * 70)
    print(f'Start: http://{HOST}:{PORT}')
    print(f'Keep-Alive Timeout: {KEEP_ALIVE_TIMEOUT}s')
    print(f'Debug: {DEBUG}')
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
    print('🔐 Manual Override Passwort: ' + SPACE_API_PASSWORD)
    print('')
    print('📌 Beispiele:')
    print('  GET  /api/get/state/open')
    print('  GET  /api/change/state/open?value=true')
    print('  POST /api/post/state/open   with {"value": true}')
    print('=' * 70)
    
    app.run(host=HOST, port=PORT, debug=DEBUG)

if __name__ == '__main__':
    main()
