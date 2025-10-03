import allure
from playwright.sync_api import Page
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