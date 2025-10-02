import pytest
import allure
from utils.test_data_manager import TestDataManager
from utils.helpers import DataGenerator
from typing import Dict, Any, List
from loguru import logger


@pytest.fixture(scope="session")
def test_data_manager() -> TestDataManager:
    """
    Create TestDataManager instance for the session
    This instance is shared across all tests
    """
    logger.info("Creating Test Data Manager fixture")
    manager = TestDataManager()
    
    # Log available test cases
    test_cases = manager.list_all_test_cases()
    logger.info(f"Available test cases in mapping: {len(test_cases)}")
    
    yield manager
    
    # Clear cache at end of session
    manager.clear_cache()
    logger.info("Test Data Manager fixture cleaned up")


@pytest.fixture(scope="function")
def get_test_data(test_data_manager: TestDataManager):
    """
    Factory fixture to get test data by test case ID
    
    Usage in test:
        data = get_test_data('test_registration_valid_user')
    
    This will look up the test case in test_mapping.json and return the data
    """
    def _get_data(test_case_id: str, use_cache: bool = True) -> Dict[str, Any]:
        logger.info(f"Retrieving test data for: {test_case_id}")
        
        try:
            data = test_data_manager.get_test_data(test_case_id, use_cache=use_cache)
            
            # Attach data to Allure report
            import json
            allure.attach(
                json.dumps(data, indent=2, ensure_ascii=False),
                name=f"Test Data - {test_case_id}",
                attachment_type=allure.attachment_type.JSON
            )
            
            logger.success(f"Test data retrieved for: {test_case_id}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to retrieve test data for '{test_case_id}': {str(e)}")
            raise
    
    return _get_data


@pytest.fixture(scope="function")
def get_data_from_file(test_data_manager: TestDataManager):
    """
    Factory fixture to get test data directly from file
    
    Usage in test:
        # Get entire file
        data = get_data_from_file('registration_data.json')
        
        # Get specific dataset
        data = get_data_from_file('registration_data.json', 'valid_user_1')
    """
    def _get_data(file_name: str, dataset: str = None, use_cache: bool = False) -> Dict[str, Any]:
        logger.info(f"Retrieving data from file: {file_name}, dataset: {dataset}")
        
        try:
            data = test_data_manager.get_data_from_file(file_name, dataset, use_cache=use_cache)
            
            # Attach data to Allure report
            import json
            allure.attach(
                json.dumps(data, indent=2, ensure_ascii=False),
                name=f"Test Data - {file_name}" + (f" - {dataset}" if dataset else ""),
                attachment_type=allure.attachment_type.JSON
            )
            
            logger.success(f"Data retrieved from: {file_name}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to retrieve data from '{file_name}': {str(e)}")
            raise
    
    return _get_data


@pytest.fixture(scope="function")
def get_all_datasets(test_data_manager: TestDataManager):
    """
    Factory fixture to get list of all datasets in a file
    
    Usage in test:
        datasets = get_all_datasets('registration_data.json')
    """
    def _get_datasets(file_name: str) -> List[str]:
        logger.info(f"Getting all datasets from: {file_name}")
        return test_data_manager.get_all_datasets(file_name)
    
    return _get_datasets


@pytest.fixture(scope="session")
def data_generator() -> DataGenerator:
    """
    Create DataGenerator instance for generating random test data
    
    Usage in test:
        email = data_generator.generate_email()
        password = data_generator.generate_password()
    """
    logger.info("Creating Data Generator fixture")
    return DataGenerator()


@pytest.fixture(scope="function")
def generate_random_user_data(data_generator: DataGenerator):
    """
    Generate random user data for testing
    
    Usage in test:
        user_data = generate_random_user_data()
        user_data = generate_random_user_data(gender='male')
    """
    def _generate(gender: str = None) -> Dict[str, Any]:
        logger.info(f"Generating random user data (gender: {gender})")
        
        first_name, last_name = data_generator.generate_name(gender=gender)
        email = data_generator.generate_email()
        password = data_generator.generate_password()
        phone = data_generator.generate_phone_number()
        
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'confirm_password': password,
            'phone': phone,
            'gender': gender if gender else 'male'
        }
        
        logger.debug(f"Generated user data: {user_data}")
        
        # Attach to Allure
        import json
        allure.attach(
            json.dumps(user_data, indent=2),
            name="Generated User Data",
            attachment_type=allure.attachment_type.JSON
        )
        
        return user_data
    
    return _generate


