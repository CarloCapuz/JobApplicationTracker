# Job Application Tracker

A personal desktop web application for tracking job applications with a modern dark mode interface.

## Features

- **Add Job Applications**: Track company name, job role, applied date, URL, status, and Notes/Additional Info
- **Status Tracking**: Monitor applications through different stages:
  - Waiting for hearback
  - Denied
  - Interview
  - Interview 2
  - Interview 3
  - Offer
- **Sorting**: Sort applications by company name, job role, applied date, status, or last updated date
- **Notes / Additional Info**: Large free-text field for IDs, confirmation numbers, interview details, etc. Shown on cards and editable in Add/Edit
- **Clickable Summary Filters**: Click any header card (Total, Waiting for hearback, Denied, Interview x, Offer) to filter the list; combines with search
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

The project includes comprehensive unit tests to ensure reliability and maintainability. The test suite includes **43 tests** covering all major functionality.

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
  - Schema creation and validation (including `notes` field)
  - Constraints and data integrity
  - Auto-increment IDs
  - Default values
  - Optional fields (URL, notes)

- **API Endpoints**: 
  - CRUD operations (Create, Read, Update, Delete)
  - Error handling and validation
  - Missing required fields
  - Invalid data handling
  - Notes field in add/edit operations
  - API response format and structure

- **Summary Statistics**: 
  - Accurate counting by status
  - Empty database handling
  - Multiple applications aggregation
  - Status consistency checks

- **Authentication**: 
  - Test fixtures automatically handle login
  - All routes require authentication in tests
  - Test credentials are managed automatically

- **Edge Cases**: 
  - Invalid data types
  - Missing fields
  - Non-existent records
  - Empty optional fields

### Test Structure

```
tests/
├── conftest.py          # Test configuration, fixtures, and authentication setup
├── test_database.py     # Database operation and schema tests (7 tests)
├── test_api.py          # API endpoint and CRUD tests (21 tests)
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

### Example Test Output

```
============================= test session starts =============================
platform win32 -- Python 3.9.5, pytest-7.4.3
collected 43 items

tests/test_api.py::test_add_application_with_notes PASSED              [ 41%]
tests/test_database.py::test_notes_field_optional PASSED               [ 79%]
...

============================= 43 passed in 1.25s ==============================
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
- **Filter by Status**: Click any summary header card (Total, Waiting for hearback, Denied, Interview, etc.) to filter by that status. Click "Total Applications" to clear the filter and show all.
- **Search**: Type in the search bar for live filtering. Searches across:
  - Company name
  - Job role
  - Status
  - Notes/Additional Information
  - Search works in combination with status filters (both filters apply simultaneously)
- **Sort**: Use the sort dropdowns to organize by different criteria (applied date, company name, job role, status, or last updated)
- **Edit**: Click "Edit" on any application card to modify details (including notes)
- **Delete**: Click "Delete" to remove an application (with confirmation dialog)

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

The application uses a SQLite database with the following structure (includes `notes`):

```sql
CREATE TABLE job_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    job_role TEXT NOT NULL,
    applied_date DATE NOT NULL,
    url TEXT,
    status TEXT NOT NULL DEFAULT 'Waiting for hearback',
    notes TEXT,
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

