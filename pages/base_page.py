import allure
from playwright.sync_api import Page
from typing import Dict, Any
from actions.generic_actions import GenericActions
from loguru import logger


class BasePage:
    """Base page class that all page objects inherit from"""
    
    def __init__(self, page: Page):
        self.page = page
        self.actions = GenericActions(page)
    
    @allure.step("Navigate to URL: {url}")
    def navigate_to(self, url: str) -> None:
        """Navigate to a URL"""
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
        logger.success(f"Successfully navigated to: {url}")
    
    @allure.step("Get page title")
    def get_title(self) -> str:
        """Get the page title"""
        title = self.page.title()
        logger.info(f"Page title: {title}")
        return title
    
    @allure.step("Get current URL")
    def get_current_url(self) -> str:
        """Get the current URL"""
        url = self.page.url
        logger.info(f"Current URL: {url}")
        return url
    
    def fill_form_data(self, field_mapping: Dict[str, str], data: Dict[str, Any]) -> None:
        """
        Generic method to fill form data based on field type
        
        Args:
            field_mapping: Dictionary mapping field names to locators and types
                Example: {
                    'username': {'locator': '#username', 'type': 'textbox'},
                    'bio': {'locator': '#bio', 'type': 'textarea'},
                    'gender': {'locator': '#male', 'type': 'radio'},
                    'terms': {'locator': '#terms', 'type': 'checkbox'}
                }
            data: Dictionary containing the actual data to fill
                Example: {
                    'username': 'john_doe',
                    'bio': 'This is my bio',
                    'gender': 'male',
                    'terms': True
                }
        """
        logger.info("Starting to fill form data")
        
        for field_name, field_value in data.items():
            if field_name not in field_mapping:
                logger.warning(f"Field '{field_name}' not found in mapping, skipping")
                continue
            
            field_config = field_mapping[field_name]
            locator = field_config['locator']
            field_type = field_config['type'].lower()
            
            try:
                with allure.step(f"Filling field: {field_name}"):
                    if field_type == 'textbox':
                        self.actions.fill_textbox(locator, str(field_value))
                    
                    elif field_type == 'textarea':
                        self.actions.fill_textarea(locator, str(field_value))
                    
                    elif field_type == 'radio':
                        self.actions.select_radio(locator)
                    
                    elif field_type == 'checkbox':
                        self.actions.select_checkbox(locator, check=bool(field_value))
                    
                    elif field_type == 'dropdown':
                        if 'select_by' in field_config:
                            select_by = field_config['select_by']
                            if select_by == 'value':
                                self.actions.select_dropdown(locator, value=str(field_value))
                            elif select_by == 'label':
                                self.actions.select_dropdown(locator, label=str(field_value))
                            elif select_by == 'index':
                                self.actions.select_dropdown(locator, index=int(field_value))
                        else:
                            self.actions.select_dropdown(locator, value=str(field_value))
                    
                    elif field_type == 'file':
                        self.actions.upload_file(locator, str(field_value))
                    
                    elif field_type == 'link':
                        # Click link if value is True
                        if bool(field_value):
                            self.actions.click(locator)
                    
                    else:
                        logger.warning(f"Unknown field type '{field_type}' for field '{field_name}'")
                        
            except Exception as e:
                logger.error(f"Error filling field '{field_name}': {str(e)}")
                allure.attach(
                    str(e),
                    name=f"Error filling {field_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise
        
        logger.success("Successfully filled all form data")