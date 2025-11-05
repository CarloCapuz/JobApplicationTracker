# Job Application Tracker

A personal desktop web application for tracking job applications with a modern dark mode interface.

## Features

- **Add Job Applications**: Track company name, job role, applied date, URL, status, and Notes/Additional Info
- **Status Tracking**: Monitor applications through different stages:
  - Applied
  - Denied without interview (visa related)
  - Denied without interview (non-visa related)
  - Interview 1
  - Interview 2
  - Interview 3
  - Offer
- **Status History / Audit Trail**: Automatically tracks all status changes with timestamps. View the complete history of when an application moved from Applied → Interview 1 → Interview 2, etc., directly on each application card
- **Sorting**: Sort applications by company name, job role, applied date, status, or last updated date
- **Notes / Additional Info**: Large free-text field for IDs, confirmation numbers, interview details, etc. Shown on cards and editable in Add/Edit
- **Clickable Summary Filters**: Click any header card (Total, Applied, Denied, Interview x, Offer) to filter the list; combines with search
- **Authentication**: Protected with login via environment variables (`FLASK_USERNAME`, `FLASK_PASSWORD`)
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

4. **Create a .env file (credentials and config)**:
   - Easiest: auto-generate a starter file
   ```bash
   python setup.py
   ```
   - Or manually create `.env` with at least:
   ```
   FLASK_USERNAME=your_username
   FLASK_PASSWORD=your_password
   SECRET_KEY=your_random_secret
   FLASK_ENV=development
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

7. **Login** with your credentials:
   - Username: The value from `FLASK_USERNAME` in your `.env` file
   - Password: The value from `FLASK_PASSWORD` in your `.env` file
   - Default (if using `setup.py`): Username and password will be shown in the setup output

## Testing

The project includes comprehensive unit tests to ensure reliability and maintainability. The test suite includes **48 tests** covering all major functionality.

### Running Tests

**Run all tests:**
```bash
python -m pytest
```

**Run tests with verbose output:**
```bash
python -m pytest -v
```

**Run tests with coverage report:**
```bash
python -m pytest --cov=app --cov-report=html
```
View the coverage report by opening `htmlcov/index.html` in your browser.

**Run specific test files:**
```bash
python -m pytest tests/test_database.py
python -m pytest tests/test_api.py
python -m pytest tests/test_summary.py
python -m pytest tests/test_app.py
```

**Run specific test functions:**
```bash
python -m pytest tests/test_api.py::test_add_application_with_notes
python -m pytest tests/test_database.py::test_notes_field_optional
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

- **Database Operations**: 
  - Schema creation and validation (including `notes` field and `status_history` table)
  - Constraints and data integrity
  - Auto-increment IDs
  - Default values (including default status 'Applied')
  - Optional fields (URL, notes)
  - Status history table schema and foreign key relationships

- **API Endpoints**: 
  - CRUD operations (Create, Read, Update, Delete)
  - Error handling and validation
  - Missing required fields
  - Invalid data handling
  - Notes field in add/edit operations
  - Status history tracking on add/edit
  - API response format and structure (including status_history)
  - All status types (Applied, Denied without interview variants, Interview 1-3, Offer)

- **Summary Statistics**: 
  - Accurate counting by status (including new status names)
  - Empty database handling
  - Multiple applications aggregation
  - Status consistency checks

- **Authentication**: 
  - Test fixtures automatically handle login
  - All routes require authentication in tests
  - Test credentials are managed automatically

- **Status History / Audit Trail**: 
  - Status history recorded when adding applications
  - Status history updated when status changes
  - Status history not duplicated when status unchanged
  - Multiple status changes tracked correctly
  - Status history included in API responses

- **Edge Cases**: 
  - Invalid data types
  - Missing fields
  - Non-existent records
  - Empty optional fields
  - Status migration from old to new names

### Test Structure

```
tests/
├── conftest.py          # Test configuration, fixtures, and authentication setup
├── test_database.py     # Database operation and schema tests (8 tests)
├── test_api.py          # API endpoint and CRUD tests (25 tests)
├── test_summary.py      # Summary statistics tests (9 tests)
└── test_app.py          # Application configuration and routing tests (6 tests)
```

### Test Configuration

**Test Environment:**
- Tests use a temporary SQLite database for each test run
- Each test runs in a clean, isolated environment
- Authentication is automatically handled via test fixtures
- Test credentials are set up and cleaned up automatically

**Test Fixtures:**
- `client`: Provides an authenticated Flask test client
- `sample_data`: Sample job application data with notes
- `multiple_applications`: Multiple test applications for bulk testing

**Notes Field Testing:**
- Tests verify notes can be added, edited, and retrieved
- Tests ensure notes field is optional (can be empty)
- Tests verify API responses include notes field
- Database tests verify notes column exists and is nullable

**Status History Testing:**
- Tests verify status history is recorded when adding applications
- Tests verify status history is updated when status changes
- Tests ensure status history is not duplicated when status unchanged
- Tests verify multiple status changes are tracked correctly
- Tests verify status_history table schema and foreign key relationships
- Database tests verify status_history table exists and has correct structure

### Example Test Output

```
============================= test session starts =============================
platform win32 -- Python 3.9.5, pytest-7.4.3
collected 48 items

tests/test_api.py::test_add_application_with_notes PASSED              [ 41%]
tests/test_api.py::test_status_history_on_add PASSED                   [ 51%]
tests/test_api.py::test_status_history_multiple_changes PASSED         [ 81%]
tests/test_database.py::test_notes_field_optional PASSED               [ 79%]
tests/test_database.py::test_status_history_table_exists PASSED        [ 82%]
...

============================= 48 passed in 2.07s ==============================
```

