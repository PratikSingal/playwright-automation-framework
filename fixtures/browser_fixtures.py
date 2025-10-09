import pytest
import allure
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from loguru import logger
from datetime import datetime
from pathlib import Path


@pytest.fixture(scope="session")
def browser(config_manager) -> Browser:
    """
    Create browser instance for the session
    Browser type is determined by configuration
    """
    browser_type = config_manager.browser_type
    headless = config_manager.headless
    
    logger.info(f"Launching {browser_type} browser (headless: {headless})")
    
    playwright = sync_playwright().start()
    
    # Launch browser based on type
    if browser_type == "chromium":
        browser = playwright.chromium.launch(
            headless=headless,
            slow_mo=config_manager.get('browser.slow_mo', 0),
            args=['--start-maximized'] if not headless else []
        )
    elif browser_type == "firefox":
        browser = playwright.firefox.launch(
            headless=headless,
            slow_mo=config_manager.get('browser.slow_mo', 0)
        )
    elif browser_type == "webkit":
        browser = playwright.webkit.launch(
            headless=headless,
            slow_mo=config_manager.get('browser.slow_mo', 0)
        )
    else:
        playwright.stop()
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    logger.success(f"{browser_type} browser launched successfully")
    
    yield browser
    
    logger.info("Closing browser")
    browser.close()
    playwright.stop()


