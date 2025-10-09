import allure
from playwright.sync_api import Page,expect
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
    
    @allure.step("Wait for network idle")
    def wait_for_network_idle(self, timeout: int = None) -> None:
        """Wait for network to be idle (useful for SPAs)"""
        self.page.wait_for_load_state("networkidle", timeout=timeout or 30000)
        logger.success("Network idle")
    
    def fill_form_data(self, field_mapping: Dict[str, str], data: Dict[str, Any]) -> None:
        """
        Generic method to fill form data based on field type and method
        
        Args:
            field_mapping: Dictionary mapping field names to locators, types, and methods
                Example: {
                    'username': {
                        'locator': 'Username',
                        'type': 'textbox',
                        'method': 'get_by_label'
                    },
                    'email': {
                        'locator': '#email',
                        'type': 'textbox',
                        'method': 'locator'
                    }
                }
            data: Dictionary containing the actual data to fill
                Example: {
                    'username': 'john_doe',
                    'email': 'john@example.com'
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
            method = field_config.get('method', 'locator')  # Default to CSS locator
            exact = field_config.get('exact', False)  # For exact text matching
            
            # Handle dynamic locators (e.g., gender radio with {value})
            if '{' in locator and isinstance(field_value, str):
                locator = locator.format(value=field_value)
            
            try:
                with allure.step(f"Filling field: {field_name}"):
                    # Handle different locator methods
                    if method == 'get_by_label':
                        self._fill_by_label(field_type, locator, field_value, exact)
                    
                    elif method == 'get_by_placeholder':
                        self._fill_by_placeholder(field_type, locator, field_value)
                    
                    elif method == 'get_by_role':
                        self._fill_by_role(field_type, locator, field_value, exact)
                    
                    elif method == 'get_by_text':
                        self._fill_by_text(field_type, locator, field_value, exact)
                    
                    else:  # Default to CSS/XPath locator
                        self._fill_by_locator(field_type, locator, field_value, field_config)
                        
            except Exception as e:
                logger.error(f"Error filling field '{field_name}': {str(e)}")
                allure.attach(
                    str(e),
                    name=f"Error filling {field_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise
        
        logger.success("Successfully filled all form data")
    
    def _fill_by_label(self, field_type: str, locator: str, value: Any, exact: bool) -> None:
        """Fill field using get_by_label"""
        if field_type in ['textbox', 'textarea']:
            self.actions.fill_by_label(locator, str(value), exact=exact)
        elif field_type == 'checkbox':
            if bool(value):
                self.actions.check_by_label(locator, exact=exact)
            else:
                self.actions.uncheck_by_label(locator, exact=exact)
        elif field_type == 'radio':
            self.actions.check_by_label(locator, exact=exact)
    
    def _fill_by_placeholder(self, field_type: str, locator: str, value: Any) -> None:
        """Fill field using get_by_placeholder"""
        if field_type in ['textbox', 'textarea']:
            self.actions.fill_by_placeholder(locator, str(value))
    
    def _fill_by_role(self, field_type: str, locator: str, value: Any, exact: bool) -> None:
        """Fill field using get_by_role"""
        if field_type == 'button':
            if bool(value):
                self.actions.click_by_role('button', name=locator, exact=exact)
        elif field_type == 'link':
            if bool(value):
                self.actions.click_by_role('link', name=locator, exact=exact)
        elif field_type == 'textbox':
            element = self.page.get_by_role('textbox', name=locator, exact=exact)
            element.fill(str(value))
    
    def _fill_by_text(self, field_type: str, locator: str, value: Any, exact: bool) -> None:
        """Fill field using get_by_text"""
        if bool(value):
            self.actions.click_by_text(locator, exact=exact)
    
    def _fill_by_locator(self, field_type: str, locator: str, value: Any, field_config: Dict) -> None:
        """Fill field using traditional CSS/XPath locator or handle special dropdown types"""
        
        # ==========================================
        # CUSTOM DROPDOWNS (NON-SELECT TAG)
        # ==========================================
        if field_type == 'custom_dropdown_iframe':
            # Custom dropdown inside iframe using label
            iframe_loc = field_config.get('iframe_locator')
            label = field_config.get('label')
            placeholder = field_config.get('placeholder')
            exact = field_config.get('exact', True)
            
            if label:
                self.actions.select_custom_dropdown_by_label_in_iframe(
                    iframe_loc, label, str(value), exact
                )
            elif placeholder:
                self.actions.select_custom_dropdown_by_placeholder_in_iframe(
                    iframe_loc, placeholder, str(value), exact
                )
            else:
                raise ValueError(f"Custom dropdown in iframe must have 'label' or 'placeholder'")
        
        elif field_type == 'custom_dropdown':
            # Custom dropdown without iframe using label
            label = field_config.get('label')
            exact = field_config.get('exact', True)
            
            if label:
                self.actions.select_custom_dropdown_by_label(label, str(value), exact)
            else:
                raise ValueError(f"Custom dropdown must have 'label'")
        
        # ==========================================
        # STANDARD SELECT TAG DROPDOWNS
        # ==========================================
        elif field_type == 'dropdown':
            # Check if it's in iframe
            if 'iframe_locator' in field_config:
                iframe_loc = field_config['iframe_locator']
                label = field_config.get('label')
                
                if label:
                    # Select dropdown by label in iframe
                    if 'select_by' in field_config:
                        select_by = field_config['select_by']
                        if select_by == 'value':
                            self.actions.select_dropdown_by_label_in_iframe(
                                iframe_loc, label, value=str(value)
                            )
                        elif select_by == 'label':
                            self.actions.select_dropdown_by_label_in_iframe(
                                iframe_loc, label, label=str(value)
                            )
                        elif select_by == 'index':
                            self.actions.select_dropdown_by_label_in_iframe(
                                iframe_loc, label, index=int(value)
                            )
                    else:
                        # Default to value
                        self.actions.select_dropdown_by_label_in_iframe(
                            iframe_loc, label, value=str(value)
                        )
                else:
                    raise ValueError("Dropdown in iframe must have 'label'")
            else:
                # Regular dropdown (not in iframe)
                if 'select_by' in field_config:
                    select_by = field_config['select_by']
                    if select_by == 'value':
                        self.actions.select_dropdown(locator, value=str(value))
                    elif select_by == 'label':
                        self.actions.select_dropdown(locator, label=str(value))
                    elif select_by == 'index':
                        self.actions.select_dropdown(locator, index=int(value))
                else:
                    self.actions.select_dropdown(locator, value=str(value))
        
        # ==========================================
        # OTHER FIELD TYPES
        # ==========================================
        elif field_type == 'textbox':
            self.actions.fill_textbox(locator, str(value))
        
        elif field_type == 'textarea':
            self.actions.fill_textarea(locator, str(value))
        
        elif field_type == 'radio':
            self.actions.select_radio(locator)
        
        elif field_type == 'checkbox':
            self.actions.select_checkbox(locator, check=bool(value))
        
        elif field_type == 'file':
            self.actions.upload_file(locator, str(value))
        
        elif field_type == 'link':
            if bool(value):
                self.actions.click(locator)
        
        else:
            logger.warning(f"Unknown field type '{field_type}'")

        
    def verify_form_data(
        self, 
        field_mapping: Dict[str, Any], 
        expected_data: Dict[str, Any],
        timeout: int = 5000
    ) -> None:
        """
        Generic method to verify form data based on field type and method
        
        Args:
            field_mapping: Same structure as fill_form_data
            expected_data: Dictionary containing expected values to verify
            timeout: Timeout for assertions in milliseconds
        """
        logger.info("Starting to verify form data")
        
        for field_name, expected_value in expected_data.items():
            if field_name not in field_mapping:
                logger.warning(f"Field '{field_name}' not found in mapping, skipping verification")
                continue
            
            field_config = field_mapping[field_name]
            locator = field_config['locator']
            field_type = field_config['type'].lower()
            method = field_config.get('method', 'locator')
            exact = field_config.get('exact', False)
            
            # Handle dynamic locators
            if '{' in locator and isinstance(expected_value, str):
                locator = locator.format(value=expected_value)
            
            try:
                with allure.step(f"Verifying field: {field_name}"):
                    # Get the element based on method
                    element = self._get_element_by_method(method, field_type, locator, exact)
                    
                    # Verify based on field type
                    self._verify_field_value(element, field_type, expected_value, timeout)
                    
                    logger.success(f"✓ Field '{field_name}' verified")
                    
            except AssertionError as e:
                logger.error(f"✗ Verification failed for '{field_name}': {str(e)}")
                allure.attach(
                    str(e),
                    name=f"Verification failed: {field_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise
        
        logger.success("All form data verified successfully")
    
    def _get_element_by_method(self, method: str, field_type: str, locator: str, exact: bool):
        """Get element based on locator method"""
        if method == 'get_by_label':
            return self.page.get_by_label(locator, exact=exact)
        elif method == 'get_by_placeholder':
            return self.page.get_by_placeholder(locator)
        elif method == 'get_by_role':
            return self.page.get_by_role(field_type, name=locator, exact=exact)
        elif method == 'get_by_text':
            return self.page.get_by_text(locator, exact=exact)
        else:
            return self.page.locator(locator)
    
    def _verify_field_value(self, element, field_type: str, expected_value: Any, timeout: int):
        """Verify field value based on type"""
        if field_type in ['textbox', 'textarea']:
            expect(element).to_have_value(str(expected_value), timeout=timeout)
        
        elif field_type == 'checkbox':
            if bool(expected_value):
                expect(element).to_be_checked(timeout=timeout)
            else:
                expect(element).not_to_be_checked(timeout=timeout)
        
        elif field_type == 'radio':
            expect(element).to_be_checked(timeout=timeout)
        
        elif field_type == 'dropdown':
            # Verify selected option
            expect(element).to_have_value(str(expected_value), timeout=timeout)
        
        elif field_type == 'link':
            # Verify link is visible
            if bool(expected_value):
                expect(element).to_be_visible(timeout=timeout)
        
        elif field_type == 'button':
            # Verify button is enabled
            if bool(expected_value):
                expect(element).to_be_enabled(timeout=timeout)