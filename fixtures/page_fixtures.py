import pytest
from playwright.sync_api import Page
from pages.registration_page import RegistrationPage
# Import other pages as you create them
# from pages.login_page import LoginPage
# from pages.dashboard_page import DashboardPage
from loguru import logger


@pytest.fixture(scope="function")
def registration_page(page: Page) -> RegistrationPage:
    """
    Create Registration Page Object
    
    Usage in test:
        def test_registration(registration_page):
            registration_page.open("https://example.com/register")
            registration_page.fill_registration_form(data)
    """
    logger.info("Creating Registration Page fixture")
    reg_page = RegistrationPage(page)
    logger.success("Registration Page fixture created")
    return reg_page


# Add more page fixtures here as you create more pages

# Example for Login Page:
# @pytest.fixture(scope="function")
# def login_page(page: Page) -> LoginPage:
#     """Create Login Page Object"""
#     logger.info("Creating Login Page fixture")
#     return LoginPage(page)

# Example for Dashboard Page:
# @pytest.fixture(scope="function")
# def dashboard_page(page: Page) -> DashboardPage:
#     """Create Dashboard Page Object"""
#     logger.info("Creating Dashboard Page fixture")
#     return DashboardPage(page)


@pytest.fixture(scope="function")
def multi_page_setup(page: Page):
    """
    Setup multiple pages for tests that need multiple page objects
    
    Usage in test:
        def test_workflow(multi_page_setup):
            pages = multi_page_setup()
            pages['registration'].open(url)
            pages['registration'].fill_form(data)
    """
    def _setup_pages():
        logger.info("Setting up multiple page objects")
        
        pages = {
            'registration': RegistrationPage(page),
            # Add more pages as needed:
            # 'login': LoginPage(page),
            # 'dashboard': DashboardPage(page),
        }
        
        logger.success(f"Created {len(pages)} page objects")
        return pages
    
    return _setup_pages


@pytest.fixture(scope="function")
def page_with_url(page: Page):
    """
    Factory fixture to create page object and navigate to URL
    
    Usage in test:
        reg_page = page_with_url(RegistrationPage, "https://example.com/register")
    """
    def _create_page(page_class, url: str):
        logger.info(f"Creating {page_class.__name__} and navigating to {url}")
        page_obj = page_class(page)
        page_obj.navigate_to(url)
        logger.success(f"{page_class.__name__} created and navigated")
        return page_obj
    
    return _create_page