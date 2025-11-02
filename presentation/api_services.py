"""
API Service Layer for Tides & Tomes Dashboard
Handles all external API calls with error handling, retries, and caching
Production-ready implementation with best practices
"""

import requests
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import time
from functools import lru_cache
import hashlib
import json

from .config import config

logger = logging.getLogger(__name__)


class APIException(Exception):
    """Custom exception for API errors"""
    pass


class APIService:
    """Base class for API services with common functionality"""
    
    def __init__(self, name: str):
        self.name = name
        self.session = requests.Session()
        self._cache = {}
        self._cache_timestamps = {}
    
    def _get_cache_key(self, **kwargs) -> str:
        """Generate cache key from parameters"""
        key_string = json.dumps(kwargs, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cached(self, cache_key: str, ttl: int) -> Optional[Any]:
        """Get data from cache if not expired"""
        if cache_key in self._cache:
            timestamp = self._cache_timestamps.get(cache_key, 0)
            if time.time() - timestamp < ttl:
                logger.debug(f"{self.name}: Cache hit for {cache_key}")
                return self._cache[cache_key]
            else:
                logger.debug(f"{self.name}: Cache expired for {cache_key}")
                del self._cache[cache_key]
                del self._cache_timestamps[cache_key]
        return None
    
    def _set_cached(self, cache_key: str, data: Any):
        """Store data in cache"""
        self._cache[cache_key] = data
        self._cache_timestamps[cache_key] = time.time()
        logger.debug(f"{self.name}: Cached data for {cache_key}")
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with retries and timeout"""
        kwargs.setdefault('timeout', config.API_TIMEOUT)
        
        for attempt in range(config.API_RETRY_ATTEMPTS):
            try:
                logger.info(f"{self.name}: {method} {url} (attempt {attempt + 1}/{config.API_RETRY_ATTEMPTS})")
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            
            except requests.exceptions.Timeout:
                logger.warning(f"{self.name}: Request timeout (attempt {attempt + 1})")
                if attempt < config.API_RETRY_ATTEMPTS - 1:
                    time.sleep(config.API_RETRY_DELAY * (attempt + 1))
                else:
                    raise APIException(f"{self.name} API timeout after {config.API_RETRY_ATTEMPTS} attempts")
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code >= 500:
                    # Server error - retry
                    logger.warning(f"{self.name}: Server error {e.response.status_code} (attempt {attempt + 1})")
                    if attempt < config.API_RETRY_ATTEMPTS - 1:
                        time.sleep(config.API_RETRY_DELAY * (attempt + 1))
                    else:
                        raise APIException(f"{self.name} API server error: {e}")
                else:
                    # Client error - don't retry
                    logger.error(f"{self.name}: Client error {e.response.status_code}: {e}")
                    raise APIException(f"{self.name} API error: {e}")
            
            except requests.exceptions.RequestException as e:
                logger.error(f"{self.name}: Request failed: {e}")
                if attempt < config.API_RETRY_ATTEMPTS - 1:
                    time.sleep(config.API_RETRY_DELAY * (attempt + 1))
                else:
                    raise APIException(f"{self.name} API request failed: {e}")


class WeatherbitService(APIService):
    """Service for Weatherbit weather API"""
    
    def __init__(self):
        super().__init__("Weatherbit")
        self.base_url = config.WEATHERBIT_BASE_URL
        self.api_key = config.WEATHERBIT_API_KEY
    
    def get_current_weather(self, city: str, country: str = 'GB') -> Dict[str, Any]:
        """Get current weather for a city"""
        cache_key = self._get_cache_key(city=city, country=country)
        cached = self._get_cached(cache_key, config.CACHE_TTL_WEATHER)
        if cached:
            return cached
        
        if not self.api_key:
            raise APIException("Weatherbit API key not configured")
        
        url = f"{self.base_url}/current"
        params = {
            'city': city,
            'country': country,
            'key': self.api_key
        }
        
        response = self._make_request('GET', url, params=params)
        data = response.json()
        
        if 'data' not in data or len(data['data']) == 0:
            raise APIException(f"No weather data returned for {city}")
        
        weather = data['data'][0]
        result = {
            'city': weather.get('city_name'),
            'temperature': weather.get('temp'),
            'feels_like': weather.get('app_temp'),
            'description': weather.get('weather', {}).get('description'),
            'wind_speed': weather.get('wind_spd'),
            'humidity': weather.get('rh'),
            'pressure': weather.get('pres'),
            'timestamp': weather.get('ob_time'),
            'clouds': weather.get('clouds'),
            'uv_index': weather.get('uv'),
            'visibility': weather.get('vis')
        }
        
        self._set_cached(cache_key, result)
        return result
    
    def get_scottish_regional_summary(self) -> Dict[str, Any]:
        """Get weather summary for all Scottish regions"""
        results = []
        total_temp = 0
        total_humidity = 0
        
        for location in config.SCOTTISH_LOCATIONS:
            try:
                weather = self.get_current_weather(location['name'])
                results.append({
                    'location': location['name'],
                    'weather': weather
                })
                total_temp += weather['temperature']
                total_humidity += weather['humidity']
            except Exception as e:
                logger.error(f"Failed to get weather for {location['name']}: {e}")
        
        if not results:
            raise APIException("Failed to retrieve weather for any Scottish location")
        
        return {
            'regions': results,
            'count': len(results),
            'avg_temperature': total_temp / len(results),
            'avg_humidity': total_humidity / len(results),
            'timestamp': datetime.now().isoformat()
        }


class NOAAService(APIService):
    """Service for NOAA Climate Data API"""
    
    def __init__(self):
        super().__init__("NOAA")
        self.base_url = config.NOAA_BASE_URL
        self.api_key = config.NOAA_API_KEY
    
    def get_datasets(self) -> List[Dict[str, Any]]:
        """Get available NOAA datasets"""
        cache_key = self._get_cache_key(endpoint='datasets')
        cached = self._get_cached(cache_key, config.CACHE_TTL_CLIMATE)
        if cached:
            return cached
        
        if not self.api_key:
            raise APIException("NOAA API key not configured")
        
        url = f"{self.base_url}/datasets"
        headers = config.get_api_headers('noaa')
        
        response = self._make_request('GET', url, headers=headers)
        data = response.json()
        
        datasets = data.get('results', [])
        self._set_cached(cache_key, datasets)
        return datasets
    
    def get_climate_data(self, dataset_id: str = 'GHCND', 
                        location_id: str = 'CITY:UK000001',
                        days: int = 30) -> Dict[str, Any]:
        """Get climate data for a location"""
        cache_key = self._get_cache_key(
            dataset=dataset_id, 
            location=location_id, 
            days=days
        )
        cached = self._get_cached(cache_key, config.CACHE_TTL_CLIMATE)
        if cached:
            return cached
        
        if not self.api_key:
            raise APIException("NOAA API key not configured")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = f"{self.base_url}/data"
        headers = config.get_api_headers('noaa')
        params = {
            'datasetid': dataset_id,
            'locationid': location_id,
            'startdate': start_date.strftime('%Y-%m-%d'),
            'enddate': end_date.strftime('%Y-%m-%d'),
            'limit': 1000
        }
        
        response = self._make_request('GET', url, headers=headers, params=params)
        data = response.json()
        
        result = {
            'dataset': dataset_id,
            'location': location_id,
            'records': data.get('results', []),
            'count': len(data.get('results', [])),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        
        self._set_cached(cache_key, result)
        return result


class GlobalFishingWatchService(APIService):
    """Service for Global Fishing Watch API"""
    
    def __init__(self):
        super().__init__("GlobalFishingWatch")
        self.base_url = config.GFW_API_BASE_URL
        self.api_token = config.GFW_API_TOKEN
    
    def get_fishing_events(self, start_date: str, end_date: str, 
                          limit: int = 100) -> Dict[str, Any]:
        """Get fishing events within date range"""
        cache_key = self._get_cache_key(
            start=start_date, 
            end=end_date, 
            limit=limit
        )
        cached = self._get_cached(cache_key, config.CACHE_TTL_MARINE)
        if cached:
            return cached
        
        if not self.api_token:
            raise APIException("Global Fishing Watch API token not configured")
        
        url = f"{self.base_url}/v3/events"
        headers = config.get_api_headers('gfw')
        params = {
            'datasets[0]': 'public-global-fishing-events:latest',
            'start-date': start_date,
            'end-date': end_date,
            'limit': limit,
            'offset': 0
        }
        
        response = self._make_request('GET', url, headers=headers, params=params)
        data = response.json()
        
        result = {
            'events': data.get('entries', []),
            'count': len(data.get('entries', [])),
            'start_date': start_date,
            'end_date': end_date,
            'timestamp': datetime.now().isoformat()
        }
        
        self._set_cached(cache_key, result)
        return result
    
    def get_fishing_activity_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get summary of fishing activity for recent period"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        events_data = self.get_fishing_events(
            start_date=start_date.strftime('%Y-%m-%dT00:00:00.000Z'),
            end_date=end_date.strftime('%Y-%m-%dT23:59:59.999Z'),
            limit=500
        )
        
        events = events_data['events']
        
        # Analyze events
        vessel_ids = set()
        event_types = {}
        locations = []
        
        for event in events:
            vessel_ids.add(event.get('vessel', {}).get('id'))
            event_type = event.get('type', 'unknown')
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            if 'position' in event:
                pos = event['position']
                locations.append({
                    'lat': pos.get('lat'),
                    'lon': pos.get('lon')
                })
        
        return {
            'total_events': len(events),
            'unique_vessels': len(vessel_ids),
            'event_types': event_types,
            'locations': locations,
            'period_days': days,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }


# Create service instances
try:
    weatherbit_service = WeatherbitService()
    noaa_service = NOAAService()
    gfw_service = GlobalFishingWatchService()
    
    logger.info("All API services initialized successfully")
except Exception as e:
    logger.error(f"Error initializing API services: {e}")
    weatherbit_service = None
    noaa_service = None
    gfw_service = None
