"""
Test script for production-ready dashboard components
"""

from presentation.config import config
from presentation.api_services import weatherbit_service, noaa_service, gfw_service
from presentation.data_analysis import analyzer

print("="*60)
print("Testing Production Dashboard Components")
print("="*60)

# Test 1: Config
print("\n1. Testing Configuration...")
validation = config.validate_api_keys()
print(f"   API Keys Present: {validation['all_present']}")
print(f"   Status: {validation['status']}")

# Test 2: Weatherbit
print("\n2. Testing Weatherbit Service...")
try:
    weather = weatherbit_service.get_current_weather('Edinburgh')
    print(f"   ✓ Edinburgh: {weather['temperature']}°C - {weather['description']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: NOAA
print("\n3. Testing NOAA Service...")
try:
    datasets = noaa_service.get_datasets()
    print(f"   ✓ Retrieved {len(datasets)} climate datasets")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Global Fishing Watch
print("\n4. Testing Global Fishing Watch Service...")
try:
    from datetime import datetime, timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    fishing = gfw_service.get_fishing_events(
        start_date=start_date.strftime('%Y-%m-%dT00:00:00.000Z'),
        end_date=end_date.strftime('%Y-%m-%dT23:59:59.999Z'),
        limit=5
    )
    print(f"   ✓ Retrieved {fishing['count']} fishing events")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Data Analysis
print("\n5. Testing Data Analyzer...")
try:
    historical = analyzer.generate_environmental_timeseries(days=30)
    print(f"   ✓ Generated {len(historical)} days of data")
    print(f"   ✓ Columns: {list(historical.columns)}")
    
    # Check correlations
    corr = historical[['seaweed_health', 'habitat_quality']].corr().iloc[0, 1]
    print(f"   ✓ Seaweed-Habitat correlation: {corr:.3f}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*60)
print("All component tests completed!")
print("="*60)
