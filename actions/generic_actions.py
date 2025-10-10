import allure
from playwright.sync_api import Page, Locator, expect
from typing import List, Optional, Union
from loguru import logger


class GenericActions:
    """Generic actions class for common web element interactions"""
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 30000
    
    # ==================== CSS Locator Methods ====================
    
    @allure.step("Fill textbox: {locator} with value: {value}")
    def fill_textbox(self, locator: str, value: str, clear_first: bool=True) -> None:
        """Fill a textbox with the given value"""
        try:
            logger.info(f"Filling textbox '{locator}' with value '{value}'")
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=self.timeout)
            
            if clear_first:
                element.clear()
            
            element.fill(value)
            logger.success(f"Successfully filled textbox '{locator}'")
        except Exception as e:
            logger.error(f"Failed to fill textbox '{locator}': {str(e)}")
            raise
    
    @allure.step("Fill textarea: {locator} with value: {value}")
    def fill_textarea(self, locator: str, value: str, clear_first: bool=True) -> None:
        """Fill a textarea with the given value"""
        try:
            logger.info(f"Filling textarea '{locator}' with value '{value}'")
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=self.timeout)
            
            if clear_first:
                element.clear()
            
            element.fill(value)
            logger.success(f"Successfully filled textarea '{locator}'")
        except Exception as e:
            logger.error(f"Failed to fill textarea '{locator}': {str(e)}")
            raise
    
    @allure.step("Select radio button: {locator}")
    def select_radio(self, locator: str) -> None:
        """Select a radio button"""
        try:
            logger.info(f"Selecting radio button '{locator}'")
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=self.timeout)
            
            if not element.is_checked():
                element.check()
            
            logger.success(f"Successfully selected radio button '{locator}'")
        except Exception as e:
            logger.error(f"Failed to select radio button '{locator}': {str(e)}")
            raise
    
    @allure.step("Select checkbox: {locator}")
    def select_checkbox(self, locator: str, check: bool=True) -> None:
        """Check or uncheck a checkbox"""
        try:
            action = "Checking" if check else "Unchecking"
            logger.info(f"{action} checkbox '{locator}'")
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=self.timeout)
            
            if check:
                element.check()
            else:
                element.uncheck()
            
            logger.success(f"Successfully {action.lower()}ed checkbox '{locator}'")
        except Exception as e:
            logger.error(f"Failed to modify checkbox '{locator}': {str(e)}")
            raise
    
    @allure.step("Click element: {locator}")
    def click(self, locator: str) -> None:
        """Click an element"""
        try:
            logger.info(f"Clicking element '{locator}'")
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=self.timeout)
            element.click()
            logger.success(f"Successfully clicked element '{locator}'")
        except Exception as e:
            logger.error(f"Failed to click element '{locator}': {str(e)}")
            raise
    
    # ==================== Accessibility-Based Methods ====================
    
    @allure.step("Fill by label: {label}")
    def fill_by_label(self, label: str, value: str, exact: bool=False) -> None:
        """Fill input using associated label"""
        try:
            logger.info(f"Filling input with label '{label}'")
            self.page.get_by_label(label, exact=exact).fill(value)
            logger.success(f"Filled input with label '{label}'")
        except Exception as e:
            logger.error(f"Failed to fill input with label '{label}': {str(e)}")
            raise
    
    @allure.step("Fill by placeholder: {placeholder}")
    def fill_by_placeholder(self, placeholder: str, value: str) -> None:
        """Fill input by placeholder text"""
        try:
            logger.info(f"Filling input with placeholder '{placeholder}'")
            self.page.get_by_placeholder(placeholder).fill(value)
            logger.success(f"Filled input with placeholder '{placeholder}'")
        except Exception as e:
            logger.error(f"Failed to fill by placeholder '{placeholder}': {str(e)}")
            raise
    
    @allure.step("Click by role: {role}")
    def click_by_role(self, role: str, name: str=None, exact: bool=False) -> None:
        """Click element using accessibility role"""
        try:
            logger.info(f"Clicking {role}" + (f" with name '{name}'" if name else ""))
            if name:
                self.page.get_by_role(role, name=name, exact=exact).click()
            else:
                self.page.get_by_role(role).click()
            logger.success(f"Clicked {role}")
        except Exception as e:
            logger.error(f"Failed to click {role}: {str(e)}")
            raise
    
    @allure.step("Click button: {name}")
    def click_button(self, name: str, exact: bool=False) -> None:
        """Click button by accessible name"""
        try:
            logger.info(f"Clicking button '{name}'")
            self.page.get_by_role("button", name=name, exact=exact).click()
            logger.success(f"Clicked button '{name}'")
        except Exception as e:
            logger.error(f"Failed to click button '{name}': {str(e)}")
            raise
    
    @allure.step("Click link: {name}")
    def click_link(self, name: str, exact: bool=False) -> None:
        """Click link by accessible name"""
        try:
            logger.info(f"Clicking link '{name}'")
            self.page.get_by_role("link", name=name, exact=exact).click()
            logger.success(f"Clicked link '{name}'")
        except Exception as e:
            logger.error(f"Failed to click link '{name}': {str(e)}")
            raise
    
    @allure.step("Check by label: {label}")
    def check_by_label(self, label: str, exact: bool=False) -> None:
        """Check checkbox/radio by label"""
        try:
            logger.info(f"Checking '{label}'")
            self.page.get_by_label(label, exact=exact).check()
            logger.success(f"Checked '{label}'")
        except Exception as e:
            logger.error(f"Failed to check '{label}': {str(e)}")
            raise
    
    @allure.step("Uncheck by label: {label}")
    def uncheck_by_label(self, label: str, exact: bool=False) -> None:
        """Uncheck checkbox by label"""
        try:
            logger.info(f"Unchecking '{label}'")
            self.page.get_by_label(label, exact=exact).uncheck()
            logger.success(f"Unchecked '{label}'")
        except Exception as e:
            logger.error(f"Failed to uncheck '{label}': {str(e)}")
            raise
    
    @allure.step("Click by text: {text}")
    def click_by_text(self, text: str, exact: bool=False) -> None:
        """Click element by visible text"""
        try:
            logger.info(f"Clicking element with text '{text}'")
            self.page.get_by_text(text, exact=exact).click()
            logger.success(f"Clicked element with text '{text}'")
        except Exception as e:
            logger.error(f"Failed to click by text '{text}': {str(e)}")
            raise
    
    # ==================== Assertion Methods ====================
    
    @allure.step("Assert text equals: {expected_text}")
    def assert_text_equals(self, locator: str, expected_text: str, timeout: int=None) -> None:
        """Assert element text matches expected with auto-retry"""
        try:
            element = self.page.locator(locator)
            expect(element).to_have_text(expected_text, timeout=timeout or self.timeout)
            logger.success(f"Text assertion passed for '{locator}'")
        except AssertionError as e:
            logger.error(f"Text assertion failed for '{locator}': {str(e)}")
            raise
    
    @allure.step("Assert visible: {locator}")
    def assert_visible(self, locator: str, timeout: int=None) -> None:
        """Assert element is visible with auto-retry"""
        try:
            element = self.page.locator(locator)
            expect(element).to_be_visible(timeout=timeout or self.timeout)
            logger.success(f"Element '{locator}' is visible")
        except AssertionError as e:
            logger.error(f"Visibility assertion failed for '{locator}': {str(e)}")
            raise
    
    @allure.step("Assert enabled: {locator}")
    def assert_enabled(self, locator: str) -> None:
        """Assert element is enabled"""
        try:
            element = self.page.locator(locator)
            expect(element).to_be_enabled()
            logger.success(f"Element '{locator}' is enabled")
        except AssertionError as e:
            logger.error(f"Enabled assertion failed for '{locator}': {str(e)}")
            raise
    
    # ==================== Existing Methods ====================
    
    @allure.step("Double click element: {locator}")
    def double_click(self, locator: str) -> None:
        """Double click an element"""
        try:
            logger.info(f"Double clicking element '{locator}'")
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=self.timeout)
            element.dblclick()
            logger.success(f"Successfully double clicked element '{locator}'")
        except Exception as e:
            logger.error(f"Failed to double click element '{locator}': {str(e)}")
            raise
    
    @allure.step("Get text from element: {locator}")
    def get_text(self, locator: str) -> str:
        """Get text from an element"""
        try:
            logger.info(f"Getting text from element '{locator}'")
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=self.timeout)
            text = element.inner_text()
            logger.success(f"Successfully retrieved text from '{locator}': {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from '{locator}': {str(e)}")
            raise
    
    @allure.step("Verify element is visible: {locator}")
    def is_visible(self, locator: str) -> bool:
        """Check if element is visible"""
        try:
            logger.info(f"Checking visibility of element '{locator}'")
            element = self.page.locator(locator)
            is_visible = element.is_visible()
            logger.success(f"Element '{locator}' visibility: {is_visible}")
            return is_visible
        except Exception as e:
            logger.error(f"Failed to check visibility of '{locator}': {str(e)}")
            return False
    
    @allure.step("Wait for element: {locator}")
    def wait_for_element(self, locator: str, state: str="visible") -> None:
        """Wait for element to reach a specific state"""
        try:
            logger.info(f"Waiting for element '{locator}' to be {state}")
            element = self.page.locator(locator)
            element.wait_for(state=state, timeout=self.timeout)
            logger.success(f"Element '{locator}' is now {state}")
        except Exception as e:
            logger.error(f"Element '{locator}' did not reach state '{state}': {str(e)}")
            raise
    
    @allure.step("Upload file: {file_path} to element: {locator}")
    def upload_file(self, locator: str, file_path: str) -> None:
        """Upload a file"""
        try:
            logger.info(f"Uploading file '{file_path}' to element '{locator}'")
            element = self.page.locator(locator)
            element.set_input_files(file_path)
            logger.success(f"Successfully uploaded file to '{locator}'")
        except Exception as e:
            logger.error(f"Failed to upload file to '{locator}': {str(e)}")
            raise
    
    @allure.step("Press key: {key}")
    def press_key(self, key: str, locator: str=None) -> None:
        """Press a keyboard key"""
        try:
            logger.info(f"Pressing key '{key}'")
            if locator:
                element = self.page.locator(locator)
                element.press(key)
            else:
                self.page.keyboard.press(key)
            logger.success(f"Successfully pressed key '{key}'")
        except Exception as e:
            logger.error(f"Failed to press key '{key}': {str(e)}")
            raise
    
    @allure.step("Take screenshot: {name}")
    def take_screenshot(self, name: str) -> None:
        """Take a screenshot"""
        try:
            logger.info(f"Taking screenshot: {name}")
            screenshot_path = f"reports/screenshots/{name}.png"
            self.page.screenshot(path=screenshot_path, full_page=True)
            allure.attach.file(screenshot_path, name=name, attachment_type=allure.attachment_type.PNG)
            logger.success(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    @allure.step("Scroll to element: {locator}")
    def scroll_to_element(self, locator: str) -> None:
        """Scroll to an element"""
        try:
            logger.info(f"Scrolling to element '{locator}'")
            element = self.page.locator(locator)
            element.scroll_into_view_if_needed()
            logger.success(f"Successfully scrolled to element '{locator}'")
        except Exception as e:
            logger.error(f"Failed to scroll to element '{locator}': {str(e)}")
            raise

    # ==========================================
    # CUSTOM DROPDOWN METHODS (NON-SELECT TAG)
    # ==========================================
    
    @allure.step("Select custom dropdown by label in iframe: {label} -> {option_text}")
    def select_custom_dropdown_by_label_in_iframe(
        self,
        iframe_locator: str,
        label: str,
        option_text: str,
        exact: bool=True
    ) -> None:
        """
        Select from custom dropdown (non-select tag) using label inside iframe
        
        Args:
            iframe_locator: Iframe locator (e.g., '#iframeView')
            label: Label text of the dropdown field
            option_text: Option text to select (from data file)
            exact: Exact text match for option
        """
        try:
            logger.info(f"Selecting '{option_text}' from custom dropdown with label '{label}' in iframe")
            frame = self.page.frame_locator(iframe_locator)
            
            # Click dropdown using label
            frame.get_by_label(label).click()
            
            # Wait for dropdown options to appear
            self.page.wait_for_timeout(500)
            
            # Select option by text
            frame.get_by_text(option_text, exact=exact).click()
            
            logger.success(f"Successfully selected '{option_text}' from '{label}' dropdown")
        except Exception as e:
            logger.error(f"Failed to select custom dropdown by label in iframe: {str(e)}")
            raise
    
    @allure.step("Select custom dropdown by label: {label_text} -> {option_text}")
    def select_custom_dropdown_by_label(
        self, 
        label_text: str, 
        option_text: str, 
        input_class: str = "PB_DropDownInput",
        exact: bool = False
    ) -> None:
        """
        Select from custom dropdown (non-select tag) using label (no iframe)
        Configurable for different input classes
        
        Args:
            label_text: Label text of the dropdown field
            option_text: Option text to select (from data file)
            input_class: CSS class of the dropdown input (default: PB_DropDownInput)
            exact: Exact text match for option
        """
        try:
            logger.info(f"Selecting '{option_text}' from dropdown with label '{label_text}' (input class: {input_class})")
            
            # Try multiple XPath strategies to find the dropdown input
            dropdown = None
            strategies = [
                f'//label[contains(text(), "{label_text}")]/following-sibling::*//input[contains(@class, "{input_class}")]',
                f'//label[contains(text(), "{label_text}")]/ancestor::tr[1]//input[contains(@class, "{input_class}")]',
                f'//label[contains(text(), "{label_text}")]/..//input[contains(@class, "{input_class}")]',
                f'//label[contains(text(), "{label_text}")]/parent::td/following-sibling::td//input[contains(@class, "{input_class}")]',
            ]
            
            for i, xpath in enumerate(strategies, 1):
                try:
                    logger.debug(f"Trying strategy {i}: {xpath}")
                    dropdown = self.page.locator(f'xpath={xpath}').first
                    dropdown.wait_for(state="visible", timeout=3000)
                    logger.info(f"✓ Found dropdown using strategy {i}")
                    break
                except Exception as e:
                    logger.debug(f"Strategy {i} failed: {str(e)}")
                    continue
            
            if dropdown is None:
                raise Exception(f"Could not find dropdown with label '{label_text}' and input class '{input_class}'")
            
            # Click dropdown to open options list
            dropdown.click()
            logger.info(f"✓ Dropdown opened")
            
            # Wait for dropdown options to appear
            self.page.wait_for_timeout(500)
            
            # Select option by text
            self.page.get_by_text(option_text, exact=exact).click()
            
            logger.success(f"✓ Successfully selected '{option_text}' from '{label_text}' dropdown")
            
        except Exception as e:
            logger.error(f"✗ Failed to select custom dropdown by label: {str(e)}")
            screenshot_name = f"error_dropdown_{label_text.replace(' ', '_')}_{option_text.replace(' ', '_')}.png"
            self.page.screenshot(path=screenshot_name, full_page=True)
            logger.error(f"Screenshot saved: {screenshot_name}")
            raise


    
    @allure.step("Select custom dropdown by placeholder in iframe: {placeholder} -> {option_text}")
    def select_custom_dropdown_by_placeholder_in_iframe(
        self,
        iframe_locator: str,
        placeholder: str,
        option_text: str,
        exact: bool=True
    ) -> None:
        """
        Select from custom dropdown using placeholder inside iframe
        
        Args:
            iframe_locator: Iframe locator
            placeholder: Placeholder text of the dropdown
            option_text: Option text to select
            exact: Exact text match
        """
        try:
            logger.info(f"Selecting '{option_text}' from dropdown with placeholder '{placeholder}' in iframe")
            frame = self.page.frame_locator(iframe_locator)
            
            # Click dropdown using placeholder
            frame.get_by_placeholder(placeholder).click()
            
            # Wait for options
            self.page.wait_for_timeout(500)
            
            # Select option
            frame.get_by_text(option_text, exact=exact).click()
            
            logger.success(f"Successfully selected '{option_text}'")
        except Exception as e:
            logger.error(f"Failed to select custom dropdown by placeholder in iframe: {str(e)}")
            raise
    
    # ==========================================
    # STANDARD SELECT TAG DROPDOWN METHODS
    # ==========================================
    
    @allure.step("Select dropdown option: {locator}")
    def select_dropdown(self, locator: str, value: str=None, label: str=None, index: int=None) -> None:
        """
        Select an option from standard <select> dropdown by value, label, or index
        
        Args:
            locator: CSS/XPath locator for select element
            value: Value attribute of option
            label: Visible text of option
            index: Index of option (0-based)
        """
        try:
            logger.info(f"Selecting dropdown option from '{locator}'")
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=self.timeout)
            
            if value:
                element.select_option(value=value)
                logger.success(f"Selected option by value: {value}")
            elif label:
                element.select_option(label=label)
                logger.success(f"Selected option by label: {label}")
            elif index is not None:
                element.select_option(index=index)
                logger.success(f"Selected option by index: {index}")
            else:
                raise ValueError("Must provide value, label, or index")
            
        except Exception as e:
            logger.error(f"Failed to select dropdown option from '{locator}': {str(e)}")
            raise
    
    @allure.step("Select dropdown by label in iframe: {label_text}")
    def select_dropdown_by_label_in_iframe(
        self,
        iframe_locator: str,
        label_text: str,
        value: str=None,
        label: str=None,
        index: int=None
    ) -> None:
        """
        Select standard <select> dropdown using its label inside iframe
        
        Args:
            iframe_locator: Iframe locator
            label_text: Label text for the dropdown
            value/label/index: Selection criteria
        """
        try:
            logger.info(f"Selecting <select> dropdown with label '{label_text}' in iframe")
            frame = self.page.frame_locator(iframe_locator)
            element = frame.get_by_label(label_text)
            
            if value:
                element.select_option(value=value)
            elif label:
                element.select_option(label=label)
            elif index is not None:
                element.select_option(index=index)
            else:
                raise ValueError("Must provide value, label, or index")
            
            logger.success(f"Successfully selected from dropdown")
        except Exception as e:
            logger.error(f"Failed to select dropdown by label in iframe: {str(e)}")
            raise

    @allure.step("Click by text with index: {text} at position {index}")
    def click_by_text_at_index(self, text: str, index: int=0, exact: bool=False) -> None:
        """Click element by visible text when multiple matches exist"""
        try:
            logger.info(f"Clicking element with text '{text}' at index {index}")
            self.page.get_by_text(text, exact=exact).nth(index).click()
            logger.success(f"Clicked element with text '{text}' at index {index}")
        except Exception as e:
            logger.error(f"Failed to click by text '{text}' at index {index}: {str(e)}")
            raise


    @allure.step("Select SumoSelect dropdown: {dropdown_name} -> {option_text}")
    def select_sumo_dropdown(
        self,
        dropdown_name: str,
        option_text: str,
        option_index: int = 0,
        exact: bool = False
    ) -> None:
        """
        Generic method to select option from SumoSelect custom dropdown (no iframe)
        
        Args:
            dropdown_name: Name attribute of the select element
            option_text: Option text to select
            option_index: Which occurrence if multiple options have same text
            exact: Use exact text match for option selection
        
        Examples:
            actions.select_sumo_dropdown("accountType", "New Account")
            actions.select_sumo_dropdown("country", "United States")
            actions.select_sumo_dropdown("status", "Active", option_index=1)
        """
        try:
            logger.info(f"Selecting '{option_text}' from SumoSelect dropdown '{dropdown_name}'")
            
            # Step 1: Click the SumoSelect container to open dropdown
            logger.info(f"Opening SumoSelect dropdown '{dropdown_name}'...")
            sumo_select = self.page.locator(f".SumoSelect.sumo_{dropdown_name}")
            sumo_select.wait_for(state="visible", timeout=self.timeout)
            sumo_select.click()
            
            
            # Step 2: Wait for options list
            self.page.locator("ul.options").wait_for(state="visible", timeout=self.timeout)
            
            # Step 3: Click the option
            logger.info(f"Selecting option '{option_text}' at index {option_index}...")
            option = self.page.locator("label").filter(has_text=option_text).nth(option_index)
            option.wait_for(state="visible", timeout=self.timeout)
            option.click()
            
            logger.success(f"✓ Selected '{option_text}' from '{dropdown_name}' dropdown")
            
        except Exception as e:
            logger.error(f"✗ Failed to select option: {str(e)}")
            self.page.screenshot(path=f"error_sumo_{dropdown_name}_{option_text.replace(' ', '_')}.png", full_page=True)
            raise

    @allure.step("Select SumoSelect dropdown in iframe: {dropdown_name} -> {option_text} at index {option_index}")
    def select_sumo_dropdown_in_iframe(
        self,
        iframe_locator: str,
        dropdown_name: str,
        option_text: str,
        option_index: int = 0,
        exact: bool = False
    ) -> None:
        """
        Generic method to select option from SumoSelect custom dropdown inside iframe
        
        This method handles the two-step process:
        1. Click the SumoSelect container to open the dropdown
        2. Click the desired option label
        
        Args:
            iframe_locator: Iframe CSS selector (e.g., '#iframeView')
            dropdown_name: Name attribute of the select element (e.g., 'accountType', 'country', 'status')
            option_text: Option text to select (e.g., 'New Account', 'USA', 'Active')
            option_index: Which occurrence if multiple options have same text (0 = first, 1 = second, etc.)
            exact: Use exact text match for option selection
        
        Examples:
            # Select account type
            actions.select_sumo_dropdown_in_iframe("#iframeView", "accountType", "New Account")
            
            # Select country
            actions.select_sumo_dropdown_in_iframe("#iframeView", "country", "United States")
            
            # Select second occurrence of same text
            actions.select_sumo_dropdown_in_iframe("#iframeView", "accountType", "New Account", option_index=1)
            
            # Exact match
            actions.select_sumo_dropdown_in_iframe("#iframeView", "status", "Active", exact=True)
        """
        try:
            logger.info(f"Selecting '{option_text}' from SumoSelect dropdown '{dropdown_name}' in iframe")
            frame = self.page.frame_locator(iframe_locator)
            
            # Step 1: Click the SumoSelect container to open dropdown
            logger.info(f"Step 1: Opening SumoSelect dropdown '{dropdown_name}'...")
            sumo_select = frame.locator(f".SumoSelect.sumo_{dropdown_name}")
            sumo_select.wait_for(state="visible", timeout=self.timeout)
            sumo_select.click()
            
            
            # Step 2: Wait for options list to be visible
            logger.info("Step 2: Waiting for options to appear...")
            frame.locator(f".SumoSelect.sumo_{dropdown_name} ul.options").wait_for(state="visible")
            
            # Step 3: Click the desired option label
            logger.info(f"Step 3: Selecting option '{option_text}' at index {option_index}...")
            option = frame.locator(f".SumoSelect.sumo_{dropdown_name} label").filter(has_text=option_text).nth(option_index)            option.wait_for(state="visible", timeout=self.timeout)
            option.scroll_into_view_if_needed()
            option.click()
            
            logger.success(f"✓ Successfully selected '{option_text}' from '{dropdown_name}' dropdown")
            
        except Exception as e:
            logger.error(f"✗ Failed to select SumoSelect option '{option_text}' from '{dropdown_name}': {str(e)}")
            screenshot_name = f"error_sumo_{dropdown_name}_{option_text.replace(' ', '_')}_{option_index}.png"
            self.page.screenshot(path=screenshot_name, full_page=True)
            logger.error(f"Screenshot saved: {screenshot_name}")
            raise


    @allure.step("Select dropdown by clicking input: {locator} -> {option_text}")
    def select_dropdown_by_click(
        self, 
        locator: str, 
        option_text: str, 
        exact: bool = False,
        scroll_if_needed: bool = True,
        dropdown_list_class: str = "PB_DropDownList"
    ) -> None:
        """
        Simple dropdown selection - click input, scroll if needed, then select option
        Works with any custom dropdown pattern
        
        Args:
            locator: XPath/CSS locator for the dropdown input
            option_text: Option text to select
            exact: Exact text match for option
            scroll_if_needed: Whether to scroll within dropdown if option not visible
            dropdown_list_class: CSS class of the dropdown list container (for scrolling)
        """
        try:
            logger.info(f"Selecting '{option_text}' from dropdown at '{locator}'")
            
            # Step 1: Click the input to open dropdown
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=self.timeout)
            element.click()
            
            logger.info(f"✓ Dropdown opened")
            
            # Step 2: Wait for dropdown list to appear
            self.page.wait_for_timeout(500)
            
            # Step 3: Try to find and click the option
            try:
                # First attempt - option might be visible already
                option = self.page.get_by_text(option_text, exact=exact)
                option.wait_for(state="visible", timeout=2000)
                option.click()
                logger.success(f"✓ Selected '{option_text}' (visible immediately)")
                
            except:
                # Option not visible - need to scroll in dropdown
                if scroll_if_needed:
                    logger.info(f"Option not immediately visible, scrolling in dropdown...")
                    
                    # Find the dropdown list container
                    dropdown_list = self.page.locator(f'.{dropdown_list_class}')
                    dropdown_list.wait_for(state="visible", timeout=2000)
                    
                    # Scroll to the option within the dropdown list
                    option = dropdown_list.get_by_text(option_text, exact=exact)
                    option.scroll_into_view_if_needed()
                    
                    # Wait a bit after scroll
                    self.page.wait_for_timeout(300)
                    
                    # Click the option
                    option.click()
                    logger.success(f"✓ Selected '{option_text}' (after scrolling)")
                else:
                    raise Exception(f"Option '{option_text}' not found and scroll disabled")
            
        except Exception as e:
            logger.error(f"✗ Failed to select dropdown: {str(e)}")
            screenshot_name = f"error_dropdown_{option_text.replace(' ', '_')}.png"
            self.page.screenshot(path=screenshot_name, full_page=True)
            logger.error(f"Screenshot saved: {screenshot_name}")
            raise

    
    @allure.step("Select dropdown with JS scroll: {locator} -> {option_text}")
