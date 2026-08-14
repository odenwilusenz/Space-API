"""
Space-API Configuration
Lädt Einstellungen aus Umgebungsvariablen
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Flask Configuration
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
HOST = os.environ.get('FLASK_HOST', 'localhost')
PORT = int(os.environ.get('FLASK_PORT', '8000'))
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'space-api-secret-key-change-in-production')

# Space-API Configuration
KEEP_ALIVE_TIMEOUT = int(os.environ.get('KEEP_ALIVE_TIMEOUT', '30'))
SPACE_API_PASSWORD = os.environ.get('SPACE_API_PASSWORD', 'admin123')

# API Config File Path
API_CONFIG_FILE = BASE_DIR / 'api.json'

# Logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
