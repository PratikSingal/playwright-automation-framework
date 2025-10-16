# ==================== CELL-BASED METHODS WITH IFRAME_AWARE ====================

@iframe_aware
@allure.step("Fill field in cell: {cell_name} -> {value}")
def fill_by_cell(
    self, 
    cell_name: str, 
    field_type: str, 
    value: Any,
    iframe_locator: Optional[str] = None
) -> None:
    """
    Fill field using cell-based navigation (iframe aware)
    Pattern: get_by_role("cell", name="Cell Name").get_by_role("textbox")
    
    Args:
        cell_name: Name/text of the cell to find
        field_type: Role of element to find within cell (textbox, checkbox, button, etc.)
        value: Value to fill/set
        iframe_locator: Optional iframe locator (handled by decorator)
    """
    try:
        logger.info(f"Filling {field_type} in cell '{cell_name}' with value '{value}'")
        
        # Navigate to cell
        cell = self.page.get_by_role("cell", name=cell_name)
        
        # Find element within cell by role (no name needed)
        element = cell.get_by_role(field_type)
        
        # Fill based on field type
        if field_type in ['textbox', 'searchbox', 'spinbutton']:
            element.fill(str(value))
        elif field_type == 'checkbox':
            if bool(value):
                element.check()
            else:
                element.uncheck()
        elif field_type == 'button':
            element.click()
        elif field_type == 'combobox':
            element.select_option(str(value))
        else:
            element.fill(str(value))  # Default to fill
        
        logger.success(f"✓ Filled {field_type} in cell '{cell_name}'")
        
    except Exception as e:
        logger.error(f"✗ Failed to fill field in cell '{cell_name}': {str(e)}")
        raise


@iframe_aware
@allure.step("Verify field in cell: {cell_name} = {expected_value}")
def verify_by_cell(
    self,
    cell_name: str,
    field_type: str,
    expected_value: Any,
    iframe_locator: Optional[str] = None,
    timeout: int = 5000
) -> None:
    """
    Verify field value using cell-based navigation (iframe aware)
    Pattern: get_by_role("cell", name="Cell Name").get_by_role("textbox")
    
    Args:
        cell_name: Name/text of the cell to find
        field_type: Role of element to find within cell
        expected_value: Expected value to verify
        iframe_locator: Optional iframe locator (handled by decorator)
        timeout: Assertion timeout
    """
    try:
        logger.info(f"Verifying {field_type} in cell '{cell_name}' = '{expected_value}'")
        
        # Navigate to cell
        cell = self.page.get_by_role("cell", name=cell_name)
        
        # Find element within cell by role
        element = cell.get_by_role(field_type)
        
        # Verify based on field type
        if field_type in ['textbox', 'searchbox', 'spinbutton', 'combobox']:
            expect(element).to_have_value(str(expected_value), timeout=timeout)
        elif field_type == 'checkbox':
            if bool(expected_value):
                expect(element).to_be_checked(timeout=timeout)
            else:
                expect(element).not_to_be_checked(timeout=timeout)
        elif field_type == 'button':
            if bool(expected_value):
                expect(element).to_be_visible(timeout=timeout)
        else:
            expect(element).to_have_value(str(expected_value), timeout=timeout)
        
        logger.success(f"✓ Verified {field_type} in cell '{cell_name}'")
        
    except AssertionError as e:
        logger.error(f"✗ Verification failed for cell '{cell_name}': {str(e)}")
        self.page.screenshot(path=f"error_verify_cell_{cell_name.replace(' ', '_')}.png")
        raise



def _fill_by_locator(self, field_type: str, locator: str, value: Any, field_config: Dict) -> None:
    """Fill field using traditional CSS/XPath locator or handle special dropdown types"""
    
    # Check if this is a cell-based field
    if field_config.get('method') == 'cell':
        cell_name = field_config.get('cell_name')
        iframe_loc = field_config.get('iframe_locator')
        
        if not cell_name:
            raise ValueError("Cell method requires 'cell_name' in field config")
        
        # Use the iframe-aware cell method
        self.actions.fill_by_cell(
            cell_name=cell_name,
            field_type=field_type,
            value=value,
            iframe_locator=iframe_loc
        )
        return  # Exit early
    
    # ... rest of your existing _fill_by_locator code for dropdowns, textboxes, etc.


