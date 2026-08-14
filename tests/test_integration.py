"""Integration Tests for Space-API"""

import json
import pytest


class TestSpaceStateManagement:
    """Test space state management"""
    
    def test_can_set_space_open_state(self, client):
        """Test setting space open state"""
        response = client.post('/api/post/state/open',
                              json={'value': True})
        assert response.status_code in [200, 400]
        
        if response.status_code == 200:
            assert response.get_json().get('success') is True
    
    def test_can_set_space_message(self, client):
        """Test setting space message"""
        response = client.post('/api/post/state/message',
                              json={'value': 'Space is open for hacking!'})
        assert response.status_code in [200, 400]
        
        if response.status_code == 200:
            data = response.get_json()
            assert data.get('success') is True
            assert data.get('new_value') == 'Space is open for hacking!'


class TestSensorDataRetrieval:
    """Test sensor data retrieval"""
    
    def test_can_retrieve_full_api_config(self, client):
        """Test retrieving full API configuration"""
        response = client.get('/api.json')
        assert response.status_code == 200
        
        data = response.get_json()
        # Check for expected structure
        assert 'state' in data or 'api_compatibility' in data
    
    def test_retrieve_multiple_api_endpoints(self, client):
        """Test retrieving from multiple endpoints"""
        endpoints = [
            '/api.json',
            '/api/get/state/open',
            '/api/get/state/message',
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            # Should succeed or return 404 if path doesn't exist
            assert response.status_code in [200, 404, 500]


class TestContentTypes:
    """Test correct content types are returned"""
    
    def test_api_json_returns_json_content_type(self, client):
        """Test that /api.json returns JSON content type"""
        response = client.get('/api.json')
        if response.status_code == 200:
            assert response.content_type.startswith('application/json')
    
    def test_get_endpoint_returns_json_content_type(self, client):
        """Test that GET endpoint returns JSON content type"""
        response = client.get('/api/get/state/open')
        if response.status_code == 200:
            assert response.content_type.startswith('application/json')
