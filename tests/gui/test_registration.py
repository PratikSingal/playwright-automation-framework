import pytest
import allure
from pages.registration_page import RegistrationPage
from playwright.sync_api import Page, expect
from config.config_manager import config
from loguru import logger


@allure.feature("User Registration - Advanced Tests")
@allure.story("Registration with Dynamic Data")
@pytest.mark.gui
class TestRegistrationAdvanced:
    """Advanced test cases demonstrating all fixture capabilities"""
    
    @allure.title("Test registration with generated random data")
    @allure.description("Verify registration using dynamically generated user data")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_registration_with_generated_data(
        self,
        registration_page: RegistrationPage,
        generate_random_user_data,
        base_url: str
    ):
        """Test registration with randomly generated user data"""
        
        with allure.step("Generate random user data"):
            user_data = generate_random_user_data(gender='male')
            logger.info(f"Generated user: {user_data['email']}")
        
        with allure.step("Navigate to registration page"):
            registration_page.open(f"{base_url}/register")
            assert registration_page.is_registration_form_displayed()
        
        with allure.step("Fill registration form with generated data"):
            registration_page.fill_registration_form(user_data)
        
        with allure.step("Submit registration"):
            registration_page.submit_form()
            # Add your success verification here
    
    @allure.title("Test registration with data overrides")
    @allure.description("Use test data but override specific fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_registration_with_overrides(
        self,
        registration_page: RegistrationPage,
        test_data_with_overrides,
        base_url: str,
        unique_id: str
    ):
        """Test registration with overridden test data"""
        
        with allure.step("Get test data with custom email"):
            custom_email = f"testuser_{unique_id}@example.com"
            data = test_data_with_overrides(
                'test_registration_valid_user',
                email=custom_email,
                phone='+919876543299'
            )
            logger.info(f"Using custom email: {custom_email}")
        
        with allure.step("Navigate and fill form"):
            registration_page.open(f"{base_url}/register")
            registration_page.fill_registration_form(data)
        
        with allure.step("Verify email field contains custom value"):
            email_value = registration_page.get_field_value('email')
            assert email_value == custom_email, f"Expected {custom_email}, got {email_value}"
    
    @allure.title("Test registration from multiple data files")
    @allure.description("Merge data from different sources")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_registration_merged_data(
        self,
        registration_page: RegistrationPage,
        get_data_from_file,
        base_url: str
    ):
        """Test using merged data from multiple datasets"""
        
        with allure.step("Get and merge data from different datasets"):
            base_data = get_data_from_file('registration_data.json', 'valid_user_1')
            additional_info = get_data_from_file('registration_data.json', 'complete_registration')
            
            # Merge: take personal info from base_data, add bio and country from additional_info
            merged_data = {**base_data}
            if 'bio' in additional_info:
                merged_data['bio'] = additional_info['bio']
            if 'country' in additional_info:
                merged_data['country'] = additional_info['country']
            
            logger.info(f"Merged data has {len(merged_data)} fields")
        
        with allure.step("Navigate and fill form with merged data"):
            registration_page.open(f"{base_url}/register")
            registration_page.fill_registration_form(merged_data)
    
    @allure.title("Test registration with screenshot on specific step")
    @allure.description("Capture screenshot at important verification points")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.sanity
    def test_registration_with_custom_screenshot(
        self,
        page: Page,
        registration_page: RegistrationPage,
        get_test_data,
        screenshot_path,
        base_url: str
    ):
        """Test with manual screenshot capture"""
        
        data = get_test_data('test_registration_valid_user')
        
        with allure.step("Navigate to registration page"):
            registration_page.open(f"{base_url}/register")
        
        with allure.step("Fill form and capture screenshot"):
            registration_page.fill_registration_form(data)
            
            # Take custom screenshot
            screenshot_file = screenshot_path("form_filled")
            page.screenshot(path=screenshot_file)
            
            # Attach to Allure
            allure.attach.file(
                screenshot_file,
                name="Form Filled State",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info("Screenshot captured after filling form")
        
        with allure.step("Submit form"):
            registration_page.submit_form()
    
    @allure.title("Test registration with retry mechanism")
    @allure.description("Retry operations that might fail intermittently")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_registration_with_retry(
        self,
        registration_page: RegistrationPage,
        get_test_data,
        retry_helper,
        base_url: str
    ):
        """Test with retry mechanism for flaky operations"""
        
        data = get_test_data('test_registration_valid_user')
        
        with allure.step("Navigate with retry"):
            def navigate():
                registration_page.open(f"{base_url}/register")
                if not registration_page.is_registration_form_displayed():
                    raise Exception("Form not displayed")
            
            retry_helper(navigate, max_attempts=3, delay=2.0)
        
        with allure.step("Fill and submit form"):
            registration_page.fill_registration_form(data)
            registration_page.submit_form()
    
    @allure.title("Test registration with wait helpers")
    @allure.description("Use custom wait conditions")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_registration_with_wait_helpers(
        self,
        registration_page: RegistrationPage,
        get_test_data,
        wait_helper,
        base_url: str
    ):
        """Test using custom wait helpers"""
        
        data = get_test_data('test_registration_valid_user')
        
        with allure.step("Navigate and wait for URL"):
            registration_page.open(f"{base_url}/register")
            wait_helper.for_url_contains("/register")
        
        with allure.step("Fill form"):
            registration_page.fill_registration_form(data)
        
        with allure.step("Submit and wait"):
            registration_page.submit_form()
            # Wait for success page
            wait_helper.for_url_contains("/success")
    
    @allure.title("Test registration with console monitoring")
    @allure.description("Capture and verify browser console messages")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_registration_with_console_monitoring(
        self,
        registration_page: RegistrationPage,
        get_test_data,
        console_messages,
        base_url: str
    ):
        """Test while monitoring browser console"""
        
        data = get_test_data('test_registration_valid_user')
        
        with allure.step("Navigate to registration page"):
            registration_page.open(f"{base_url}/register")
        
        with allure.step("Fill and submit form"):
            registration_page.fill_registration_form(data)
            registration_page.submit_form()
        
        with allure.step("Check for console errors"):
            errors = [msg for msg in console_messages if msg['type'] == 'error']
            
            if errors:
                logger.warning(f"Found {len(errors)} console errors")
                for error in errors:
                    logger.warning(f"Console error: {error['text']}")
            else:
                logger.success("No console errors found")
            
            # You can assert no errors if needed
            # assert len(errors) == 0, f"Found {len(errors)} console errors"
    
    @allure.title("Test registration skipped in production")
    @allure.description("Demonstrate environment-based test skipping")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_registration_skip_in_prod(
        self,
        registration_page: RegistrationPage,
        get_test_data,
        skip_if_environment,
        base_url: str
    ):
        """Test that should skip in production environment"""
        
        # Skip if running in production
        skip_if_environment(['prod', 'production'])
        
        data = get_test_data('test_registration_valid_user')
        
        with allure.step("Execute test (not in production)"):
            registration_page.open(f"{base_url}/register")
            registration_page.fill_registration_form(data)
            registration_page.submit_form()
    
    @allure.title("Test registration with custom Allure labels")
    @allure.description("Add custom metadata to Allure report")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_registration_with_allure_labels(
        self,
        registration_page: RegistrationPage,
        get_test_data,
        allure_labels,
        base_url: str
    ):
        """Test with custom Allure labels and links"""
        
        # Add custom labels
        allure_labels.add('component', 'User Registration')
        allure_labels.add('owner', 'QA Team')
        allure_labels.add('layer', 'UI')
        
        # Add links
        allure_labels.add_link('Jira Ticket', 'https://jira.example.com/PROJ-123')
        allure_labels.add_issue('BUG-456', 'https://jira.example.com/BUG-456')
        allure_labels.add_testcase('TC-789', 'https://testrail.example.com/TC-789')
        
        data = get_test_data('test_registration_valid_user')
        
        with allure.step("Execute registration test"):
            registration_page.open(f"{base_url}/register")
            registration_page.fill_registration_form(data)
            registration_page.submit_form()
    
    @allure.title("Test registration with temporary file upload")
    @allure.description("Create and upload temporary file")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_registration_with_file_upload(
        self,
        registration_page: RegistrationPage,
        get_test_data,
        temp_file,
        base_url: str
    ):
        """Test file upload with temporary file"""
        
        data = get_test_data('test_registration_complete_registration')
        
        with allure.step("Create temporary file"):
            # Create a dummy profile picture file
            file_path = temp_file("profile.txt", "This is a test profile picture")
            logger.info(f"Created temporary file: {file_path}")
        
        with allure.step("Navigate and fill form"):
            registration_page.open(f"{base_url}/register")
            
            # Add file path to data
            data['profile_picture'] = str(file_path)
            registration_page.fill_registration_form(data)
        
        with allure.step("Submit form"):
            registration_page.submit_form()


# Example of parametrized test using test data
@allure.feature("User Registration - Parametrized")
@allure.story("Multiple Registration Scenarios")
@pytest.mark.gui
@pytest.mark.regression
class TestRegistrationParametrized:
    """Parametrized tests using different datasets"""
    
    @pytest.mark.parametrize("dataset_name", [
        "valid_user_1",
        "valid_user_2",
        "complete_registration"
    ])
    @allure.title("Test registration with dataset: {dataset_name}")
    def test_registration_multiple_users(
        self,
        registration_page: RegistrationPage,
        get_data_from_file,
        base_url: str,
        dataset_name: str
    ):
        """Test registration with multiple user datasets"""
        
        with allure.step(f"Get test data for: {dataset_name}"):
            data = get_data_from_file('registration_data.json', dataset_name)
        
        with allure.step("Execute registration"):
            registration_page.open(f"{base_url}/register")
            registration_page.fill_registration_form