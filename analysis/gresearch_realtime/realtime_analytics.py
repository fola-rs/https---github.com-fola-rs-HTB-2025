"""
G-Research Challenge: Real-Time Data Analytics
==============================================

Demonstrating real-time data ingestion, processing, and analytics.

Key Features:
- Live data streaming from turtle, seaweed, and whisky sensors
- Real-time anomaly detection
- Live dashboard updates
- Predictive alerts based on streaming data
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from collections import deque
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealTimeAnalytics:
    """
    Real-time analytics engine for streaming data
    
    PLACEHOLDER: Will integrate with actual data streams when format is ready
    """
    
    def __init__(self, window_size: int = 100):
        """
        Initialize real-time analytics
        
        Args:
            window_size: Number of recent data points to keep in memory
        """
        self.window_size = window_size
        
        # Sliding windows for each data stream
        self.turtle_window = deque(maxlen=window_size)
        self.seaweed_window = deque(maxlen=window_size)
        self.whisky_window = deque(maxlen=window_size)
        
        # Analytics state
        self.alerts = []
        self.statistics = {}
        self.anomalies = []
        
        logger.info(f"✅ Real-time analytics initialized (window={window_size})")
    
    async def process_turtle_stream(self, data: Dict[str, Any]):
        """
        Process incoming turtle population data in real-time
        
        PLACEHOLDER: Data format pending
        Expected format:
        {
            "timestamp": "2025-11-01T12:00:00Z",
            "location": {"lat": 56.0, "lon": -3.0},
            "count": 15,
            "nesting_success_rate": 0.65,
            "temperature": 18.5
        }
        """
        
        self.turtle_window.append(data)
        
        # Real-time anomaly detection
        if len(self.turtle_window) >= 10:
            recent_counts = [d['count'] for d in list(self.turtle_window)[-10:]]
            mean_count = np.mean(recent_counts)
            std_count = np.std(recent_counts)
            
            if abs(data['count'] - mean_count) > 2 * std_count:
                alert = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'type': 'TURTLE_ANOMALY',
                    'severity': 'HIGH',
                    'message': f"Unusual turtle count detected: {data['count']} (expected ~{mean_count:.1f})",
                    'data': data
                }
                self.alerts.append(alert)
                logger.warning(f"🚨 {alert['message']}")
        
        # Update statistics
        self._update_statistics('turtle', data)
        
        return self.get_current_state()
    
    async def process_seaweed_stream(self, data: Dict[str, Any]):
        """
        Process incoming seaweed sensor data in real-time
        
        PLACEHOLDER: Data format pending
        Expected format:
        {
            "timestamp": "2025-11-01T12:00:00Z",
            "biomass_kg_per_m2": 4.2,
            "health_index": 0.85,
            "water_temperature": 12.0
        }
        """
        
        self.seaweed_window.append(data)
        
        # Real-time trend detection
        if len(self.seaweed_window) >= 20:
            recent_biomass = [d['biomass_kg_per_m2'] for d in list(self.seaweed_window)[-20:]]
            
            # Simple trend detection using linear fit
            x = np.arange(len(recent_biomass))
            slope = np.polyfit(x, recent_biomass, 1)[0]
            
            if slope < -0.1:  # Declining trend
                alert = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'type': 'SEAWEED_DECLINE',
                    'severity': 'MEDIUM',
                    'message': f"Seaweed biomass declining (trend: {slope:.3f} kg/m²/reading)",
                    'data': data,
                    'recommendation': 'Consider delaying harvest by 2-3 weeks'
                }
                self.alerts.append(alert)
                logger.warning(f"🌊 {alert['message']}")
        
        self._update_statistics('seaweed', data)
        
        return self.get_current_state()
    
    async def process_whisky_stream(self, data: Dict[str, Any]):
        """
        Process incoming whisky warehouse sensor data in real-time
        
        PLACEHOLDER: Data format pending
        Expected format:
        {
            "timestamp": "2025-11-01T12:00:00Z",
            "warehouse_id": "EDI-W-001",
            "ambient_temperature": 15.5,
            "humidity": 65.0,
            "cooling_load_kw": 12.3
        }
        """
        
        self.whisky_window.append(data)
        
        # Real-time temperature monitoring
        temp = data.get('ambient_temperature', 0)
        optimal_temp = 15.0
        tolerance = 2.0
        
        if abs(temp - optimal_temp) > tolerance:
            severity = 'CRITICAL' if abs(temp - optimal_temp) > 3.0 else 'MEDIUM'
            
            alert = {
                'timestamp': datetime.utcnow().isoformat(),
                'type': 'WAREHOUSE_TEMPERATURE',
                'severity': severity,
                'message': f"Warehouse {data['warehouse_id']} temperature deviation: {temp}°C (optimal: {optimal_temp}°C)",
                'data': data,
                'recommendation': 'Adjust HVAC setpoint immediately' if severity == 'CRITICAL' else 'Monitor closely'
            }
            self.alerts.append(alert)
            logger.warning(f"🥃 {alert['message']}")
        
        # Predictive cooling load
        if len(self.whisky_window) >= 30:
            recent_loads = [d.get('cooling_load_kw', 0) for d in list(self.whisky_window)[-30:]]
            predicted_peak = max(recent_loads) * 1.15  # 15% buffer
            
            if data.get('cooling_load_kw', 0) > predicted_peak * 0.9:
                alert = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'type': 'COOLING_CAPACITY',
                    'severity': 'LOW',
                    'message': f"Approaching peak cooling capacity: {data.get('cooling_load_kw')}kW (predicted peak: {predicted_peak:.1f}kW)",
                    'data': data
                }
                self.alerts.append(alert)
        
        self._update_statistics('whisky', data)
        
        return self.get_current_state()
    
    def _update_statistics(self, stream_type: str, data: Dict[str, Any]):
        """Update running statistics for each stream"""
        
        if stream_type not in self.statistics:
            self.statistics[stream_type] = {
                'count': 0,
                'last_update': None,
                'data_rate': 0
            }
        
        stats = self.statistics[stream_type]
        stats['count'] += 1
        stats['last_update'] = datetime.utcnow().isoformat()
        
        # Calculate data rate (readings per minute)
        if stream_type == 'turtle' and len(self.turtle_window) >= 2:
            window = self.turtle_window
        elif stream_type == 'seaweed' and len(self.seaweed_window) >= 2:
            window = self.seaweed_window
        elif stream_type == 'whisky' and len(self.whisky_window) >= 2:
            window = self.whisky_window
        else:
            return
        
        # Estimate data rate
        if len(window) >= 2:
            stats['data_rate'] = len(window) / 5  # Approximate per minute
    
    def get_current_state(self) -> Dict[str, Any]:
        """
        Get current state of all real-time analytics
        
        Returns comprehensive snapshot for dashboard
        """
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'statistics': self.statistics,
            'recent_alerts': self.alerts[-10:],  # Last 10 alerts
            'data_windows': {
                'turtle': len(self.turtle_window),
                'seaweed': len(self.seaweed_window),
                'whisky': len(self.whisky_window)
            },
            'health': {
                'turtle_stream': 'HEALTHY' if len(self.turtle_window) > 0 else 'NO_DATA',
                'seaweed_stream': 'HEALTHY' if len(self.seaweed_window) > 0 else 'NO_DATA',
                'whisky_stream': 'HEALTHY' if len(self.whisky_window) > 0 else 'NO_DATA'
            }
        }
    
    def get_alerts_by_severity(self, severity: str = None) -> List[Dict[str, Any]]:
        """Get alerts filtered by severity"""
        
        if severity:
            return [a for a in self.alerts if a['severity'] == severity]
        return self.alerts
    
    def clear_old_alerts(self, hours: int = 24):
        """Clear alerts older than specified hours"""
        
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        self.alerts = [
            a for a in self.alerts 
            if datetime.fromisoformat(a['timestamp'].replace('Z', '+00:00')) > cutoff
        ]


class StreamSimulator:
    """
    Simulate real-time data streams for testing
    
    PLACEHOLDER: Remove when actual streams are available
    """
    
    def __init__(self, analytics: RealTimeAnalytics):
        self.analytics = analytics
        self.running = False
    
    async def simulate_turtle_stream(self):
        """Simulate turtle data stream"""
        
        base_count = 15
        
        while self.running:
            data = {
                'timestamp': datetime.utcnow().isoformat(),
                'location': {'lat': 56.0, 'lon': -3.0, 'region': 'North Sea'},
                'count': int(base_count + np.random.normal(0, 3)),
                'nesting_success_rate': 0.65 + np.random.normal(0, 0.05),
                'temperature': 18.5 + np.random.normal(0, 1.0)
            }
            
            await self.analytics.process_turtle_stream(data)
            await asyncio.sleep(5)  # Every 5 seconds
    
    async def simulate_seaweed_stream(self):
        """Simulate seaweed sensor stream"""
        
        base_biomass = 4.2
        
        while self.running:
            data = {
                'timestamp': datetime.utcnow().isoformat(),
                'location': {'lat': 57.5, 'lon': -2.0, 'region': 'Aberdeenshire Coast'},
                'biomass_kg_per_m2': base_biomass + np.random.normal(0, 0.3),
                'health_index': 0.85 + np.random.normal(0, 0.05),
                'water_temperature': 12.0 + np.random.normal(0, 0.5)
            }
            
            await self.analytics.process_seaweed_stream(data)
            await asyncio.sleep(3)  # Every 3 seconds
    
    async def simulate_whisky_stream(self):
        """Simulate whisky warehouse sensor stream"""
        
        base_temp = 15.5
        
        while self.running:
            data = {
                'timestamp': datetime.utcnow().isoformat(),
                'warehouse_id': 'EDI-W-001',
                'location': {'lat': 55.95, 'lon': -3.19, 'city': 'Edinburgh'},
                'ambient_temperature': base_temp + np.random.normal(0, 1.5),
                'humidity': 65.0 + np.random.normal(0, 5.0),
                'cooling_load_kw': 12.3 + np.random.normal(0, 2.0)
            }
            
            await self.analytics.process_whisky_stream(data)
            await asyncio.sleep(2)  # Every 2 seconds
    
    async def start_simulation(self, duration_seconds: int = 60):
        """Start simulating all streams"""
        
        self.running = True
        
        logger.info(f"🚀 Starting real-time stream simulation for {duration_seconds} seconds...")
        
        # Run all streams in parallel
        tasks = [
            asyncio.create_task(self.simulate_turtle_stream()),
            asyncio.create_task(self.simulate_seaweed_stream()),
            asyncio.create_task(self.simulate_whisky_stream())
        ]
        
        # Run for specified duration
        await asyncio.sleep(duration_seconds)
        
        self.running = False
        
        # Cancel tasks
        for task in tasks:
            task.cancel()
        
        logger.info("✅ Simulation complete")


# Example usage for G-Research challenge demonstration
async def main():
    print("📊 G-Research Challenge: Real-Time Data Analytics Demo")
    print("=" * 70)
    
    # Initialize analytics
    analytics = RealTimeAnalytics(window_size=100)
    
    # Start simulator (PLACEHOLDER)
    simulator = StreamSimulator(analytics)
    await simulator.start_simulation(duration_seconds=30)
    
    # Get final state
    state = analytics.get_current_state()
    
    print("\n📈 Real-Time Analytics Summary:")
    print(json.dumps(state, indent=2))
    
    print(f"\n🚨 Total Alerts: {len(analytics.alerts)}")
    for alert in analytics.alerts[-5:]:
        print(f"  - [{alert['severity']}] {alert['message']}")


if __name__ == "__main__":
    asyncio.run(main())
