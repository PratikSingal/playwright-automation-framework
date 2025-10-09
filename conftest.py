import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and setup logger from utils
from utils.logger import setup_logger, logger  # ✅ Import both

# Setup logger once at the start
setup_logger(log_dir=str(project_root / "logs"))

# Import all fixtures
pytest_plugins = [
    "fixtures.browser_fixtures",
    "fixtures.page_fixtures",
    "fixtures.data_fixtures",
    "fixtures.utility_fixtures",
]


def pytest_configure(config):
    """Pytest configuration hook"""
    logger.info("=" * 80)
    logger.info("TEST EXECUTION STARTED")
    logger.info("=" * 80)
    
    # Create reports directories
    reports_dir = project_root / "reports"
    (reports_dir / "allure-results").mkdir(parents=True, exist_ok=True)
    (reports_dir / "screenshots").mkdir(parents=True, exist_ok=True)
    (reports_dir / "videos").mkdir(parents=True, exist_ok=True)
    
    # Set environment variables for Allure
    os.environ['ALLURE_RESULTS_DIR'] = str(reports_dir / "allure-results")


def pytest_unconfigure(config):
    """Pytest unconfiguration hook"""
    logger.info("=" * 80)
    logger.info("TEST EXECUTION COMPLETED")
    logger.info("=" * 80)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before all tests"""
    logger.info("Setting up test environment")
    yield
    logger.info("Tearing down test environment")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test execution status
    This helps in screenshot capture and reporting
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        if rep.failed:
            logger.error(f"Test FAILED: {item.nodeid}")
        elif rep.passed:
            logger.success(f"Test PASSED: {item.nodeid}")
        elif rep.skipped:
            logger.warning(f"Test SKIPPED: {item.nodeid}")
    
    setattr(item, f"rep_{rep.when}", rep)


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against: dev, qa, staging, prod"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to run tests: chromium, firefox, webkit"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )


@pytest.fixture(scope="session")
def env(request):
    """Get environment from command line"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def browser_name(request):
    """Get browser name from command line"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless_mode(request):
    """Get headless mode from command line"""
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def test_data_manager(env):
    """Create TestDataManager with current environment"""
    from utils.test_data_manager import TestDataManager
    from pathlib import Path
    
    data_dir = Path(__file__).parent / "testdata"
    return TestDataManager(data_dir=str(data_dir), env=env)