@pytest.fixture(scope="function")
def save_test_data(test_data_manager: TestDataManager):
    """
    Factory fixture to save test data to file
    
    Usage in test:
        save_test_data('new_data.json', {'key': 'value'})
    """
    def _save_data(file_name: str, data: Dict[str, Any], overwrite: bool = False) -> None:
        logger.info(f"Saving test data to: {file_name}")
        test_data_manager.save_test_data(file_name, data, overwrite=overwrite)
        logger.success(f"Test data saved to: {file_name}")
    
    return _save_data


@pytest.fixture(scope="function")
def update_test_mapping(test_data_manager: TestDataManager):
    """
    Factory fixture to update test case mapping
    
    Usage in test:
        update_test_mapping(
            'test_new_case',
            'data_file.json',
            'dataset_name',
            'Description'
        )
    """
    def _update_mapping(
        test_case_id: str,
        data_file: str,
        dataset: str,
        description: str = ""
    ) -> None:
        logger.info(f"Updating test mapping for: {test_case_id}")
        test_data_manager.update_test_mapping(
            test_case_id,
            data_file,
            dataset,
            description
        )
        logger.success(f"Test mapping updated for: {test_case_id}")
    
    return _update_mapping


@pytest.fixture(scope="function")
def validate_test_data(test_data_manager: TestDataManager):
    """
    Factory fixture to validate test data exists
    
    Usage in test:
        is_valid = validate_test_data('test_registration_valid_user')
    """
    def _validate(test_case_id: str) -> bool:
        logger.info(f"Validating test data for: {test_case_id}")
        return test_data_manager.validate_test_data(test_case_id)
    
    return _validate


@pytest.fixture(scope="function")
def test_data_with_overrides(get_test_data):
    """
    Get test data and allow overriding specific fields
    
    Usage in test:
        data = test_data_with_overrides(
            'test_registration_valid_user',
            email='custom@email.com',
            phone='+919999999999'
        )
    """
    def _get_data_with_overrides(test_case_id: str, **overrides) -> Dict[str, Any]:
        logger.info(f"Getting test data for '{test_case_id}' with overrides")
        
        data = get_test_data(test_case_id)
        
        # Apply overrides
        if overrides:
            logger.debug(f"Applying overrides: {overrides}")
            data.update(overrides)
            
            # Attach overridden data to Allure
            import json
            allure.attach(
                json.dumps(overrides, indent=2),
                name=f"Data Overrides - {test_case_id}",
                attachment_type=allure.attachment_type.JSON
            )
        
        return data
    
    return _get_data_with_overrides


@pytest.fixture(scope="function")
def merge_test_data(get_test_data):
    """
    Merge data from multiple test cases
    
    Usage in test:
        data = merge_test_data(
            'test_case_1',
            'test_case_2',
            custom_field='value'
        )
    """
    def _merge_data(*test_case_ids, **additional_data) -> Dict[str, Any]:
        logger.info(f"Merging test data from: {test_case_ids}")
        
        merged_data = {}
        
        for test_case_id in test_case_ids:
            data = get_test_data(test_case_id)
            merged_data.update(data)
        
        # Add any additional data
        if additional_data:
            merged_data.update(additional_data)
        
        logger.success(f"Merged data from {len(test_case_ids)} test cases")
        
        # Attach merged data to Allure
        import json
        allure.attach(
            json.dumps(merged_data, indent=2),
            name="Merged Test Data",
            attachment_type=allure.attachment_type.JSON
        )
        
        return merged_data
    
    return _merge_data


@pytest.fixture(scope="function", autouse=False)
def log_test_data(request):
    """
    Automatically log test data used in the test
    Enable by marking test with @pytest.mark.log_data
    """
    test_name = request.node.name
    logger.info(f"Test '{test_name}' started")
    
    yield
    
    logger.info(f"Test '{test_name}' completed")


@pytest.fixture(scope="function")
def parametrized_test_data(get_data_from_file):
    """
    Get multiple datasets for parametrized tests
    
    Usage with pytest.mark.parametrize:
        @pytest.mark.parametrize("data", parametrized_test_data('file.json'))
        def test_something(data):
            # data will be each dataset from the file
    """
    def _get_parametrized_data(file_name: str, dataset_names: List[str] = None) -> List[Dict[str, Any]]:
        logger.info(f"Getting parametrized data from: {file_name}")
        
        if dataset_names:
            # Get specific datasets
            datasets = [get_data_from_file(file_name, name) for name in dataset_names]
        else:
            # Get all datasets
            all_data = get_data_from_file(file_name)
            if isinstance(all_data, dict):
                datasets = list(all_data.values())
            else:
                datasets = [all_data]
        
        logger.success(f"Retrieved {len(datasets)} datasets for parametrization")
        return datasets
    
    return _get_parametrized_data