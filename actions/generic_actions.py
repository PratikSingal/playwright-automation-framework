import allure
from playwright.sync_api import Page, Locator, expect
from typing import List, Optional, Union
from loguru import logger


class GenericActions:
    """Generic actions class for common web element interactions"""
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 30000
    
    @allure.step("Fill textbox: {locator} with value: {value}")
    def fill_textbox(self, locator: str, value: str, clear_first: bool = True) -> None:
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
    def fill_textarea(self, locator: str, value: str, clear_first: bool = True) -> None:
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
    def select_checkbox(self, locator: str, check: bool = True) -> None:
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
    
    @allure.step("Select dropdown option: {locator} with value: {value}")
    def select_dropdown(self, locator: str, value: str = None, label: str = None, index: int = None) -> None:
        """Select an option from a dropdown by value, label, or index"""
        try:
            logger.info(f"Selecting dropdown option from '{locator}'")
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=self.timeout)
            
            if value:
                element.select_option(value=value)
            elif label:
                element.select_option(label=label)
            elif index is not None:
                element.select_option(index=index)
            else:
                raise ValueError("Must provide value, label, or index")
            
            logger.success(f"Successfully selected dropdown option from '{locator}'")
        except Exception as e:
            logger.error(f"Failed to select dropdown option from '{locator}': {str(e)}")
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
    def wait_for_element(self, locator: str, state: str = "visible") -> None:
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
    def press_key(self, key: str, locator: str = None) -> None:
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