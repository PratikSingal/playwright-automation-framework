import allure
from playwright.sync_api import Page , expect
from pages.base_page import BasePage
from typing import Dict, Any
from loguru import logger


class RegistrationPage(BasePage):
    """Page Object Model for Registration Form"""
    
    # Define field mapping with locators, types, and methods
    FIELD_MAPPING = {
        # Using get_by_label (recommended for form inputs with labels)
        'first_name': {
            'locator': 'First Name',
            'type': 'textbox',
            'method': 'get_by_label'
        },
        'last_name': {
            'locator': 'Last Name',
            'type': 'textbox',
            'method': 'get_by_label'
        },
        
        # Using get_by_placeholder (when no label exists)
        'email': {
            'locator': 'Enter your email',
            'type': 'textbox',
            'method': 'get_by_placeholder'
        },
        
        # Using traditional CSS locator
        'password': {
            'locator': '#password',
            'type': 'textbox',
            'method': 'locator'
        },
        'confirm_password': {
            'locator': '#confirmPassword',
            'type': 'textbox',
            'method': 'locator'
        },
        
        # Using get_by_label for phone
        'phone': {
            'locator': 'Phone Number',
            'type': 'textbox',
            'method': 'get_by_label'
        },
        
        'date_of_birth': {
            'locator': '#dob',
            'type': 'textbox',
            'method': 'locator'
        },
        
        'bio': {
            'locator': '#bio',
            'type': 'textarea',
            'method': 'locator'
        },
        
        # Dynamic radio button with CSS locator
        'gender': {
            'locator': 'input[name="gender"][value="{value}"]',
            'type': 'radio',
            'method': 'locator'
        },
        
        # Dropdown with CSS
        'country': {
            'locator': '#country',
            'type': 'dropdown',
            'method': 'locator',
            'select_by': 'value'
        },
        
        # Checkbox using get_by_label
        'terms_conditions': {
            'locator': 'I agree to terms and conditions',
            'type': 'checkbox',
            'method': 'get_by_label'
        },
        
        'newsletter': {
            'locator': '#newsletter',
            'type': 'checkbox',
            'method': 'locator'
        },
        
        'profile_picture': {
            'locator': '#profilePicture',
            'type': 'file',
            'method': 'locator'
        },
        
        # Link using get_by_role
        'privacy_policy': {
            'locator': 'Privacy Policy',
            'type': 'link',
            'method': 'get_by_role'
        }
    }
    
    # Page-specific locators
    SUBMIT_BUTTON = 'Submit'  # Using accessible name
    SUCCESS_MESSAGE = '.success-message'
    ERROR_MESSAGE = '.error-message'
    REGISTRATION_FORM = '#registrationForm'
    
    def __init__(self, page: Page):
        super().__init__(page)
        logger.info("Initialized Registration Page")
    
    @allure.step("Open registration page")
    def open(self, url: str) -> None:
        """Open the registration page"""
        self.navigate_to(url)
        self.actions.wait_for_element(self.REGISTRATION_FORM, state="visible")
    
    @allure.step("Fill registration form")
    def fill_registration_form(self, data: Dict[str, Any]) -> None:
        """
        Fill the registration form with provided data
        
        Args:
            data: Dictionary containing form field values
                Example: {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john@example.com',
                    'password': 'Test@123',
                    'gender': 'male',
                    'terms_conditions': True
                }
        """
        logger.info("Filling registration form with data")
        
        # Use the generic fill_form_data method from BasePage
        # No need for special handling - dynamic locators handled automatically
        self.fill_form_data(self.FIELD_MAPPING, data)
        
        logger.success("Registration form filled successfully")
    
    @allure.step("Submit registration form")
    def submit_form(self) -> None:
        """Submit the registration form"""
        logger.info("Submitting registration form")
        # Using accessible button name
        self.actions.click_button(self.SUBMIT_BUTTON)
        logger.success("Registration form submitted")
    
    @allure.step("Get success message")
    def get_success_message(self) -> str:
        """Get the success message after registration"""
        logger.info("Retrieving success message")
        self.actions.wait_for_element(self.SUCCESS_MESSAGE, state="visible")
        message = self.actions.get_text(self.SUCCESS_MESSAGE)
        logger.success(f"Success message: {message}")
        return message
    
    @allure.step("Get error message")
    def get_error_message(self) -> str:
        """Get the error message if registration fails"""
        logger.info("Retrieving error message")
        self.actions.wait_for_element(self.ERROR_MESSAGE, state="visible")
        message = self.actions.get_text(self.ERROR_MESSAGE)
        logger.warning(f"Error message: {message}")
        return message
    
    @allure.step("Verify registration form is displayed")
    def is_registration_form_displayed(self) -> bool:
        """Verify if the registration form is displayed"""
        is_displayed = self.actions.is_visible(self.REGISTRATION_FORM)
        logger.info(f"Registration form displayed: {is_displayed}")
        return is_displayed
    
    @allure.step("Verify registration form data")
    def verify_registration_form(self, expected_data: Dict[str, Any]) -> None:
        """
        Verify the registration form contains expected data
        
        Args:
            expected_data: Dictionary containing expected field values
                Example: {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john@example.com',
                    'terms_conditions': True
                }
        """
        logger.info("Verifying registration form data")
        self.verify_form_data(self.FIELD_MAPPING, expected_data)
        logger.success("Registration form data verified successfully")
    
    @allure.step("Verify successful registration")
    def verify_successful_registration(self, expected_email: str = None) -> None:
        """Verify registration was successful"""
        
        # Check success message
        success_locator = self.page.locator(self.SUCCESS_MESSAGE)
        expect(success_locator).to_be_visible(timeout=10000)
        expect(success_locator).to_contain_text("successful", ignore_case=True)
        logger.success("✓ Success message verified")
        
        # Check URL changed
        expect(self.page).not_to_have_url("**/register")
        logger.success("✓ Navigated away from registration page")
        
        # Check email if provided
        if expected_email:
            email_locator = self.page.locator('.user-email')
            expect(email_locator).to_contain_text(expected_email)
            logger.success(f"✓ Email {expected_email} verified")
    
    @allure.step("Verify registration failed")
    def verify_registration_failed(self, expected_error: str = None) -> None:
        """Verify registration failed with error message"""
        
        # Check error message exists
        error_locator = self.page.locator(self.ERROR_MESSAGE)
        expect(error_locator).to_be_visible(timeout=10000)
        logger.warning("Error message displayed")
        
        # Check specific error if provided
        if expected_error:
            expect(error_locator).to_contain_text(expected_error, ignore_case=True)
            logger.success(f"✓ Expected error '{expected_error}' verified")
        
        # Verify still on registration page
        expect(self.page).to_have_url("**/register")
        logger.success("✓ Still on registration page")
    
    @allure.step("Verify all required fields are visible")
    def verify_required_fields_visible(self, required_fields: List[str]) -> None:
        """Verify all required fields are visible on the form"""
        for field_name in required_fields:
            if field_name not in self.FIELD_MAPPING:
                logger.warning(f"Field '{field_name}' not in mapping")
                continue
            
            field_config = self.FIELD_MAPPING[field_name]
            locator = field_config['locator']
            method = field_config.get('method', 'locator')
            
            element = self._get_element_by_method(
                method, 
                field_config['type'], 
                locator, 
                field_config.get('exact', False)
            )
            
            expect(element).to_be_visible()
            logger.success(f"✓ Field '{field_name}' is visible")