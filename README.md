# Playwright Python Test Automation Framework

A comprehensive test automation framework built with Playwright (Python), featuring Page Object Model (POM), generic actions, Allure reporting, and support for GUI, API, and Database testing.

## 📁 Project Structure

```
playwright-automation-framework/
│
├── actions/                      # Generic action classes
│   ├── __init__.py
│   └── generic_actions.py       # Reusable web element interactions
│
├── api/                         # API testing utilities
│   ├── __init__.py
│   └── api_client.py           # HTTP client for API testing
│
├── config/                      # Configuration files
│   ├── __init__.py
│   ├── config_manager.py       # Configuration manager
│   ├── dev.yaml                # Development environment config
│   ├── qa.yaml                 # QA environment config (create as needed)
│   └── prod.yaml               # Production environment config (create as needed)
│
├── database/                    # Database utilities
│   ├── __init__.py
│   └── db_manager.py           # Oracle database manager
│
├── fixtures/                    # Pytest fixtures
│   ├── __init__.py
│   ├── browser_fixtures.py     # Browser and page fixtures
│   ├── page_fixtures.py        # Page object fixtures
│   └── data_fixtures.py        # Test data fixtures
│
├── logs/                        # Test execution logs
│
├── pages/                       # Page Object Models
│   ├── __init__.py
│   ├── base_page.py            # Base page class
│   └── registration_page.py    # Registration page POM
│
├── reports/                     # Test reports
│   ├── allure-results/         # Allure raw results
│   ├── allure-report/          # Allure HTML reports
│   ├── screenshots/            # Failure screenshots
│   └── videos/                 # Test execution videos
│
├── testdata/                    # Test data files
│   ├── __init__.py
│   ├── test_mapping.json       # Test case to data mapping
│   └── registration_data.json  # Registration test data
│
├── tests/                       # Test cases
│   ├── __init__.py
│   └── test_registration.py    # Registration tests
│
├── utils/                       # Utility modules
│   ├── __init__.py
│   ├── helpers.py              # Helper functions
│   ├── logger.py               # Custom logger
│   └── test_data_manager.py   # Test data manager
│
├── conftest.py                  # Pytest configuration
├── pytest.ini                   # Pytest settings
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or create the project structure:**
   ```powershell
   # Run the project structure script (from artifacts)
   # This will create all necessary folders
   ```

2. **Create a virtual environment:**
   ```powershell
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```powershell
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Install Playwright browsers:**
   ```powershell
   playwright install
   ```

## ⚙️ Configuration

### Environment Configuration

Edit `config/dev.yaml` (or create qa.yaml, staging.yaml, prod.yaml) with your settings:

```yaml
application:
  base_url: "https://your-app-url.com"

browser:
  type: "chromium"  # chromium, firefox, webkit
  headless: false
  timeout: 30000

database:
  host: "localhost"
  port: 1521
  service_name: "ORCL"
  username: "your_username"
  password: "your_password"

api:
  base_url: "https://api.your-app.com"
```

## 📝 Writing Tests

### 1. Create a Page Object Model

```python
# pages/your_page.py
from pages.base_page import BasePage

class YourPage(BasePage):
    FIELD_MAPPING = {
        'field_name': {
            'locator': '#field_id',
            'type': 'textbox'  # textbox, textarea, radio, checkbox, dropdown, file
        }
    }
    
    def fill_form(self, data):
        self.fill_form_data(self.FIELD_MAPPING, data)
```

### 2. Create Test Data

```json
// testdata/your_data.json
{
  "test_scenario_1": {
    "field_name": "value",
    "another_field": "another_value"
  }
}
```

### 3. Map Test to Data

```json
// testdata/test_mapping.json
{
  "test_your_scenario": {
    "data_file": "your_data.json",
    "dataset": "test_scenario_1"
  }
}
```

### 4. Write Test Case

```python
# tests/test_your_feature.py
import pytest
import allure

