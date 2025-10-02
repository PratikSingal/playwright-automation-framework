import requests
import allure
from typing import Dict, Any, Optional
from config.config_manager import config
from loguru import logger
import json


class APIClient:
    """API client for making HTTP requests"""
    
    def __init__(self):
        self.base_url = config.api_config.get('base_url', '')
        self.timeout = config.api_config.get('timeout', 30)
        self.verify_ssl = config.api_config.get('verify_ssl', True)
        self.default_headers = config.api_config.get('headers', {})
        self.session = requests.Session()
        self.session.headers.update(self.default_headers)
    
    @allure.step("GET request to: {endpoint}")
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send GET request
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to: {url}")
        
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            self._log_response(response)
            return response
            
        except Exception as e:
            logger.error(f"GET request failed: {str(e)}")
            raise
    
    @allure.step("POST request to: {endpoint}")
    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send POST request
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON payload
            headers: Additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to: {url}")
        
        try:
            response = self.session.post(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            self._log_response(response)
            return response
            
        except Exception as e:
            logger.error(f"POST request failed: {str(e)}")
            raise
    
    @allure.step("PUT request to: {endpoint}")
    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send PUT request
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON payload
            headers: Additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT request to: {url}")
        
        try:
            response = self.session.put(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            self._log_response(response)
            return response
            
        except Exception as e:
            logger.error(f"PUT request failed: {str(e)}")
            raise
    
    @allure.step("DELETE request to: {endpoint}")
    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send DELETE request
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE request to: {url}")
        
        try:
            response = self.session.delete(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            self._log_response(response)
            return response
            
        except Exception as e:
            logger.error(f"DELETE request failed: {str(e)}")
            raise
    
    @allure.step("PATCH request to: {endpoint}")
    def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send PATCH request
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON payload
            headers: Additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH request to: {url}")
        
        try:
            response = self.session.patch(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            self._log_response(response)
            return response
            
        except Exception as e:
            logger.error(f"PATCH request failed: {str(e)}")
            raise
    
    def _log_response(self, response: requests.Response) -> None:
        """Log response details"""
        logger.info(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")
        
        try:
            response_json = response.json()
            logger.debug(f"Response Body: {json.dumps(response_json, indent=2)}")
            
            # Attach to Allure report
            allure.attach(
                json.dumps(response_json, indent=2),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
        except:
            logger.debug(f"Response Body: {response.text}")
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.TEXT
            )
    
    def set_auth_token(self, token: str, token_type: str = "Bearer") -> None:
        """Set authentication token"""
        self.session.headers.update({
            "Authorization": f"{token_type} {token}"
        })
        logger.info("Authentication token set")
    
    def clear_auth_token(self) -> None:
        """Clear authentication token"""
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
        logger.info("Authentication token cleared")