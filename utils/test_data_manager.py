import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from loguru import logger
import copy


class TestDataManager:
    """Manager for handling environment-specific test data from JSON files"""
    
    def __init__(self, data_dir: str = "testdata", env: str = "dev"):
        self.data_dir = Path(data_dir)
        self.env = env.lower()  # ✅ Store environment
        self.test_mapping_file = self.data_dir / "test_mapping.json"
        self.test_mapping = self._load_test_mapping()
        self._cached_data = {}
        logger.info(f"Initialized TestDataManager for environment: {self.env}")
    
    def _load_test_mapping(self) -> Dict[str, Any]:
        """Load test case to data file mapping"""
        if not self.test_mapping_file.exists():
            logger.warning(f"Test mapping file not found: {self.test_mapping_file}")
            logger.info("Creating empty test mapping file")
            self._create_empty_mapping()
            return {}
        
        try:
            with open(self.test_mapping_file, 'r', encoding='utf-8') as file:
                mapping = json.load(file)
                logger.info(f"Loaded test mapping from {self.test_mapping_file}")
                logger.debug(f"Available test mappings: {list(mapping.keys())}")
                return mapping
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in test mapping file: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading test mapping: {str(e)}")
            raise
    
    def _create_empty_mapping(self) -> None:
        """Create an empty test mapping file"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        empty_mapping = {
            "_comment": "Map test case IDs to data files and datasets",
            "_example": {
                "test_case_id": {
                    "data_file": "test_data.json",
                    "dataset": "dataset_name",
                    "description": "Description of the test case"
                }
            }
        }
        with open(self.test_mapping_file, 'w', encoding='utf-8') as file:
            json.dump(empty_mapping, file, indent=4, ensure_ascii=False)
    
    def _get_data_file_path(self, base_filename: str) -> Path:
        """
        Get the appropriate data file path based on environment
        Priority: env-specific file > base file
        
        Example:
        - If env='qa' and base_filename='registration_data.json'
        - First tries: testdata/qa/registration_data.json
        - Falls back to: testdata/registration_data.json
        """
        # Try environment-specific file first
        env_file = self.data_dir / self.env / base_filename
        if env_file.exists():
            logger.info(f"Using environment-specific data file: {env_file}")
            return env_file
        
        # Fall back to base file
        base_file = self.data_dir / base_filename
        if base_file.exists():
            logger.info(f"Using base data file: {base_file}")
            return base_file
        
        raise FileNotFoundError(
            f"Data file not found: {base_filename} "
            f"(checked: {env_file}, {base_file})"
        )
    
    def get_test_data(self, test_case_id: str, data_key: Optional[str] = None, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get test data for a specific test case (environment-aware)
        
        Args:
            test_case_id: Test case identifier (e.g., 'test_registration_valid_user')
            data_key: Optional key to get specific data set
            use_cache: Whether to use cached data if available
            
        Returns:
            Dictionary containing test data
            
        Raises:
            ValueError: If test case ID not found in mapping
            FileNotFoundError: If data file doesn't exist
        """
        cache_key = f"{test_case_id}:{data_key}" if data_key else test_case_id
        
        # Check cache first
        if use_cache and cache_key in self._cached_data:
            logger.debug(f"Returning cached data for '{cache_key}'")
            return copy.deepcopy(self._cached_data[cache_key])
        
        # Validate test case exists in mapping
        if test_case_id not in self.test_mapping:
            available_tests = [k for k in self.test_mapping.keys() if not k.startswith('_')]
            logger.error(f"Test case '{test_case_id}' not found in mapping")
            logger.info(f"Available test cases: {available_tests}")
            raise ValueError(
                f"Test case '{test_case_id}' not found in test_mapping.json. "
                f"Available: {available_tests}"
            )
        
        mapping = self.test_mapping[test_case_id]
        
        # ✅ Use environment-aware file path
        data_file = self._get_data_file_path(mapping['data_file'])
        dataset_name = mapping.get('dataset', data_key)
        
        # Load data from file
        try:
            with open(data_file, 'r', encoding='utf-8') as file:
                all_data = json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in data file {data_file}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading data file {data_file}: {str(e)}")
            raise
        
        # Extract specific dataset if specified
        if dataset_name:
            if dataset_name not in all_data:
                available_datasets = list(all_data.keys())
                logger.error(f"Dataset '{dataset_name}' not found in {data_file}")
                logger.info(f"Available datasets: {available_datasets}")
                raise ValueError(
                    f"Dataset '{dataset_name}' not found in {data_file}. "
                    f"Available: {available_datasets}"
                )
            test_data = all_data[dataset_name]
        else:
            test_data = all_data
        
        # Cache the data
        self._cached_data[cache_key] = copy.deepcopy(test_data)
        
        logger.success(f"Retrieved test data for '{test_case_id}' from {data_file} ({self.env} environment)")
        logger.debug(f"Data keys: {list(test_data.keys())}")
        
        return copy.deepcopy(test_data)
    
    def get_data_from_file(
        self, 
        file_name: str, 
        data_key: Optional[str] = None,
        use_cache: bool = False
    ) -> Dict[str, Any]:
        """
        Get data directly from a file without using test mapping (environment-aware)
        
        Args:
            file_name: Name of the data file (e.g., 'registration_data.json')
            data_key: Optional specific dataset name within the file
            use_cache: Whether to use cached data
            
        Returns:
            Dictionary containing test data
            
        Raises:
            FileNotFoundError: If data file doesn't exist
        """
        cache_key = f"{file_name}:{data_key}" if data_key else file_name
        
        if use_cache and cache_key in self._cached_data:
            logger.debug(f"Returning cached data for '{cache_key}'")
            return copy.deepcopy(self._cached_data[cache_key])
        
        # ✅ Use environment-aware file path
        data_file = self._get_data_file_path(file_name)
        
        try:
            with open(data_file, 'r', encoding='utf-8') as file:
                all_data = json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {data_file}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading file {data_file}: {str(e)}")
            raise
        
        if data_key:
            if data_key not in all_data:
                available_datasets = list(all_data.keys())
                logger.error(f"Dataset '{data_key}' not found in {data_file}")
                logger.info(f"Available datasets: {available_datasets}")
                raise ValueError(
                    f"Dataset '{data_key}' not found in {data_file}. "
                    f"Available: {available_datasets}"
                )
            result = all_data[data_key]
        else:
            result = all_data
        
        self._cached_data[cache_key] = copy.deepcopy(result)
        logger.success(f"Loaded data from {data_file} ({self.env} environment)" + 
                      (f", dataset: {data_key}" if data_key else ""))
        
        return copy.deepcopy(result)
    
    def get_all_datasets(self, file_name: str) -> List[str]:
        """
        Get list of all dataset names in a data file
        
        Args:
            file_name: Name of the data file
            
        Returns:
            List of dataset names
        """
        data_file = self._get_data_file_path(file_name)
        
        with open(data_file, 'r', encoding='utf-8') as file:
            all_data = json.load(file)
        
        datasets = list(all_data.keys())
        logger.info(f"Available datasets in {file_name}: {datasets}")
        return datasets
    
    def merge_data(self, *data_dicts: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge multiple data dictionaries (later values override earlier ones)
        
        Args:
            *data_dicts: Variable number of dictionaries to merge
        
        Returns:
            Merged dictionary
        """
        merged = {}
        for data_dict in data_dicts:
            merged.update(data_dict)
        
        logger.info(f"Merged {len(data_dicts)} data dictionaries")
        return merged
    
    def override_data(self, base_data: Dict[str, Any], **overrides) -> Dict[str, Any]:
        """
        Override specific fields in base data
        
        Args:
            base_data: Base data dictionary
            **overrides: Key-value pairs to override
        
        Returns:
            Data dictionary with overrides applied
        """
        updated_data = base_data.copy()
        updated_data.update(overrides)
        
        logger.info(f"Applied {len(overrides)} overrides to data")
        return updated_data
    
    def save_test_data(
        self, 
        file_name: str, 
        data: Dict[str, Any],
        overwrite: bool = False
    ) -> None:
        """
        Save test data to a file
        
        Args:
            file_name: Name of the file to save
            data: Data to save
            overwrite: Whether to overwrite existing file
        """
        data_file = self.data_dir / file_name
        
        if data_file.exists() and not overwrite:
            logger.warning(f"File {data_file} already exists. Use overwrite=True to replace")
            raise FileExistsError(f"File {data_file} already exists")
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        
        logger.success(f"Saved test data to {data_file}")
    
    def update_test_mapping(
        self, 
        test_case_id: str, 
        data_file: str,
        dataset: str,
        description: str = ""
    ) -> None:
        """
        Add or update a test case mapping
        
        Args:
            test_case_id: Test case identifier
            data_file: Name of the data file
            dataset: Dataset name within the file
            description: Description of the test case
        """
        self.test_mapping[test_case_id] = {
            "data_file": data_file,
            "dataset": dataset,
            "description": description
        }
        
        with open(self.test_mapping_file, 'w', encoding='utf-8') as file:
            json.dump(self.test_mapping, file, indent=4, ensure_ascii=False)
        
        logger.success(f"Updated test mapping for '{test_case_id}'")
    
    def list_all_test_cases(self) -> List[str]:
        """Get list of all mapped test cases"""
        test_cases = [k for k in self.test_mapping.keys() if not k.startswith('_')]
        logger.info(f"Available test cases: {test_cases}")
        return test_cases
    
    def clear_cache(self) -> None:
        """Clear the data cache"""
        self._cached_data.clear()
        logger.info("Data cache cleared")
    
    def validate_test_data(self, test_case_id: str) -> bool:
        """
        Validate that test data exists and is accessible
        
        Args:
            test_case_id: Test case identifier
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self.get_test_data(test_case_id, use_cache=False)
            logger.success(f"Test data for '{test_case_id}' is valid")
            return True
        except Exception as e:
            logger.error(f"Test data validation failed for '{test_case_id}': {str(e)}")
            return False