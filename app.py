from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# Database configuration
DATABASE = 'job_tracker.db'

def init_db():
    """Initialize the database with the required tables"""
    conn = sqlite3.connect(DATABASE)
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
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
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
def add_application():
    """Add a new job application"""
    if request.method == 'POST':
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO job_applications (company_name, job_role, applied_date, url, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['company_name'],
            data['job_role'],
            data['applied_date'],
            data['url'],
            data['status']
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Job application added successfully'})
    
    return render_template('add.html')

@app.route('/edit/<int:app_id>', methods=['GET', 'POST'])
def edit_application(app_id):
    """Edit an existing job application"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json()
        
        cursor.execute('''
            UPDATE job_applications 
            SET company_name = ?, job_role = ?, applied_date = ?, 
                url = ?, status = ?, last_updated = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data['company_name'],
            data['job_role'],
            data['applied_date'],
            data['url'],
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
def delete_application(app_id):
    """Delete a job application"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM job_applications WHERE id = ?', (app_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Job application deleted successfully'})

@app.route('/api/applications')
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
    app.run(debug=True, host='0.0.0.0', port=5000)

