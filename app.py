from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv
import hashlib

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Database configuration
DATABASE = 'job_tracker.db'

# Simple User class for authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_credentials(username, password):
    """Verify user credentials against environment variables"""
    expected_username = os.getenv('FLASK_USERNAME')
    expected_password = os.getenv('FLASK_PASSWORD')
    
    if not expected_username or not expected_password:
        return False
    
    return username == expected_username and hash_password(password) == hash_password(expected_password)

def init_db():
    """Initialize the database with the required tables"""
    db_path = app.config.get('DATABASE', DATABASE)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            job_role TEXT NOT NULL,
            applied_date DATE NOT NULL,
            url TEXT,
            status TEXT NOT NULL DEFAULT 'Waiting for hearback',
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    db_path = app.config.get('DATABASE', DATABASE)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if verify_credentials(username, password):
            user = User(username)
            login_user(user)
            flash('Successfully logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Main page showing all job applications"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get sort parameter
    sort_by = request.args.get('sort', 'applied_date')
    sort_order = request.args.get('order', 'desc')
    
    # Validate sort parameters
    valid_sorts = ['company_name', 'job_role', 'applied_date', 'status', 'last_updated']
    if sort_by not in valid_sorts:
        sort_by = 'applied_date'
    
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    query = f'''
        SELECT * FROM job_applications 
        ORDER BY {sort_by} {sort_order.upper()}
    '''
    
    applications = cursor.execute(query).fetchall()
    conn.close()
    
    return render_template('index.html', applications=applications, 
                         current_sort=sort_by, current_order=sort_order)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_application():
    """Add a new job application"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company_name', 'job_role', 'applied_date', 'status']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return jsonify({'success': False, 'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO job_applications (company_name, job_role, applied_date, url, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['company_name'],
            data['job_role'],
            data['applied_date'],
            data.get('url', ''),  # Use empty string if URL not provided
            data['status']
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Job application added successfully'})
    
    return render_template('add.html')

@app.route('/edit/<int:app_id>', methods=['GET', 'POST'])
@login_required
def edit_application(app_id):
    """Edit an existing job application"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company_name', 'job_role', 'applied_date', 'status']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return jsonify({'success': False, 'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        cursor.execute('''
            UPDATE job_applications 
            SET company_name = ?, job_role = ?, applied_date = ?, 
                url = ?, status = ?, last_updated = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data['company_name'],
            data['job_role'],
            data['applied_date'],
            data.get('url', ''),  # Use empty string if URL not provided
            data['status'],
            app_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Job application updated successfully'})
    
    # GET request - fetch application data
    application = cursor.execute('SELECT * FROM job_applications WHERE id = ?', (app_id,)).fetchone()
    conn.close()
    
    if not application:
        return redirect(url_for('index'))
    
    return render_template('edit.html', application=application)

@app.route('/delete/<int:app_id>', methods=['POST'])
@login_required
def delete_application(app_id):
    """Delete a job application"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM job_applications WHERE id = ?', (app_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Job application deleted successfully'})

@app.route('/api/applications')
@login_required
def api_applications():
    """API endpoint to get all applications as JSON"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sort_by = request.args.get('sort', 'applied_date')
    sort_order = request.args.get('order', 'desc')
    
    valid_sorts = ['company_name', 'job_role', 'applied_date', 'status', 'last_updated']
    if sort_by not in valid_sorts:
        sort_by = 'applied_date'
    
    if sort_order not in ['asc', 'desc']:
        sort_order = 'desc'
    
    query = f'''
        SELECT * FROM job_applications 
        ORDER BY {sort_by} {sort_order.upper()}
    '''
    
    applications = cursor.execute(query).fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    apps_list = []
    for app in applications:
        apps_list.append({
            'id': app['id'],
            'company_name': app['company_name'],
            'job_role': app['job_role'],
            'applied_date': app['applied_date'],
            'url': app['url'],
            'status': app['status'],
            'last_updated': app['last_updated']
        })
    
    return jsonify(apps_list)

@app.route('/api/summary')
@login_required
def api_summary():
    """API endpoint to get job application summary statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get total count
    total_count = cursor.execute('SELECT COUNT(*) FROM job_applications').fetchone()[0]
    
    # Get counts by status
    status_counts = cursor.execute('''
        SELECT status, COUNT(*) as count 
        FROM job_applications 
        GROUP BY status
    ''').fetchall()
    
    conn.close()
    
    # Convert to dictionary
    summary = {
        'total': total_count,
        'by_status': {}
    }
    
    for status, count in status_counts:
        summary['by_status'][status] = count
    
    return jsonify(summary)

if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)