@allure.feature("Your Feature")
@pytest.mark.gui
def test_your_scenario(your_page, get_test_data):
    data = get_test_data('test_your_scenario')
    your_page.open("https://your-url.com")
    your_page.fill_form(data)
    # Add assertions
```

## 🏃 Running Tests

### Run all tests:
```powershell
pytest
```

### Run specific test file:
```powershell
pytest tests/test_registration.py
```

### Run with specific markers:
```powershell
pytest -m smoke        # Run smoke tests
pytest -m regression   # Run regression tests
pytest -m "gui and critical"  # Run GUI critical tests
```

### Run with specific environment:
```powershell
pytest --env=qa
```

### Run with specific browser:
```powershell
pytest --browser=firefox
```

### Run in headless mode:
```powershell
pytest --headless
```

### Run with parallel execution:
```powershell
pip install pytest-xdist
pytest -n 4  # Run with 4 workers
```

## 📊 Viewing Reports

### Generate and view Allure report:
```powershell
# Generate report
allure generate reports/allure-results --clean -o reports/allure-report

# Open report in browser
allure open reports/allure-report
```

### Or use allure serve (generates and opens):
```powershell
allure serve reports/allure-results
```

## 🎯 Test Markers

Available pytest markers:
- `@pytest.mark.smoke` - Smoke tests
- `@pytest.mark.regression` - Regression tests
- `@pytest.mark.sanity` - Sanity tests
- `@pytest.mark.gui` - GUI tests
- `@pytest.mark.api` - API tests
- `@pytest.mark.database` - Database tests
- `@pytest.mark.critical` - Critical priority
- `@pytest.mark.high` - High priority
- `@pytest.mark.medium` - Medium priority
- `@pytest.mark.low` - Low priority

## 🔧 Framework Features

### Generic Actions
The framework includes a comprehensive generic actions class that supports:
- Textbox input
- Textarea input
- Radio button selection
- Checkbox selection
- Dropdown selection
- File upload
- Click actions
- Keyboard actions
- Screenshot capture
- Element visibility checks
- Wait operations

### Page Object Model (POM)
- Base page with common functionality
- Generic `fill_form_data()` method
- Field mapping configuration
- Easy to extend for new pages
- **Adding new fields**: Just update the FIELD_MAPPING dictionary - no method changes needed!

### Test Data Management
- JSON-based test data storage
- Test case to data file mapping
- Support for multiple datasets per file
- Easy data retrieval using test case IDs

### Allure Reporting
- Detailed step-by-step execution logs
- Screenshot on failure
- Video recording (optional)
- Trace files for debugging
- Test categorization with features and stories
- Severity levels
- Test parameters tracking

### Database Support
- Oracle database connectivity
- Context manager for automatic connection handling
- Query execution and result fetching
- Stored procedure support
- Transaction management

### API Testing Support
- RESTful API client
- Support for GET, POST, PUT, DELETE, PATCH methods
- Request/response logging
- Authentication token management
- JSON payload handling

## 📚 Best Practices

### 1. Page Object Model
```python
# ✅ Good - Generic and scalable
FIELD_MAPPING = {
    'username': {'locator': '#username', 'type': 'textbox'},
    'bio': {'locator': '#bio', 'type': 'textarea'}
}

def fill_form(self, data):
    self.fill_form_data(self.FIELD_MAPPING, data)

# ❌ Avoid - Hardcoded and inflexible
def fill_username(self, username):
    self.page.locator('#username').fill(username)

def fill_bio(self, bio):
    self.page.locator('#bio').fill(bio)
```

### 2. Test Data
- Keep test data separate from test code
- Use descriptive dataset names
- Maintain different datasets for positive and negative scenarios
- Use test_mapping.json to link tests with data

### 3. Assertions
```python
# ✅ Good - Clear assertion messages
assert registration_page.is_registration_form_displayed(), \
    "Registration form should be visible"

