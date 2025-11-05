"""Test summary statistics endpoint."""

import pytest
import json
from conftest import insert_test_data

def test_api_summary_empty_database(client):
    """Test summary endpoint with empty database."""
    response = client.get('/api/summary')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['total'] == 0
    assert data['by_status'] == {}

def test_api_summary_single_application(client, sample_data):
    """Test summary endpoint with single application."""
    # Add one application
    client.post('/add', json=sample_data, content_type='application/json')
    
    response = client.get('/api/summary')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['total'] == 1
    assert data['by_status']['Applied'] == 1

def test_api_summary_multiple_applications(client, multiple_applications):
    """Test summary endpoint with multiple applications."""
    insert_test_data(client, multiple_applications)
    
    response = client.get('/api/summary')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['total'] == 4
    assert data['by_status']['Applied'] == 1
    assert data['by_status']['Denied without interview (visa related)'] == 1
    assert data['by_status']['Interview 1'] == 1
    assert data['by_status']['Offer'] == 1

def test_api_summary_after_deletion(client, multiple_applications):
    """Test summary endpoint after deleting applications."""
    insert_test_data(client, multiple_applications)
    
    # Delete one application
    client.post('/delete/1')
    
    response = client.get('/api/summary')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['total'] == 3  # One less than before

def test_api_summary_after_edit(client, sample_data):
    """Test summary endpoint after editing application status."""
    # Add application
    client.post('/add', json=sample_data, content_type='application/json')
    
    # Edit status
    updated_data = sample_data.copy()
    updated_data['status'] = 'Interview 1'
    client.post('/edit/1', json=updated_data, content_type='application/json')
    
    response = client.get('/api/summary')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['total'] == 1
    assert 'Applied' not in data['by_status'] or data['by_status'].get('Applied', 0) == 0
    assert data['by_status']['Interview 1'] == 1

def test_api_summary_all_status_types(client):
    """Test summary endpoint with all status types."""
    statuses = [
        'Applied',
        'Denied without interview (visa related)',
        'Denied without interview (non-visa related)',
        'Interview 1',
        'Interview 2',
        'Interview 3',
        'Offer'
    ]
    
    # Add applications with each status
    for i, status in enumerate(statuses):
        data = {
            'company_name': f'Company {i+1}',
            'job_role': f'Role {i+1}',
            'applied_date': '2024-01-01',
            'status': status
        }
        client.post('/add', json=data, content_type='application/json')
    
    response = client.get('/api/summary')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['total'] == 7
    
    # Check all statuses are present
    for status in statuses:
        assert data['by_status'][status] == 1

def test_api_summary_multiple_same_status(client):
    """Test summary endpoint with multiple applications of same status."""
    # Add multiple applications with same status
    for i in range(3):
        data = {
            'company_name': f'Company {i+1}',
            'job_role': f'Role {i+1}',
            'applied_date': '2024-01-01',
            'status': 'Applied'
        }
        client.post('/add', json=data, content_type='application/json')
    
    response = client.get('/api/summary')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['total'] == 3
    assert data['by_status']['Applied'] == 3

def test_api_summary_response_format(client, multiple_applications):
    """Test that summary response has correct format."""
    insert_test_data(client, multiple_applications)
    
    response = client.get('/api/summary')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    
    # Check response structure
    assert 'total' in data
    assert 'by_status' in data
    assert isinstance(data['total'], int)
    assert isinstance(data['by_status'], dict)
    
    # Check that all status counts are integers
    for status, count in data['by_status'].items():
        assert isinstance(count, int)
        assert count > 0

def test_api_summary_consistency_with_applications(client, multiple_applications):
    """Test that summary is consistent with applications endpoint."""
    insert_test_data(client, multiple_applications)
    
    # Get applications
    apps_response = client.get('/api/applications')
    apps_data = json.loads(apps_response.data)
    
    # Get summary
    summary_response = client.get('/api/summary')
    summary_data = json.loads(summary_response.data)
    
    # Check consistency
    assert len(apps_data) == summary_data['total']
    
    # Count statuses manually
    status_counts = {}
    for app in apps_data:
        status = app['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Compare with summary
    assert status_counts == summary_data['by_status']