## Authentication

The application is protected with login authentication. You must log in before accessing any features.

**First Time Setup:**
- Run `python setup.py` to create a `.env` file with default credentials
- Or manually create `.env` with your own `FLASK_USERNAME` and `FLASK_PASSWORD`
- **Important**: Change default credentials before deploying to production!

**Login:**
- Visit `http://localhost:5000` - you'll be redirected to the login page
- Enter your username and password
- Click "Login" to access the application
- Your session will remain active until you log out

**Security:**
- Credentials are stored in environment variables (not in code)
- Passwords are hashed using SHA-256
- Sessions are managed securely with Flask-Login
- The `.env` file is excluded from Git via `.gitignore`

## Usage

### Adding a New Application
1. Click "Add New Application" button
2. Fill in the required fields:
   - Company Name
   - Job Role
   - Applied Date (use the date picker)
   - Job URL (optional)
   - Status (select from radio buttons)
   - Notes / Additional Information (optional free text)
3. Click "Add Application"

### Managing Applications
- **View All**: See all applications in a card-based layout
- **View Status History**: Each application card shows a complete audit trail of status changes with timestamps. See when an application moved from Applied → Interview 1 → Interview 2, etc.
- **Filter by Status**: Click any summary header card (Total, Applied, Denied, Interview x, Offer) to filter by that status. Click "Total Applications" to clear the filter and show all.
- **Search**: Type in the search bar for live filtering. Searches across:
  - Company name
  - Job role
  - Status
  - Notes/Additional Information
  - Search works in combination with status filters (both filters apply simultaneously)
- **Sort**: Use the sort dropdowns to organize by different criteria (applied date, company name, job role, status, or last updated)
- **Edit**: Click "Edit" on any application card to modify details (including notes). Status changes are automatically tracked in the history.
- **Delete**: Click "Delete" to remove an application (with confirmation dialog). This also removes all associated status history.

### Keyboard Shortcuts
- `Ctrl/Cmd + N`: Add new application
- `Escape`: Return to main list

## File Structure

```
Tracker/
├── app.py                 # Flask application with authentication
├── wsgi.py                # WSGI entry point (used by Vercel)
├── vercel.json            # Vercel deployment config
├── setup.py               # Setup helper (creates .env file)
├── .gitignore             # Ensures .env and DB are not committed
├── requirements.txt       # Python dependencies (includes Flask-Login)
├── pytest.ini             # Pytest configuration
├── run_tests.py           # Test runner script
├── job_tracker.db         # SQLite database (created automatically)
├── templates/             # HTML templates
│   ├── index.html         # Main application list with filters
│   ├── add.html           # Add new application form
│   ├── edit.html          # Edit application form
│   └── login.html         # Login page
├── static/                # Static assets
│   ├── style.css          # Dark mode styling
│   └── script.js          # JavaScript functionality (filters, search)
└── tests/                 # Test suite
    ├── conftest.py        # Test fixtures and authentication setup
    ├── test_database.py   # Database tests
    ├── test_api.py        # API endpoint tests
    ├── test_summary.py    # Summary statistics tests
    └── test_app.py        # Application configuration tests
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
    status TEXT NOT NULL DEFAULT 'Applied',
    notes TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE status_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES job_applications(id) ON DELETE CASCADE
);
```

**Status History Table**: The `status_history` table automatically tracks all status changes for audit purposes. Each time a status changes, a new entry is created with a timestamp. This allows you to see the complete timeline of an application's journey.

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

### Authentication Issues
- **"Invalid username or password"**: 
  - Check your `.env` file exists and contains `FLASK_USERNAME` and `FLASK_PASSWORD`
  - Verify credentials match exactly (case-sensitive)
  - Run `python setup.py` to create a new `.env` file if needed
- **Redirected to login repeatedly**:
  - Clear your browser cookies/session data
  - Restart the Flask application
  - Check that `SECRET_KEY` is set in your `.env` file

### Database Issues
- The app will auto-migrate to add `notes` if missing. For a clean reset, stop the app, delete `job_tracker.db`, and start again
- If you see database errors, the app will attempt to recreate the database automatically

### Port Already in Use
- If port 5000 is busy, modify the port in `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Change port number
  ```

### Search/Filter Not Working
- Ensure JavaScript is enabled in your browser
- Clear browser cache and reload the page
- Check browser console for JavaScript errors (F12 → Console)

## Deployment (Vercel)

Vercel offers a generous free tier and simple deployment.

1. Ensure these files exist: `vercel.json`, `wsgi.py`, `requirements.txt`
2. Push to GitHub (make sure `.env` and `job_tracker.db` are ignored via `.gitignore`)
3. Import the repo in Vercel or run `vercel` from the project directory
4. In Vercel dashboard, add Environment Variables:
```
FLASK_USERNAME=your_username
FLASK_PASSWORD=your_password
SECRET_KEY=your_random_secret
FLASK_ENV=production
```

Note: SQLite is not persistent on serverless platforms; for production persistence, use an external DB (e.g., Supabase, Postgres). For personal/light use, the current setup works but data resets on redeploy.

### Browser Compatibility
- Works best with modern browsers (Chrome, Firefox, Safari, Edge)
- JavaScript must be enabled for full functionality

## License

This is a personal project for individual use. Feel free to modify and adapt for your own needs.

