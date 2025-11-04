"""Test database operations and initialization."""

import pytest
import sqlite3
from app import init_db, get_db_connection

def test_database_initialization(client):
    """Test that the database is properly initialized with correct schema."""
    with client.application.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='job_applications'
        """)
        table_exists = cursor.fetchone()
        assert table_exists is not None
        
        # Check table schema
        cursor.execute("PRAGMA table_info(job_applications)")
        columns = cursor.fetchall()
        
        expected_columns = [
            'id', 'company_name', 'job_role', 'applied_date', 
            'url', 'status', 'notes', 'last_updated'
        ]
        
        actual_columns = [col[1] for col in columns]
        for expected_col in expected_columns:
            assert expected_col in actual_columns
        
        conn.close()

def test_database_connection(client):
    """Test database connection functionality."""
    with client.application.app_context():
        conn = get_db_connection()
        assert conn is not None
        
        # Test basic query
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM job_applications")
        count = cursor.fetchone()[0]
        assert count == 0
        
        conn.close()

def test_database_constraints(client):
    """Test database constraints and data integrity."""
    with client.application.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test that required fields cannot be NULL
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO job_applications (company_name, job_role, applied_date, status)
                VALUES (NULL, 'Test Role', '2024-01-01', 'Waiting for hearback')
            """)
        
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO job_applications (company_name, job_role, applied_date, status)
                VALUES ('Test Company', NULL, '2024-01-01', 'Waiting for hearback')
            """)
        
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO job_applications (company_name, job_role, applied_date, status)
                VALUES ('Test Company', 'Test Role', NULL, 'Waiting for hearback')
            """)
        
        conn.close()

def test_auto_increment_id(client):
    """Test that ID auto-increment works correctly."""
    with client.application.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert test data
        cursor.execute("""
            INSERT INTO job_applications (company_name, job_role, applied_date, status)
            VALUES ('Company 1', 'Role 1', '2024-01-01', 'Waiting for hearback')
        """)
        
        cursor.execute("""
            INSERT INTO job_applications (company_name, job_role, applied_date, status)
            VALUES ('Company 2', 'Role 2', '2024-01-02', 'Denied')
        """)
        
        conn.commit()
        
        # Check IDs
        cursor.execute("SELECT id FROM job_applications ORDER BY id")
        ids = [row[0] for row in cursor.fetchall()]
        assert ids == [1, 2]
        
        conn.close()

def test_default_values(client):
    """Test that default values are set correctly."""
    with client.application.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert data without status (should use default)
        cursor.execute("""
            INSERT INTO job_applications (company_name, job_role, applied_date)
            VALUES ('Test Company', 'Test Role', '2024-01-01')
        """)
        
        conn.commit()
        
        # Check default status
        cursor.execute("SELECT status FROM job_applications WHERE id = 1")
        result = cursor.fetchone()
        assert result is not None
        status = result[0]
        assert status == 'Waiting for hearback'
        
        # Check that last_updated is set
        cursor.execute("SELECT last_updated FROM job_applications WHERE id = 1")
        result = cursor.fetchone()
        assert result is not None
        last_updated = result[0]
        assert last_updated is not None
        
        conn.close()

def test_notes_field_optional(client):
    """Test that notes field is optional and can be NULL or empty."""
    with client.application.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert data without notes (should be NULL)
        cursor.execute("""
            INSERT INTO job_applications (company_name, job_role, applied_date, status)
            VALUES ('Test Company', 'Test Role', '2024-01-01', 'Waiting for hearback')
        """)
        
        # Insert data with notes
        cursor.execute("""
            INSERT INTO job_applications (company_name, job_role, applied_date, status, notes)
            VALUES ('Test Company 2', 'Test Role 2', '2024-01-02', 'Interview', 'Application ID: 12345')
        """)
        
        conn.commit()
        
        # Check that notes can be NULL
        cursor.execute("SELECT notes FROM job_applications WHERE id = 1")
        result = cursor.fetchone()
        assert result is not None
        notes = result[0]
        assert notes is None or notes == ''
        
        # Check that notes can have a value
        cursor.execute("SELECT notes FROM job_applications WHERE id = 2")
        result = cursor.fetchone()
        assert result is not None
        notes = result[0]
        assert notes == 'Application ID: 12345'
        
        conn.close()
