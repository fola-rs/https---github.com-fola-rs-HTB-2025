"""
Global Fishing Watch API Integration
====================================

Real API integration for marine vessel tracking and environmental data.
This data can serve as a proxy for coastal ecosystem health and marine activity.
"""

import os
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GlobalFishingWatchAPI:
    """
    Integration with Global Fishing Watch API for marine data
    
    Use cases for our project:
    - Vessel tracking as proxy for fishing pressure on marine ecosystems
    - Coastal activity patterns correlating with seaweed bed health
    - Marine traffic data as environmental impact indicator
    """
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize GFW API client
        
        Args:
            api_token: JWT token for GFW API. If not provided, reads from env.
        """
        self.api_token = api_token or os.getenv('GFW_API_TOKEN')
        self.base_url = os.getenv('GFW_API_BASE_URL', 'https://gateway.api.globalfishingwatch.org')
        
        if not self.api_token:
            logger.warning("No GFW API token found. Set GFW_API_TOKEN environment variable.")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    def get_vessels_in_region(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get vessel activity in a region (e.g., North Sea near turtle sites)
        
        Args:
            lat_min, lat_max: Latitude bounds
            lon_min, lon_max: Longitude bounds
            start_date: ISO format date (default: 30 days ago)
            end_date: ISO format date (default: today)
        
        Returns:
            Vessel tracking data
        """
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # GFW API v2 endpoint for vessel tracking
        endpoint = f"{self.base_url}/v2/events"
        
        params = {
            'datasets': 'public-global-fishing-effort:latest',
            'start-date': start_date,
            'end-date': end_date,
            'lat-min': lat_min,
            'lat-max': lat_max,
            'lon-min': lon_min,
            'lon-max': lon_max
        }
        
        try:
            logger.info(f"🌊 Fetching GFW vessel data for region ({lat_min},{lon_min}) to ({lat_max},{lon_max})")
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✅ Retrieved GFW data: {len(data.get('entries', []))} vessel events")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ GFW API request failed: {e}")
            return {'error': str(e), 'entries': []}
    
    def get_fishing_effort_summary(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get aggregated fishing effort summary for a region
        
        This is useful as an indicator of:
        - Marine ecosystem pressure
        - Coastal activity levels
        - Potential correlation with seaweed bed health
        
        Args:
            lat_min, lat_max, lon_min, lon_max: Region bounds
            days: Number of days to aggregate
        
        Returns:
            Summary statistics
        """
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        vessel_data = self.get_vessels_in_region(
            lat_min, lat_max, lon_min, lon_max,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        
        # Calculate summary statistics
        entries = vessel_data.get('entries', [])
        
        summary = {
            'region': {
                'lat_range': [lat_min, lat_max],
                'lon_range': [lon_min, lon_max]
            },
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'days': days
            },
            'vessel_events': len(entries),
            'fishing_hours': sum(e.get('fishing_hours', 0) for e in entries),
            'unique_vessels': len(set(e.get('vessel_id', '') for e in entries if e.get('vessel_id'))),
            'avg_daily_activity': len(entries) / days if days > 0 else 0,
            'ecosystem_pressure_index': self._calculate_pressure_index(entries),
            'correlation_note': 'Higher fishing effort may correlate with degraded seaweed habitats'
        }
        
        return summary
    
    def _calculate_pressure_index(self, entries: List[Dict]) -> float:
        """
        Calculate a simple ecosystem pressure index (0-100)
        Based on fishing intensity
        
        Args:
            entries: Vessel event data
        
        Returns:
            Pressure index (0=low, 100=extreme)
        """
        
        if not entries:
            return 0.0
        
        # Simple heuristic: more vessels + more fishing hours = higher pressure
        vessel_count = len(entries)
        total_fishing_hours = sum(e.get('fishing_hours', 0) for e in entries)
        
        # Normalize to 0-100 scale (adjust thresholds based on real data)
        pressure = min(100, (vessel_count * 2 + total_fishing_hours * 0.5))
        
        return round(pressure, 2)
    
    def get_north_sea_marine_activity(self) -> Dict[str, Any]:
        """
        Get marine activity for North Sea region (relevant to our project)
        
        North Sea coordinates approximate bounds
        """
        
        return self.get_fishing_effort_summary(
            lat_min=54.0,
            lat_max=58.0,
            lon_min=-4.0,
            lon_max=2.0,
            days=30
        )
    
    def get_scottish_coast_activity(self) -> Dict[str, Any]:
        """
        Get marine activity for Scottish coast (Aberdeenshire seaweed region)
        """
        
        return self.get_fishing_effort_summary(
            lat_min=56.5,
            lat_max=58.5,
            lon_min=-3.5,
            lon_max=-1.0,
            days=30
        )


# Example usage for integrating with our project
def integrate_gfw_with_seaweed_model():
    """
    Example: Use GFW fishing pressure as additional feature for seaweed health prediction
    """
    
    gfw = GlobalFishingWatchAPI()
    
    # Get fishing pressure for Scottish coast
    activity = gfw.get_scottish_coast_activity()
    
    # This ecosystem pressure index can be used as a model feature
    pressure_index = activity.get('ecosystem_pressure_index', 0)
    
    logger.info(f"""
    🌊 GFW Integration Example:
    
    Ecosystem Pressure Index: {pressure_index}/100
    
    Model Integration:
    - Use as additional feature in seaweed health prediction
    - Higher pressure → potentially degraded seaweed beds
    - Combine with turtle population data for holistic ecosystem view
    
    Correlation Hypothesis:
    High fishing effort → Disturbed marine ecosystem → Reduced seaweed health
    → Affects our seaweed → whisky → Edinburgh economic chain
    """)
    
    return {
        'fishing_pressure_index': pressure_index,
        'vessel_events': activity.get('vessel_events', 0),
        'recommendation': 'Incorporate into seaweed biomass prediction model'
    }


if __name__ == "__main__":
    print("🌊 Testing Global Fishing Watch API Integration")
    print("=" * 70)
    
    # Initialize API
    gfw = GlobalFishingWatchAPI()
    
    # Test 1: North Sea activity
    print("\n📍 North Sea Marine Activity (Turtle Region)")
    north_sea = gfw.get_north_sea_marine_activity()
    print(f"  Vessel Events: {north_sea.get('vessel_events', 'N/A')}")
    print(f"  Fishing Hours: {north_sea.get('fishing_hours', 'N/A')}")
    print(f"  Ecosystem Pressure: {north_sea.get('ecosystem_pressure_index', 'N/A')}/100")
    
    # Test 2: Scottish coast
    print("\n📍 Scottish Coast Activity (Seaweed Region)")
    scotland = gfw.get_scottish_coast_activity()
    print(f"  Vessel Events: {scotland.get('vessel_events', 'N/A')}")
    print(f"  Unique Vessels: {scotland.get('unique_vessels', 'N/A')}")
    print(f"  Ecosystem Pressure: {scotland.get('ecosystem_pressure_index', 'N/A')}/100")
    
    # Test 3: Integration example
    print("\n🔗 Model Integration Example")
    integration = integrate_gfw_with_seaweed_model()
    print(f"  Fishing Pressure for Model: {integration['fishing_pressure_index']}")
    print(f"  Recommendation: {integration['recommendation']}")
    
    print("\n✅ GFW API integration complete!")
    print("💡 This real data enhances our G-Research real-time challenge!")
