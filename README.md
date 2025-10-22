# Job Application Tracker

A personal desktop web application for tracking job applications with a modern dark mode interface.

## Features

- **Add Job Applications**: Track company name, job role, applied date, URL, and status
- **Status Tracking**: Monitor applications through different stages:
  - Waiting for hearback
  - Denied
  - Interview
  - Interview 2
  - Interview 3
  - Offer
- **Sorting**: Sort applications by company name, job role, applied date, status, or last updated date
- **Edit/Delete**: Update or remove existing applications
- **Dark Mode**: Modern, easy-on-the-eyes dark theme
- **Responsive Design**: Works on desktop and mobile devices
- **Local Storage**: Data stored in SQLite database locally

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom dark mode CSS

## Installation

1. **Clone or download** this project to your local machine

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Testing

The project includes comprehensive unit tests to ensure reliability and maintainability.

### Running Tests

**Run all tests:**
```bash
python -m pytest
```

**Run tests with coverage report:**
```bash
python -m pytest --cov=app --cov-report=html
```

**Run specific test files:**
```bash
python -m pytest tests/test_database.py
python -m pytest tests/test_api.py
python -m pytest tests/test_summary.py
```

**Use the test runner script:**
```bash
python run_tests.py all        # Run all tests
python run_tests.py unit       # Run unit tests only
python run_tests.py integration # Run integration tests only
python run_tests.py quick      # Run tests with quick failure mode
```

### Test Coverage

The test suite covers:
- **Database Operations**: Schema creation, constraints, data integrity
- **API Endpoints**: CRUD operations, error handling, data validation
- **Summary Statistics**: Accurate counting and aggregation
- **Edge Cases**: Invalid data, missing fields, non-existent records

### Test Structure

```
tests/
├── conftest.py          # Test configuration and fixtures
├── test_database.py     # Database operation tests
├── test_api.py          # API endpoint tests
└── test_summary.py      # Summary statistics tests
```

### Test Configuration

Tests use a temporary SQLite database to ensure isolation and prevent data corruption. Each test runs in a clean environment with its own database instance.

## Usage

### Adding a New Application
1. Click "Add New Application" button
2. Fill in the required fields:
   - Company Name
   - Job Role
   - Applied Date (use the date picker)
   - Job URL (optional)
   - Status (select from radio buttons)
3. Click "Add Application"

### Managing Applications
- **View All**: See all applications in a card-based layout
- **Sort**: Use the sort dropdowns to organize by different criteria
- **Edit**: Click "Edit" on any application card to modify details
- **Delete**: Click "Delete" to remove an application (with confirmation)

### Keyboard Shortcuts
- `Ctrl/Cmd + N`: Add new application
- `Escape`: Return to main list

## File Structure

```
Tracker/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── job_tracker.db         # SQLite database (created automatically)
├── templates/             # HTML templates
│   ├── index.html        # Main application list
│   ├── add.html          # Add new application form
│   └── edit.html         # Edit application form
└── static/               # Static assets
    ├── style.css         # Dark mode styling
    └── script.js         # JavaScript functionality
```

## Database Schema

The application uses a SQLite database with the following structure:

```sql
CREATE TABLE job_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    job_role TEXT NOT NULL,
    applied_date DATE NOT NULL,
    url TEXT,
    status TEXT NOT NULL DEFAULT 'Waiting for hearback',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Customization

### Adding New Status Options
To add new status options:
1. Update the radio buttons in `templates/add.html` and `templates/edit.html`
2. Add corresponding CSS classes in `static/style.css`
3. Update the status validation in `app.py` if needed

### Changing Colors
Modify the CSS variables in `static/style.css`:
```css
:root {
    --accent-primary: #4a9eff;    /* Main accent color */
    --bg-primary: #1a1a1a;        /* Background color */
    --text-primary: #ffffff;      /* Text color */
    /* ... other variables */
}
```

## Troubleshooting

### Database Issues
- If you encounter database errors, delete `job_tracker.db` and restart the application
- The database will be recreated automatically

### Port Already in Use
- If port 5000 is busy, modify the port in `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Change port number
  ```

### Browser Compatibility
- Works best with modern browsers (Chrome, Firefox, Safari, Edge)
- JavaScript must be enabled for full functionality

## License

This is a personal project for individual use. Feel free to modify and adapt for your own needs.

