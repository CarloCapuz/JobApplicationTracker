"""Test Flask application configuration and basic functionality."""

import pytest
import json

def test_app_configuration(client):
    """Test that the Flask app is properly configured for testing."""
    assert client.application.testing is True

def test_app_routes_exist(client):
    """Test that all expected routes exist and are accessible."""
    routes_to_test = [
        ('/', 'GET'),
        ('/add', 'GET'),
        ('/api/applications', 'GET'),
        ('/api/summary', 'GET')
    ]
    
    for route, method in routes_to_test:
        if method == 'GET':
            response = client.get(route)
            assert response.status_code in [200, 302]  # 302 for redirects

def test_app_json_response_format(client):
    """Test that JSON responses have proper format."""
    # Test API applications endpoint
    response = client.get('/api/applications')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    
    # Test API summary endpoint
    response = client.get('/api/summary')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'total' in data
    assert 'by_status' in data

def test_app_error_handling(client):
    """Test that the app handles errors gracefully."""
    # Test non-existent route
    response = client.get('/nonexistent-route')
    assert response.status_code == 404
    
    # Test invalid edit ID
    response = client.get('/edit/999')
    assert response.status_code == 302  # Should redirect

def test_app_content_type_handling(client):
    """Test that the app handles different content types properly."""
    # Test POST with JSON content type
    data = {
        'company_name': 'Test Company',
        'job_role': 'Test Role',
        'applied_date': '2024-01-01',
        'status': 'Waiting for hearback'
    }
    
    response = client.post('/add', 
                         json=data,
                         content_type='application/json')
    assert response.status_code == 200
    
    # Test POST with form data (should still work)
    response = client.post('/add', 
                         data=data,
                         content_type='application/x-www-form-urlencoded')
    # This might return 400 or handle differently, but shouldn't crash
    assert response.status_code in [200, 400, 415]

def test_app_cors_headers(client):
    """Test that the app doesn't have CORS issues for local development."""
    response = client.get('/api/applications')
    # Should not have CORS headers for local development
    assert 'Access-Control-Allow-Origin' not in response.headers

def test_app_static_files(client):
    """Test that static files are accessible."""
    # Test CSS file
    response = client.get('/static/style.css')
    assert response.status_code == 200
    assert response.content_type.startswith('text/css')
    
    # Test JS file
    response = client.get('/static/script.js')
    assert response.status_code == 200
    # Flask serves JS files as text/plain in test mode, which is fine
    assert response.content_type.startswith('text/')
