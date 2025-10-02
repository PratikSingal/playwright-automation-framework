import os
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Configuration manager for handling environment-specific configurations"""
    
    def __init__(self, env: str = None):
        self.env = env or os.getenv('TEST_ENV', 'dev')
        self.config_dir = Path(__file__).parent
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        config_file = self.config_dir / f"{self.env}.yaml"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    @property
    def base_url(self) -> str:
        """Get base URL"""
        return self.get('application.base_url')
    
    @property
    def headless(self) -> bool:
        """Get headless mode"""
        return self.get('browser.headless', False)
    
    @property
    def browser_type(self) -> str:
        """Get browser type"""
        return self.get('browser.type', 'chromium')
    
    @property
    def timeout(self) -> int:
        """Get default timeout"""
        return self.get('browser.timeout', 30000)
    
    @property
    def db_config(self) -> Dict[str, str]:
        """Get database configuration"""
        return self.get('database', {})
    
    @property
    def api_config(self) -> Dict[str, Any]:
        """Get API configuration"""
        return self.get('api', {})


# Singleton instance
config = ConfigManager()