def verify_form_data(
    self, 
    field_mapping: Dict[str, Any], 
    expected_data: Dict[str, Any],
    iframe_locator: Optional[str] = None,
    timeout: int = 5000
) -> None:
    """
    Generic method to verify form data based on field type and method
    """
    logger.info("Starting to verify form data")
    
    for field_name, expected_value in expected_data.items():
        if field_name not in field_mapping:
            logger.warning(f"Field '{field_name}' not found in mapping, skipping verification")
            continue
        
        field_config = field_mapping[field_name]
        field_type = field_config['type'].lower()
        method = field_config.get('method', 'locator')
        
        # Use iframe_locator from field config if present, otherwise use the parameter
        field_iframe = field_config.get('iframe_locator', iframe_locator)
        
        try:
            with allure.step(f"Verifying field: {field_name}"):
                
                # HANDLE CELL-BASED VERIFICATION
                if method == 'cell':
                    cell_name = field_config.get('cell_name')
                    if not cell_name:
                        raise ValueError(f"Field '{field_name}' uses 'cell' method but missing 'cell_name'")
                    
                    # Use iframe-aware cell verification
                    self.actions.verify_by_cell(
                        cell_name=cell_name,
                        field_type=field_type,
                        expected_value=expected_value,
                        iframe_locator=field_iframe,
                        timeout=timeout
                    )
                
                # HANDLE STANDARD VERIFICATION (existing code)
                elif method == 'get_by_label':
                    locator = field_config['locator']
                    exact = field_config.get('exact', False)
                    if '{' in locator and isinstance(expected_value, str):
                        locator = locator.format(value=expected_value)
                    
                    element = self._get_element_by_method(method, field_type, locator, exact, field_iframe)
                    self._verify_field_value(element, field_type, expected_value, timeout)
                
                # ... other methods (get_by_placeholder, get_by_role, etc.)
                
                else:
                    locator = field_config.get('locator')
                    exact = field_config.get('exact', False)
                    if locator and '{' in locator and isinstance(expected_value, str):
                        locator = locator.format(value=expected_value)
                    
                    element = self._get_element_by_method(method, field_type, locator, exact, field_iframe)
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


class NewAccountPage(BasePage):
    """Page Object for New Account form in iframe"""
    
    # Locator constants
    IFRAME_LOCATOR = "#iframeView"
    
    FIELD_MAPPING = {
        # Cell-based fields from your snippet
        'account_name': {
            'cell_name': 'Account Name',
            'type': 'textbox',
            'method': 'cell',
            'iframe_locator': '#iframeView'
        },
        
        'add_branch': {
            'cell_name': 'AddBranch',
            'type': 'textbox',
            'method': 'cell',
            'iframe_locator': '#iframeView'
        },
        
        'net': {
            'cell_name': 'Net',
            'type': 'textbox',
            'method': 'cell',
            'iframe_locator': '#iframeView'
        },
        
        'principal_currency': {
            'cell_name': 'Principal Currency',
            'type': 'textbox',
            'method': 'cell',
            'iframe_locator': '#iframeView'
        },
        
        'issb_main': {
            'cell_name': 'ISSB_Main',
            'type': 'textbox',
            'method': 'cell',
            'iframe_locator': '#iframeView'
        },
        
        'ifb': {
            'cell_name': 'IFB',
            'type': 'textbox',
            'method': 'cell',
            'iframe_locator': '#iframeView'
        },
        
        'other': {
            'cell_name': 'Other',
            'type': 'textbox',
            'method': 'cell',
            'iframe_locator': '#iframeView'
        }
    }
    
    def __init__(self, page: Page):
        super().__init__(page)
        logger.info("Initialized New Account Page")
    
    @allure.step("Open new account page")
    def open(self, url: str) -> None:
        """Navigate to new account page"""
        self.navigate_to(url)
        # Wait for iframe to load
        self.page.wait_for_selector(self.IFRAME_LOCATOR, state="visible")
        self.page.frame_locator(self.IFRAME_LOCATOR).locator("body").wait_for(state="visible")
        logger.success("New account page loaded")
    
    @allure.step("Fill new account form")
    def fill_new_account_form(self, data: Dict[str, Any]) -> None:
        """Fill the new account form"""
        logger.info("Filling new account form")
        self.fill_form_data(self.FIELD_MAPPING, data)
        logger.success("New account form filled")
    
    @allure.step("Verify new account form")
    def verify_new_account_form(self, expected_data: Dict[str, Any]) -> None:
        """Verify the new account form data"""
        logger.info("Verifying new account form")
        self.verify_form_data(
            self.FIELD_MAPPING, 
            expected_data,
            iframe_locator=self.IFRAME_LOCATOR
        )
        logger.success("New account form verified")