@pytest.fixture(scope="function")
def context(browser: Browser, config_manager) -> BrowserContext:
    """
    Create a new browser context for each test
    Browser context is like an incognito window - isolated cookies, cache, etc.
    """
    viewport = config_manager.get('browser.viewport', {'width': 1920, 'height': 1080})
    record_video = config_manager.get('browser.video', False)
    
    logger.info("Creating new browser context")
    
    # Context options
    context_options = {
        'viewport': viewport,
        'ignore_https_errors': True,
        'java_script_enabled': True,
        'accept_downloads': True
    }
    
    # Add video recording if enabled
    if record_video:
        video_dir = Path(config_manager.get('reporting.videos', 'reports/videos'))
        video_dir.mkdir(parents=True, exist_ok=True)
        context_options['record_video_dir'] = str(video_dir)
        context_options['record_video_size'] = viewport
    
    context = browser.new_context(**context_options)
    
    # Enable tracing for debugging
    if config_manager.get('browser.trace_on_failure', True):
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    logger.success("Browser context created")
    
    yield context
    
    logger.info("Closing browser context")
    
    # Stop tracing
    if config_manager.get('browser.trace_on_failure', True):
        try:
            context.tracing.stop()
        except Exception as e:
            logger.warning(f"Failed to stop tracing: {str(e)}")
    
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, config_manager, request) -> Page:
    """
    Create a new page for each test
    Handles screenshot and trace capture on failure
    """
    test_name = request.node.name
    logger.info(f"Creating new page for test: {test_name}")
    
    page = context.new_page()
    page.set_default_timeout(config_manager.timeout)
    page.set_default_navigation_timeout(config_manager.timeout)
    
    # Add test info to allure report
    allure.dynamic.parameter("Browser", config_manager.browser_type)
    allure.dynamic.parameter("Environment", config_manager.env)
    allure.dynamic.parameter("Base URL", config_manager.base_url)
    
    logger.success(f"Page created for test: {test_name}")
    
    yield page
    
    # Capture artifacts on failure
    test_failed = False
    if hasattr(request.node, 'rep_call'):
        test_failed = request.node.rep_call.failed
    
    if test_failed:
        logger.warning(f"Test failed: {test_name}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Take screenshot
        if config_manager.get('browser.screenshot_on_failure', True):
            try:
                screenshot_dir = Path(config_manager.get('reporting.screenshots', 'reports/screenshots'))
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                screenshot_path = screenshot_dir / f"{test_name}_{timestamp}.png"
                
                page.screenshot(path=str(screenshot_path), full_page=True)
                
                # Attach to Allure
                with open(screenshot_path, 'rb') as image:
                    allure.attach(
                        image.read(),
                        name=f"Failure Screenshot - {test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                
                logger.info(f"Failure screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {str(e)}")
        
        # Save trace
        if config_manager.get('browser.trace_on_failure', True):
            try:
                trace_dir = Path(config_manager.get('reporting.allure_results', 'reports/allure-results'))
                trace_dir.mkdir(parents=True, exist_ok=True)
                trace_path = trace_dir / f"trace_{test_name}_{timestamp}.zip"
                
                context.tracing.stop(path=str(trace_path))
                
                # Attach to Allure
                allure.attach.file(
                    str(trace_path),
                    name=f"Trace - {test_name}",
                    attachment_type=allure.attachment_type.ZIP
                )
                
                logger.info(f"Trace saved: {trace_path}")
                
                # Restart tracing for next potential failure in same context
                context.tracing.start(screenshots=True, snapshots=True, sources=True)
            except Exception as e:
                logger.error(f"Failed to save trace: {str(e)}")
        
        # Save page HTML
        try:
            html_content = page.content()
            allure.attach(
                html_content,
                name=f"Page HTML - {test_name}",
                attachment_type=allure.attachment_type.HTML
            )
            logger.info("Page HTML attached to report")
        except Exception as e:
            logger.error(f"Failed to save page HTML: {str(e)}")
        
        # Save console logs
        try:
            console_logs = "\n".join([f"[{msg.type}] {msg.text}" for msg in page.context.pages[0]._impl_obj._console_messages])
            if console_logs:
                allure.attach(
                    console_logs,
                    name=f"Console Logs - {test_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
                logger.info("Console logs attached to report")
        except Exception as e:
            logger.debug(f"Could not capture console logs: {str(e)}")
    
    logger.info("Closing page")
    page.close()


@pytest.fixture(scope="function")
def new_page(context: BrowserContext, config_manager):
    """
    Factory fixture to create multiple pages in a single test
    Usage: page2 = new_page()
    """
    pages = []
    
    def _create_page():
        page = context.new_page()
        page.set_default_timeout(config_manager.timeout)
        pages.append(page)
        logger.info(f"Created new page (total: {len(pages)})")
        return page
    
    yield _create_page
    
    # Close all created pages
    for page in pages:
        try:
            page.close()
        except Exception as e:
            logger.warning(f"Error closing page: {str(e)}")
    
    logger.info(f"Closed {len(pages)} additional page(s)")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test result for fixtures
    This makes test result available to fixtures via request.node.rep_call
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def console_messages(page: Page):
    """
    Fixture to capture console messages from the browser
    Usage: messages = console_messages
    """
    messages = []
    
    def handle_console(msg):
        messages.append({
            'type': msg.type,
            'text': msg.text,
            'location': msg.location
        })
        logger.debug(f"Console [{msg.type}]: {msg.text}")
    
    page.on("console", handle_console)
    
    yield messages
    
    # Log summary
    if messages:
        logger.info(f"Captured {len(messages)} console messages")
        for msg in messages:
            if msg['type'] in ['error', 'warning']:
                logger.warning(f"Browser {msg['type']}: {msg['text']}")


@pytest.fixture(scope="function")
def network_requests(page: Page):
    """
    Fixture to capture network requests
    Usage: requests = network_requests
    """
    requests = []
    
    def handle_request(request):
        requests.append({
            'url': request.url,
            'method': request.method,
            'headers': request.headers,
            'post_data': request.post_data
        })
    
    page.on("request", handle_request)
    
    yield requests
    
    logger.info(f"Captured {len(requests)} network requests")


@pytest.fixture(scope="function")
def network_responses(page: Page):
    """
    Fixture to capture network responses
    Usage: responses = network_responses
    """
    responses = []
    
    def handle_response(response):
        responses.append({
            'url': response.url,
            'status': response.status,
            'headers': response.headers
        })
    
    page.on("response", handle_response)
    
    yield responses
    
    logger.info(f"Captured {len(responses)} network responses")