# ❌ Avoid - No context
assert registration_page.is_registration_form_displayed()
```

### 4. Allure Steps
```python
# Use allure steps for better reporting
with allure.step("Navigate to registration page"):
    registration_page.open(url)

with allure.step("Fill registration form"):
    registration_page.fill_registration_form(data)
```

## 🔍 Adding New Test Cases

### Step-by-Step Guide:

**1. Create test data (if needed):**
```json
// testdata/new_feature_data.json
{
  "valid_scenario": {
    "field1": "value1",
    "field2": "value2"
  }
}
```

**2. Map test to data:**
```json
// testdata/test_mapping.json
{
  "test_new_feature_valid": {
    "data_file": "new_feature_data.json",
    "dataset": "valid_scenario"
  }
}
```

**3. Create page object (if needed):**
```python
// pages/new_feature_page.py
from pages.base_page import BasePage

class NewFeaturePage(BasePage):
    FIELD_MAPPING = {
        'field1': {'locator': '#field1', 'type': 'textbox'},
        'field2': {'locator': '#field2', 'type': 'dropdown'}
    }
    
    def fill_form(self, data):
        self.fill_form_data(self.FIELD_MAPPING, data)
```

**4. Create fixture:**
```python
// fixtures/page_fixtures.py
@pytest.fixture
def new_feature_page(page: Page) -> NewFeaturePage:
    return NewFeaturePage(page)
```

**5. Write test:**
```python
// tests/test_new_feature.py
import pytest
import allure

@allure.feature("New Feature")
@pytest.mark.gui
class TestNewFeature:
    def test_new_feature_valid(self, new_feature_page, get_test_data):
        data = get_test_data('test_new_feature_valid')
        new_feature_page.open("https://example.com/feature")
        new_feature_page.fill_form(data)
        # Add assertions
```

## 🗄️ Database Testing Example

```python
from database.db_manager import DatabaseManager

def test_user_in_database():
    with DatabaseManager() as db:
        # Query database
        results = db.execute_query(
            "SELECT * FROM users WHERE email = :email",
            ('test@example.com',)
        )
        
        # Assertions
        assert len(results) > 0, "User not found in database"
        assert results[0]['STATUS'] == 'ACTIVE'
```

## 🌐 API Testing Example

```python
from api.api_client import APIClient
import allure

@allure.feature("API Tests")
def test_get_user_api():
    api = APIClient()
    
    # Make API call
    response = api.get("/users/1")
    
    # Assertions
    assert response.status_code == 200
    assert response.json()['id'] == 1
```

## 🐛 Debugging

### View Playwright trace:
```powershell
playwright show-trace reports/allure-results/trace_test_name.zip
```

### Enable debug logging:
```python
# In test file
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Slow down execution:
```yaml
# config/dev.yaml
browser:
  slow_mo: 1000  # Milliseconds
```

## 📦 Adding New Dependencies

```powershell
# Install package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

## 🔒 Security Notes

- Never commit sensitive data (passwords, tokens) to version control
- Use environment variables or secure vaults for credentials
- Add sensitive data files to `.gitignore`
- Use different config files for different environments

## 🤝 Contributing

When adding new features:
1. Follow the existing folder structure
2. Update this README
3. Add appropriate test markers
4. Include docstrings in your code
5. Add test data examples

## 📞 Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review Allure reports for detailed test execution
3. Check screenshots in `reports/screenshots/`
4. Review trace files for step-by-step execution

## 🎓 Learning Resources

- [Playwright Python Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Page Object Model Pattern](https://playwright.dev/python/docs/pom)

## 📋 Checklist for New Team Members

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] Playwright browsers installed
- [ ] Configuration files updated with correct URLs
- [ ] Can run sample tests successfully
- [ ] Allure reports generating correctly
- [ ] Familiar with project structure
- [ ] Read this README completely

---

**Happy Testing! 🚀**