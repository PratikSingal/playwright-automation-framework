import pytest
import allure
from pathlib import Path
from datetime import datetime
from loguru import logger
from config.config_manager import config


@pytest.fixture(scope="session")
def base_url():
    """
    Get base URL from configuration
    
    Usage in test:
        def test_something(base_url):
            full_url = f"{base_url}/login"
    """
    url = config.base_url
    logger.info(f"Base URL: {url}")
    return url


@pytest.fixture(scope="function")
def timestamp():
    """
    Get current timestamp
    
    Usage in test:
        def test_something(timestamp):
            filename = f"test_{timestamp}.txt"
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.debug(f"Generated timestamp: {ts}")
    return ts


@pytest.fixture(scope="function")
def unique_id():
    """
    Generate unique ID for test
    
    Usage in test:
        def test_something(unique_id):
            email = f"user_{unique_id}@example.com"
    """
    import uuid
    uid = str(uuid.uuid4())[:8]
    logger.debug(f"Generated unique ID: {uid}")
    return uid


@pytest.fixture(scope="function")
def temp_file(tmp_path):
    """
    Create temporary file for test
    
    Usage in test:
        def test_file_upload(temp_file):
            file_path = temp_file("test.txt", "content")
    """
    created_files = []
    
    def _create_file(filename: str, content: str = "") -> Path:
        file_path = tmp_path / filename
        file_path.write_text(content, encoding='utf-8')
        created_files.append(file_path)
        logger.info(f"Created temporary file: {file_path}")
        return file_path
    
    yield _create_file
    
    # Cleanup
    for file_path in created_files:
        if file_path.exists():
            file_path.unlink()
            logger.debug(f"Cleaned up temporary file: {file_path}")


@pytest.fixture(scope="function")
def screenshot_path(timestamp):
    """
    Get path for saving screenshots
    
    Usage in test:
        def test_something(page, screenshot_path):
            path = screenshot_path("test_name")
            page.screenshot(path=path)
    """
    def _get_path(name: str) -> str:
        screenshot_dir = Path(config.get('reporting.screenshots', 'reports/screenshots'))
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        path = screenshot_dir / f"{name}_{timestamp}.png"
        logger.debug(f"Screenshot path: {path}")
        return str(path)
    
    return _get_path


@pytest.fixture(scope="function")
def wait_helper(page):
    """
    Helper for custom wait operations
    
    Usage in test:
        def test_something(page, wait_helper):
            wait_helper.for_url_contains("/dashboard")
            wait_helper.for_element_count("#items", 5)
    """
    class WaitHelper:
        def __init__(self, page):
            self.page = page
        
        @allure.step("Wait for URL to contain: {text}")
        def for_url_contains(self, text: str, timeout: int = 30000):
            logger.info(f"Waiting for URL to contain: {text}")
            self.page.wait_for_url(f"**{text}**", timeout=timeout)
            logger.success(f"URL contains: {text}")
        
        @allure.step("Wait for element count: {locator} = {count}")
        def for_element_count(self, locator: str, count: int, timeout: int = 30000):
            logger.info(f"Waiting for {count} elements matching: {locator}")
            self.page.wait_for_function(
                f"document.querySelectorAll('{locator}').length === {count}",
                timeout=timeout
            )
            logger.success(f"Found {count} elements")
        
        @allure.step("Wait for {seconds} seconds")
        def for_seconds(self, seconds: float):
            import time
            logger.info(f"Waiting for {seconds} seconds")
            time.sleep(seconds)
    
    return WaitHelper(page)


@pytest.fixture(scope="function")
def retry_helper():
    """
    Helper for retrying operations
    
    Usage in test:
        def test_something(retry_helper):
            result = retry_helper(some_function, max_attempts=3)
    """
    def _retry(func, max_attempts: int = 3, delay: float = 1.0, *args, **kwargs):
        import time
        
        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(f"Attempt {attempt}/{max_attempts}")
                result = func(*args, **kwargs)
                logger.success(f"Operation succeeded on attempt {attempt}")
                return result
            except Exception as e:
                if attempt == max_attempts:
                    logger.error(f"All {max_attempts} attempts failed")
                    raise
                logger.warning(f"Attempt {attempt} failed: {str(e)}, retrying...")
                time.sleep(delay)
    
    return _retry


@pytest.fixture(scope="function")
def environment_info():
    """
    Get environment information
    
    Usage in test:
        def test_something(environment_info):
            if environment_info['env'] == 'prod':
                # Skip test in production
                pytest.skip("Skipping in production")
    """
    info = {
        'env': config.env,
        'base_url': config.base_url,
        'browser': config.browser_type,
        'headless': config.headless,
        'timeout': config.timeout
    }
    
    logger.info(f"Environment info: {info}")
    
    # Attach to Allure
    import json
    allure.attach(
        json.dumps(info, indent=2),
        name="Environment Information",
        attachment_type=allure.attachment_type.JSON
    )
    
    return info


@pytest.fixture(scope="function")
def skip_if_environment():
    """
    Skip test based on environment
    
    Usage in test:
        def test_something(skip_if_environment):
            skip_if_environment(['prod', 'staging'])
            # Test will only run in dev/qa
    """
    def _skip(environments: list):
        if config.env in environments:
            logger.warning(f"Skipping test in {config.env} environment")
            pytest.skip(f"Test skipped in {config.env} environment")
    
    return _skip


@pytest.fixture(scope="function")
def allure_labels(request):
    """
    Add custom labels to Allure report
    
    Usage in test:
        def test_something(allure_labels):
            allure_labels.add('component', 'Registration')
            allure_labels.add('owner', 'QA Team')
    """
    class AllureLabels:
        @staticmethod
        def add(label_type: str, value: str):
            allure.dynamic.label(label_type, value)
            logger.debug(f"Added Allure label: {label_type}={value}")
        
        @staticmethod
        def add_link(name: str, url: str, link_type: str = 'link'):
            allure.dynamic.link(url, name=name, link_type=link_type)
            logger.debug(f"Added Allure link: {name}={url}")
        
        @staticmethod
        def add_issue(issue_id: str, url: str = None):
            if url:
                allure.dynamic.issue(issue_id, url)
            else:
                allure.dynamic.issue(issue_id)
            logger.debug(f"Added Allure issue: {issue_id}")
        
        @staticmethod
        def add_testcase(testcase_id: str, url: str = None):
            if url:
                allure.dynamic.testcase(testcase_id, url)
            else:
                allure.dynamic.testcase(testcase_id)
            logger.debug(f"Added Allure test case: {testcase_id}")
    
    return AllureLabels()


@pytest.fixture(scope="function", autouse=True)
def test_timer(request):
    """
    Automatically time test execution
    """
    test_name = request.node.name
    start_time = datetime.now()
    
    logger.info(f"Test '{test_name}' started at {start_time.strftime('%H:%M:%S')}")
    
    yield
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logger.info(f"Test '{test_name}' completed in {duration:.2f} seconds")
    
    # Attach timing to Allure
    allure.dynamic.parameter("Execution Time", f"{duration:.2f}s")