def select_dropdown_by_click_with_js_scroll(
    self, 
    locator: str, 
    option_text: str, 
    exact: bool = False
) -> None:
    """
    Dropdown selection with JavaScript scrolling fallback
    """
    try:
        logger.info(f"Selecting '{option_text}' from dropdown")
        
        # Click to open
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=self.timeout)
        element.click()
        
        logger.info(f"✓ Dropdown opened")
        self.page.wait_for_timeout(500)
        
        # Find option
        option = self.page.get_by_text(option_text, exact=exact)
        
        # Try regular click first
        try:
            option.wait_for(state="visible", timeout=2000)
            option.click()
            logger.success(f"✓ Selected '{option_text}'")
        except:
            # Use JavaScript to scroll into view
            logger.info(f"Using JavaScript scroll...")
            option.evaluate("element => element.scrollIntoView({block: 'center', behavior: 'smooth'})")
            self.page.wait_for_timeout(500)
            option.click()
            logger.success(f"✓ Selected '{option_text}' (JS scroll)")
            
    except Exception as e:
        logger.error(f"✗ Failed: {str(e)}")
        self.page.screenshot(path="error_dropdown_scroll.png")
        raise

    
    @allure.step("Close any open dropdowns")
    def close_open_dropdowns(self) -> None:
        """Close any open dropdown by clicking outside"""
        try:
            logger.info("Closing any open dropdowns...")
            # Click on a safe area (like body or a label) to close dropdowns
            self.page.locator('body').click(position={'x': 10, 'y': 10})
            self.page.wait_for_timeout(500)
            logger.success("✓ Dropdowns closed")
        except Exception as e:
            logger.warning(f"Could not close dropdowns: {str(e)}")