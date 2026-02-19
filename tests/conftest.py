"""Test Configuration and Fixtures"""

import pytest
import json
import tempfile
import os
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Set test environment
os.environ['TESTING'] = 'true'
os.environ['FLASK_SECRET_KEY'] = 'test-secret-key'
os.environ['SPACE_API_PASSWORD'] = 'test123'

from src.app import app as flask_app
from src.config import API_CONFIG_FILE

@pytest.fixture
def app():
    """Create and configure a test application instance"""
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test-secret-key'
    
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture
def sample_api_config():
    """Sample API configuration for testing"""
    return {
        "api_compatibility": ["14", "15"],
        "space": "Odenwilusenz",
        "logo": "https://odenwilusenz.ch/favicon.ico",
        "url": "https://odenwilusenz.ch",
        "location": {
            "address": "Hardmorgenweg 21, 8222 Beringen, Schweiz",
            "lon": 8.57171860,
            "lat": 47.69790250,
            "timezone": "Europe/Zurich",
            "country_code": "CH",
            "hint": "Test Space"
        },
        "state": {
            "open": False,
            "message": "Test Space",
            "lastchange": 1704067200
        },
        "contact": {
            "email": "test@example.ch",
            "issue_mail": "test@example.ch"
        },
        "sensors": {
            "temperature": [
                {
                    "value": 20.5,
                    "unit": "°C",
                    "location": "Test",
                    "name": "indoor_temperature",
                    "description": "Test Temperature",
                    "lastchange": 1704067200
                }
            ]
        }
    }
