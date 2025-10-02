import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import Dict, Any
from loguru import logger


class RegistrationPage(BasePage):
    """Page Object Model for Registration Form"""
    
    # Define field mapping with locators and types
    # Add new fields here when the form changes - no need to modify methods
    FIELD_MAPPING = {
        'first_name': {
            'locator': '#firstName',
            'type': 'textbox'
        },
        'last_name': {
            'locator': '#lastName',
            'type': 'textbox'
        },
        'email': {
            'locator': '#email',
            'type': 'textbox'
        },
        'password': {
            'locator': '#password',
            'type': 'textbox'
        },
        'confirm_password': {
            'locator': '#confirmPassword',
            'type': 'textbox'
        },
        'phone': {
            'locator': '#phone',
            'type': 'textbox'
        },
        'date_of_birth': {
            'locator': '#dob',
            'type': 'textbox'
        },
        'bio': {
            'locator': '#bio',
            'type': 'textarea'
        },
        'gender': {
            'locator': 'input[name="gender"][value="{value}"]',  # Dynamic locator
            'type': 'radio'
        },
        'country': {
            'locator': '#country',
            'type': 'dropdown',
            'select_by': 'value'
        },
        'terms_conditions': {
            'locator': '#terms',
            'type': 'checkbox'
        },
        'newsletter': {
            'locator': '#newsletter',
            'type': 'checkbox'
        },
        'profile_picture': {
            'locator': '#profilePicture',
            'type': 'file'
        }
    }
    
    # Page-specific locators
    SUBMIT_BUTTON = '#submitBtn'
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
        
        # Handle special case for radio buttons with dynamic values
        modified_mapping = self.FIELD_MAPPING.copy()
        if 'gender' in data:
            gender_value = data['gender']
            modified_mapping['gender']['locator'] = \
                modified_mapping['gender']['locator'].format(value=gender_value)
        
        # Use the generic fill_form_data method from BasePage
        self.fill_form_data(modified_mapping, data)
        
        logger.success("Registration form filled successfully")
    
    @allure.step("Submit registration form")
    def submit_form(self) -> None:
        """Submit the registration form"""
        logger.info("Submitting registration form")
        self.actions.click(self.SUBMIT_BUTTON)
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
    
    @allure.step("Clear field: {field_name}")
    def clear_field(self, field_name: str) -> None:
        """Clear a specific field"""
        if field_name in self.FIELD_MAPPING:
            locator = self.FIELD_MAPPING[field_name]['locator']
            self.page.locator(locator).clear()
            logger.success(f"Cleared field: {field_name}")
        else:
            logger.error(f"Field '{field_name}' not found in mapping")
            raise ValueError(f"Field '{field_name}' not found")
    
    @allure.step("Get field value: {field_name}")
    def get_field_value(self, field_name: str) -> str:
        """Get the value of a specific field"""
        if field_name in self.FIELD_MAPPING:
            locator = self.FIELD_MAPPING[field_name]['locator']
            value = self.page.locator(locator).input_value()
            logger.info(f"Field '{field_name}' value: {value}")
            return value
        else:
            logger.error(f"Field '{field_name}' not found in