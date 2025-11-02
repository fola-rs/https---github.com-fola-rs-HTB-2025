"""
Configuration Management for Tides & Tomes Dashboard
Handles environment variables, API keys, and application settings
"""

import os
from dotenv import load_dotenv
from typing import Optional
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    """Application configuration with environment-based settings"""
    
    # API Keys
    WEATHERBIT_API_KEY: Optional[str] = os.getenv('WEATHERBIT_API_KEY')
    NOAA_API_KEY: Optional[str] = os.getenv('NOAA_API_KEY')
    GFW_API_TOKEN: Optional[str] = os.getenv('GFW_API_TOKEN')
    GFW_API_BASE_URL: str = os.getenv('GFW_API_BASE_URL', 'https://gateway.api.globalfishingwatch.org')
    
    # API Endpoints
    WEATHERBIT_BASE_URL: str = 'https://api.weatherbit.io/v2.0'
    NOAA_BASE_URL: str = 'https://www.ncdc.noaa.gov/cdo-web/api/v2'
    
    # Cache settings (in seconds)
    CACHE_TTL_WEATHER: int = 1800  # 30 minutes
    CACHE_TTL_MARINE: int = 3600   # 1 hour
    CACHE_TTL_CLIMATE: int = 86400  # 24 hours
    
    # API timeout settings (in seconds)
    API_TIMEOUT: int = 15
    API_RETRY_ATTEMPTS: int = 3
    API_RETRY_DELAY: int = 2
    
    # Application settings
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'production')
    
    # Scottish locations for weather data
    SCOTTISH_LOCATIONS = [
        {'name': 'Edinburgh', 'lat': 55.9533, 'lon': -3.1883},
        {'name': 'Glasgow', 'lat': 55.8642, 'lon': -4.2518},
        {'name': 'Aberdeen', 'lat': 57.1497, 'lon': -2.0943},
        {'name': 'Inverness', 'lat': 57.4778, 'lon': -4.2247},
        {'name': 'Stirling', 'lat': 56.1165, 'lon': -3.9369}
    ]
    
    # Data quality thresholds
    MIN_CORRELATION_THRESHOLD: float = 0.6
    MAX_MISSING_DATA_PERCENT: float = 10.0
    
    @classmethod
    def validate_api_keys(cls) -> dict:
        """Validate that required API keys are present"""
        keys_status = {
            'weatherbit': bool(cls.WEATHERBIT_API_KEY),
            'noaa': bool(cls.NOAA_API_KEY),
            'gfw': bool(cls.GFW_API_TOKEN)
        }
        
        missing_keys = [name for name, present in keys_status.items() if not present]
        
        if missing_keys:
            logger.warning(f"Missing API keys: {', '.join(missing_keys)}")
        
        return {
            'status': keys_status,
            'all_present': all(keys_status.values()),
            'missing': missing_keys
        }
    
    @classmethod
    def get_api_headers(cls, api_name: str) -> dict:
        """Get appropriate headers for each API"""
        headers = {}
        
        if api_name == 'weatherbit':
            # Weatherbit uses query params, not headers
            pass
        elif api_name == 'noaa':
            if cls.NOAA_API_KEY:
                headers['token'] = cls.NOAA_API_KEY
        elif api_name == 'gfw':
            if cls.GFW_API_TOKEN:
                headers['Authorization'] = f'Bearer {cls.GFW_API_TOKEN}'
                headers['Content-Type'] = 'application/json'
        
        return headers

# Create singleton instance
config = Config()

# Validate on import
if __name__ != '__main__':
    validation = config.validate_api_keys()
    if not validation['all_present']:
        logger.warning(f"Running with incomplete API configuration. Missing: {validation['missing']}")
