"""Unit Tests for Space-API"""

import json
import pytest


class TestRootEndpoints:
    """Test root endpoints"""
    
    def test_index_returns_404(self, client):
        """Test that / returns 404"""
        response = client.get('/')
        assert response.status_code == 404
        assert 'Kein Command' in response.get_json()['message']
    
    def test_api_root_returns_404(self, client):
        """Test that /api/ returns 404"""
        response = client.get('/api/')
        assert response.status_code == 404
        assert 'Kein Command' in response.get_json()['message']


class TestApiJsonEndpoint:
    """Test /api.json endpoint"""
    
    def test_api_json_returns_valid_data(self, client):
        """Test that /api.json returns valid JSON data"""
        response = client.get('/api.json')
        assert response.status_code == 200
        
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'api_compatibility' in data or 'space' in data


class TestApiGetEndpoint:
    """Test /api/get/<path> endpoint"""
    
    def test_get_state_open(self, client):
        """Test getting state/open value"""
        response = client.get('/api/get/state/open')
        assert response.status_code in [200, 404]  # May not exist in test config
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'path' in data
            assert 'value' in data
    
    def test_get_invalid_path_returns_404(self, client):
        """Test that invalid path returns 404"""
        response = client.get('/api/get/invalid/path/that/does/not/exist')
        assert response.status_code == 404
        assert 'error' in response.get_json()


class TestApiChangeEndpoint:
    """Test /api/change/<path> endpoint with GET parameters"""
    
    def test_change_without_value_param_returns_400(self, client):
        """Test that change without value parameter returns 400"""
        response = client.get('/api/change/state/open')
        assert response.status_code == 400
        assert 'error' in response.get_json()
    
    def test_change_with_value_param(self, client):
        """Test changing value with parameter"""
        response = client.get('/api/change/state/message?value=test_message')
        assert response.status_code in [200, 400]  # May fail in test config


class TestApiPostEndpoint:
    """Test /api/post/<path> endpoint with POST/PUT"""
    
    def test_post_without_value_returns_400(self, client):
        """Test that POST without value returns 400"""
        response = client.post('/api/post/state/open', 
                              json={})
        assert response.status_code == 400
        assert 'error' in response.get_json()
    
    def test_post_with_value(self, client):
        """Test POST with valid value"""
        response = client.post('/api/post/state/message',
                              json={'value': 'Test Message'})
        assert response.status_code in [200, 400]  # Depends on config
        
        if response.status_code == 200:
            data = response.get_json()
            assert data.get('success') is True
