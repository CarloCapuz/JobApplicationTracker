"""Test API endpoints and CRUD operations."""

import pytest
import json
from conftest import insert_test_data

def test_index_page(client):
    """Test that the main page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Job Application Tracker' in response.data

def test_add_application_get(client):
    """Test GET request to add application page."""
    response = client.get('/add')
    assert response.status_code == 200
    assert b'Add New Job Application' in response.data

def test_add_application_post_success(client, sample_data):
    """Test successful POST request to add application."""
    response = client.post('/add', 
                         json=sample_data,
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'successfully' in data['message']

def test_add_application_post_missing_fields(client):
    """Test POST request with missing required fields."""
    incomplete_data = {
        'company_name': 'Test Company',
        'job_role': 'Test Role'
        # Missing applied_date and status
    }
    
    response = client.post('/add', 
                         json=incomplete_data,
                         content_type='application/json')
    
    # Should return 400 for missing required fields
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'Missing required fields' in data['message']

def test_add_application_post_invalid_data(client):
    """Test POST request with invalid data."""
    invalid_data = {
        'company_name': '',  # Empty company name
        'job_role': 'Test Role',
        'applied_date': '2024-01-01',
        'status': 'Invalid Status'
    }
    
    response = client.post('/add', 
                         json=invalid_data,
                         content_type='application/json')
    
    # Should return 400 for empty required fields
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False

def test_edit_application_get(client, sample_data):
    """Test GET request to edit application page."""
    # First add an application
    response = client.post('/add', json=sample_data, content_type='application/json')
    assert response.status_code == 200
    
    # Then try to edit it
    response = client.get('/edit/1')
    assert response.status_code == 200
    assert b'Edit Job Application' in response.data

def test_edit_application_get_nonexistent(client):
    """Test GET request to edit non-existent application."""
    response = client.get('/edit/999')
    assert response.status_code == 302  # Redirect to index

def test_edit_application_post_success(client, sample_data):
    """Test successful POST request to edit application."""
    # First add an application
    client.post('/add', json=sample_data, content_type='application/json')
    
    # Then edit it
    updated_data = sample_data.copy()
    updated_data['status'] = 'Interview'
    
    response = client.post('/edit/1', 
                         json=updated_data,
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

def test_delete_application_success(client, sample_data):
    """Test successful DELETE request."""
    # First add an application
    client.post('/add', json=sample_data, content_type='application/json')
    
    # Then delete it
    response = client.post('/delete/1')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

def test_delete_application_nonexistent(client):
    """Test DELETE request for non-existent application."""
    response = client.post('/delete/999')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True  # Should still return success

def test_api_applications_endpoint(client, multiple_applications):
    """Test the API applications endpoint."""
    # Insert test data
    insert_test_data(client, multiple_applications)
    
    # Test default sorting
    response = client.get('/api/applications')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert len(data) == 4
    assert data[0]['company_name'] == 'Company D'  # Should be sorted by applied_date desc

def test_api_applications_endpoint_sorting(client, multiple_applications):
    """Test API applications endpoint with different sorting options."""
    insert_test_data(client, multiple_applications)
    
    # Test sorting by company name
    response = client.get('/api/applications?sort=company_name&order=asc')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    company_names = [app['company_name'] for app in data]
    assert company_names == ['Company A', 'Company B', 'Company C', 'Company D']

def test_api_applications_endpoint_invalid_sort(client, multiple_applications):
    """Test API applications endpoint with invalid sort parameters."""
    insert_test_data(client, multiple_applications)
    
    # Test with invalid sort parameter
    response = client.get('/api/applications?sort=invalid_field&order=asc')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert len(data) == 4  # Should still return data with default sorting

def test_api_applications_endpoint_invalid_order(client, multiple_applications):
    """Test API applications endpoint with invalid order parameter."""
    insert_test_data(client, multiple_applications)
    
    # Test with invalid order parameter
    response = client.get('/api/applications?sort=company_name&order=invalid')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert len(data) == 4  # Should still return data with default order

def test_add_application_with_url(client):
    """Test adding application with URL."""
    data_with_url = {
        'company_name': 'Test Company',
        'job_role': 'Test Role',
        'applied_date': '2024-01-01',
        'url': 'https://example.com/job',
        'status': 'Waiting for hearback'
    }
    
    response = client.post('/add', 
                         json=data_with_url,
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

def test_add_application_without_url(client):
    """Test adding application without URL."""
    data_without_url = {
        'company_name': 'Test Company',
        'job_role': 'Test Role',
        'applied_date': '2024-01-01',
        'status': 'Waiting for hearback'
        # URL field is optional and will be handled by data.get('url', '')
    }
    
    response = client.post('/add', 
                         json=data_without_url,
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

def test_all_status_values(client):
    """Test adding applications with all possible status values."""
    statuses = [
        'Waiting for hearback',
        'Denied',
        'Interview',
        'Interview 2',
        'Interview 3',
        'Offer'
    ]
    
    for i, status in enumerate(statuses):
        data = {
            'company_name': f'Company {i+1}',
            'job_role': f'Role {i+1}',
            'applied_date': '2024-01-01',
            'status': status
            # URL is optional, will default to empty string
        }
        
        response = client.post('/add', 
                             json=data,
                             content_type='application/json')
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True

def test_add_application_with_notes(client):
    """Test adding application with notes field."""
    data_with_notes = {
        'company_name': 'Test Company',
        'job_role': 'Test Role',
        'applied_date': '2024-01-01',
        'status': 'Waiting for hearback',
        'notes': 'Application ID: 12345\nConfirmation: ABC123'
    }
    
    response = client.post('/add', 
                         json=data_with_notes,
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    
    # Verify notes are stored and returned
    api_response = client.get('/api/applications')
    assert api_response.status_code == 200
    apps = json.loads(api_response.data)
    assert len(apps) == 1
    assert apps[0]['notes'] == 'Application ID: 12345\nConfirmation: ABC123'

def test_add_application_without_notes(client):
    """Test adding application without notes field (should default to empty string)."""
    data_without_notes = {
        'company_name': 'Test Company',
        'job_role': 'Test Role',
        'applied_date': '2024-01-01',
        'status': 'Waiting for hearback'
    }
    
    response = client.post('/add', 
                         json=data_without_notes,
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    
    # Verify notes field exists but is empty
    api_response = client.get('/api/applications')
    assert api_response.status_code == 200
    apps = json.loads(api_response.data)
    assert len(apps) == 1
    assert apps[0].get('notes', '') == ''

def test_edit_application_with_notes(client, sample_data):
    """Test editing application to add/update notes."""
    # First add an application
    client.post('/add', json=sample_data, content_type='application/json')
    
    # Then edit it with new notes
    updated_data = sample_data.copy()
    updated_data['notes'] = 'Updated notes: Interview scheduled for next week'
    
    response = client.post('/edit/1', 
                         json=updated_data,
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    
    # Verify notes were updated
    api_response = client.get('/api/applications')
    assert api_response.status_code == 200
    apps = json.loads(api_response.data)
    assert apps[0]['notes'] == 'Updated notes: Interview scheduled for next week'

def test_api_applications_includes_notes(client, sample_data):
    """Test that API applications endpoint includes notes field."""
    client.post('/add', json=sample_data, content_type='application/json')
    
    response = client.get('/api/applications')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert len(data) == 1
    assert 'notes' in data[0]
    assert data[0]['notes'] == 'Test notes field'