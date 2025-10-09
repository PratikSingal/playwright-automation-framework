import pytest
import allure
from typing import Dict, Any, List, Callable
from loguru import logger


# ==========================================
# CORE TEST DATA FIXTURES (Environment-Aware)
# ==========================================

@pytest.fixture(scope="function")
def get_test_data(test_data_manager):
    """
    Factory fixture to get test data by test case ID (Environment-aware)
    
    Usage in test:
        data = get_test_data('test_registration_valid_user')
        data = get_test_data('test_registration_valid_user', 'valid_user_1')
    
    This will look up the test case in test_mapping.json and return the data
    from the appropriate environment folder (qa/uat/dev)
    """
    def _get_data(test_case_id: str, data_key: str = None, use_cache: bool = True) -> Dict[str, Any]:
        logger.info(f"Retrieving test data for: {test_case_id}")
        
        try:
            # Get data from TestDataManager (environment-aware)
            if data_key:
                data = test_data_manager.get_test_data(test_case_id, data_key)
            else:
                data = test_data_manager.get_test_data(test_case_id)
            
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
def get_data_from_file(test_data_manager):
    """
    Factory fixture to get test data directly from file (Environment-aware)
    
    Usage in test:
        # Get entire file
        data = get_data_from_file('registration_data.json')
        
        # Get specific dataset
        data = get_data_from_file('registration_data.json', 'valid_user_1')
    
    Automatically checks environment-specific folder first (testdata/qa/, testdata/uat/)
    """
    def _get_data(file_name: str, data_key: str = None, use_cache: bool = False) -> Dict[str, Any]:
        logger.info(f"Retrieving data from file: {file_name}, dataset: {data_key}")
        
        try:
            # Get data from TestDataManager (environment-aware)
            data = test_data_manager.get_data_from_file(file_name, data_key)
            
            # Attach data to Allure report
            import json
            allure.attach(
                json.dumps(data, indent=2, ensure_ascii=False),
                name=f"Test Data - {file_name}" + (f" - {data_key}" if data_key else ""),
                attachment_type=allure.attachment_type.JSON
            )
            
            logger.success(f"Data retrieved from: {file_name}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to retrieve data from '{file_name}': {str(e)}")
            raise
    
    return _get_data


@pytest.fixture(scope="function")
def test_data_with_overrides(test_data_manager):
    """
    Get test data and allow overriding specific fields (Environment-aware)
    
    Usage in test:
        data = test_data_with_overrides(
            'test_registration_valid_user',
            email='custom@email.com',
            phone='+919999999999'
        )
        
        # With data_key
        data = test_data_with_overrides(
            'test_registration_valid_user',
            data_key='valid_user_1',
            email='custom@email.com'
        )
    """
    def _get_data_with_overrides(test_case_id: str, data_key: str = None, **overrides) -> Dict[str, Any]:
        logger.info(f"Getting test data for '{test_case_id}' with overrides")
        
        # Get base data (environment-aware)
        base_data = test_data_manager.get_test_data(test_case_id, data_key)
        
        # Apply overrides using TestDataManager method
        data = test_data_manager.override_data(base_data, **overrides)
        
        # Attach overridden data to Allure
        if overrides:
            logger.debug(f"Applying overrides: {overrides}")
            import json
            allure.attach(
                json.dumps(overrides, indent=2),
                name=f"Data Overrides - {test_case_id}",
                attachment_type=allure.attachment_type.JSON
            )
        
        return data
    
    return _get_data_with_overrides


@pytest.fixture(scope="function")
def merge_test_data(test_data_manager, get_test_data):
    """
    Merge data from multiple test cases (Environment-aware)
    
    Usage in test:
        data = merge_test_data(
            'test_case_1',
            'test_case_2',
            custom_field='value'
        )
    """
    def _merge_data(*test_case_ids, **additional_data) -> Dict[str, Any]:
        logger.info(f"Merging test data from: {test_case_ids}")
        
        data_dicts = []
        
        for test_case_id in test_case_ids:
            data = get_test_data(test_case_id)
            data_dicts.append(data)
        
        # Use TestDataManager's merge method
        merged_data = test_data_manager.merge_data(*data_dicts)
        
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


# ==========================================
# DATA GENERATION FIXTURES
# ==========================================

@pytest.fixture
def faker_instance():
    """Fixture to provide Faker instance for generating random data"""
    from faker import Faker
    return Faker('en_IN')  # Indian locale


@pytest.fixture
def generate_random_user_data(faker_instance) -> Callable:
    """
    Fixture to generate random user registration data
    
    Usage:
        data = generate_random_user_data()
        data = generate_random_user_data(gender='male', country='IN')
    """
    def _generate_data(**kwargs) -> Dict[str, Any]:
        fake = faker_instance
        
        default_data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password': 'Test@123',
            'confirm_password': 'Test@123',
            'phone': fake.phone_number(),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
            'gender': kwargs.get('gender', fake.random_element(['male', 'female'])),
            'country': kwargs.get('country', 'IN'),
            'terms_conditions': True,
            'newsletter': fake.boolean()
        }
        
        # Override with any provided kwargs
        default_data.update(kwargs)
        logger.info(f"Generated random user data with email: {default_data['email']}")
        
        # Attach to Allure
        import json
        allure.attach(
            json.dumps(default_data, indent=2),
            name="Generated User Data",
            attachment_type=allure.attachment_type.JSON
        )
        
        return default_data
    
    return _generate_data


@pytest.fixture
def unique_id() -> str:
    """
    Generate unique identifier for test data
    
    Usage:
        email = f"testuser_{unique_id}@example.com"
    """
    import uuid
    unique = str(uuid.uuid4())[:8]
    logger.debug(f"Generated unique ID: {unique}")
    return unique


# ==========================================
# UTILITY FIXTURES
# ==========================================

@pytest.fixture(scope="function")
def get_all_datasets(test_data_manager):
    """
    Factory fixture to get list of all datasets in a file
    
    Usage in test:
        datasets = get_all_datasets('registration_data.json')
    """
    def _get_datasets(file_name: str) -> List[str]:
        logger.info(f"Getting all datasets from: {file_name}")
        # This would need to be implemented in TestDataManager
        # For now, return empty list
        return []
    
    return _get_datasets


@pytest.fixture(scope="function")
def validate_test_data(test_data_manager):
    """
    Factory fixture to validate test data exists
    
    Usage in test:
        is_valid = validate_test_data('test_registration_valid_user')
    """
    def _validate(test_case_id: str) -> bool:
        logger.info(f"Validating test data for: {test_case_id}")
        try:
            test_data_manager.get_test_data(test_case_id)
            return True
        except Exception:
            return False
    
    return _validate


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