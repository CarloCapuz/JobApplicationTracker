import pytest
import os
import tempfile
import sqlite3
from app import app, init_db, get_db_connection

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    # Store original database path
    original_db = app.config.get('DATABASE', 'job_tracker.db')
    
    # Set test database
    app.config['DATABASE'] = db_path
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
    
    # Clean up
    os.close(db_fd)
    os.unlink(db_path)
    
    # Restore original database path
    app.config['DATABASE'] = original_db

@pytest.fixture
def sample_data():
    """Sample job application data for testing."""
    return {
        'company_name': 'Test Company',
        'job_role': 'Software Engineer',
        'applied_date': '2024-01-15',
        'url': 'https://example.com/job',
        'status': 'Waiting for hearback'
    }

@pytest.fixture
def multiple_applications():
    """Multiple job applications for testing."""
    return [
        {
            'company_name': 'Company A',
            'job_role': 'Developer',
            'applied_date': '2024-01-01',
            'url': 'https://company-a.com/job',
            'status': 'Waiting for hearback'
        },
        {
            'company_name': 'Company B',
            'job_role': 'Engineer',
            'applied_date': '2024-01-02',
            'url': 'https://company-b.com/job',
            'status': 'Denied'
        },
        {
            'company_name': 'Company C',
            'job_role': 'Analyst',
            'applied_date': '2024-01-03',
            'url': 'https://company-c.com/job',
            'status': 'Interview'
        },
        {
            'company_name': 'Company D',
            'job_role': 'Manager',
            'applied_date': '2024-01-04',
            'url': 'https://company-d.com/job',
            'status': 'Offer'
        }
    ]

def insert_test_data(client, applications):
    """Helper function to insert test data into the database."""
    for app_data in applications:
        response = client.post('/add', 
                             json=app_data,
                             content_type='application/json')
        assert response.status_code == 200
