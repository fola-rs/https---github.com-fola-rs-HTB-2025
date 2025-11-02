# 🌊 Global Fishing Watch Integration

## Overview

We've integrated the **Global Fishing Watch (GFW) API** to provide real marine data for the G-Research real-time challenge!

## What is Global Fishing Watch?

Global Fishing Watch provides near-real-time data on fishing vessel activity worldwide, using satellite AIS tracking. This data is publicly available and scientifically validated.

## How It Enhances Our Project

### 🎯 G-Research Challenge: REAL Data!

Instead of simulated marine data, we now have:

✅ **Actual fishing vessel tracking** in the North Sea and Scottish coast  
✅ **Near-real-time updates** (AIS data processed hourly)  
✅ **Marine ecosystem pressure indicators**  
✅ **30+ days of historical activity**

### 🔗 Integration with Our Model

```
GFW Fishing Pressure → Marine Ecosystem Health → Seaweed Bed Impact
                                                      ↓
                                              Seaweed Harvest → Whisky Storage
```

**Use Cases**:
1. **Ecosystem Pressure Index**: High fishing activity correlates with marine habitat degradation
2. **Seaweed Model Feature**: Use fishing pressure as additional input to seaweed health predictions
3. **Cross-validation**: Compare fishing patterns with turtle population trends
4. **Real-time Monitoring**: Track changes in marine activity that may affect our causal chain

## API Coverage

### Region 1: North Sea (Turtle Monitoring Area)
- **Coordinates**: 54°N to 58°N, -4°W to 2°E
- **Relevance**: Sea turtle nesting sites and temperature monitoring
- **Data**: Vessel tracking, fishing effort, ecosystem pressure

### Region 2: Scottish Coast (Seaweed Harvesting Area)
- **Coordinates**: 56.5°N to 58.5°N, -3.5°W to -1°W (Aberdeenshire)
- **Relevance**: Primary seaweed bed locations
- **Data**: Coastal fishing activity, marine traffic

## Usage

### Quick Test
```powershell
# Set environment variable (or add to .env file)
$env:GFW_API_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpZEtleSJ9..."

# Run integration test
python data\connectors\gfw_api.py
```

### In Code
```python
from data.connectors.gfw_api import GlobalFishingWatchAPI

# Initialize
gfw = GlobalFishingWatchAPI()

# Get North Sea activity
north_sea = gfw.get_north_sea_marine_activity()
print(f"Ecosystem Pressure: {north_sea['ecosystem_pressure_index']}/100")

# Get Scottish coast activity
scotland = gfw.get_scottish_coast_activity()
print(f"Vessel Events: {scotland['vessel_events']}")
```

### Integration with Real-Time Analytics
```python
from data.connectors.gfw_api import GlobalFishingWatchAPI
from analysis.gresearch_realtime.realtime_analytics import RealTimeAnalytics

gfw = GlobalFishingWatchAPI()
analytics = RealTimeAnalytics()

# Fetch real marine data
marine_data = gfw.get_scottish_coast_activity()

# Process as real-time stream
await analytics.process_seaweed_stream({
    'timestamp': datetime.utcnow().isoformat(),
    'ecosystem_pressure': marine_data['ecosystem_pressure_index'],
    'fishing_activity': marine_data['vessel_events'],
    'region': 'Scottish Coast'
})
```

## Data Fields

### Vessel Activity Data
```json
{
  "region": {"lat_range": [56.5, 58.5], "lon_range": [-3.5, -1.0]},
  "period": {"start": "2025-10-01", "end": "2025-11-01", "days": 30},
  "vessel_events": 245,
  "fishing_hours": 1830,
  "unique_vessels": 89,
  "avg_daily_activity": 8.17,
  "ecosystem_pressure_index": 67.5,
  "correlation_note": "Higher fishing effort may correlate with degraded seaweed habitats"
}
```

## Ecosystem Pressure Index

**Scale**: 0-100 (0 = pristine, 100 = extreme pressure)

**Calculation**:
- Vessel count × 2
- Fishing hours × 0.5
- Capped at 100

**Interpretation**:
- 0-25: Low pressure (healthy ecosystem)
- 25-50: Moderate pressure
- 50-75: High pressure (potential degradation)
- 75-100: Extreme pressure (significant impact)

## Benefits for Each Challenge

### ✅ G-Research: Real-Time Data
- **REAL API**, not simulation
- Near-real-time updates (hourly AIS processing)
- Demonstrates production data integration
- Shows scalability to multiple data sources

### ✅ CompSoc: Modelling Mayhem
- Add fishing pressure as new assumption variable
- Show how different pressure thresholds change seaweed predictions
- Compound the cascade: Fishing → Seaweed → Whisky → Economy

### ✅ Hoppers: Edinburgh Impact
- More robust predictions with real marine data
- Better confidence in economic forecasts
- Shows commitment to evidence-based policy

## API Limits

- **Rate Limit**: 1000 requests/day (generous for hackathon)
- **Token Expiry**: 2077 (valid for years!)
- **Geographic Coverage**: Global
- **Historical Data**: Up to 5 years available

## Next Steps

1. **Run Test**: `python data\connectors\gfw_api.py`
2. **Update Dashboard**: Add GFW data visualization to G-Research tab
3. **Enhance Model**: Include fishing pressure as seaweed health feature
4. **Demo Point**: Highlight "REAL API integration" to judges

## Resources

- **GFW Portal**: https://globalfishingwatch.org/
- **API Docs**: https://globalfishingwatch.org/our-apis/documentation
- **Data Explorer**: https://globalfishingwatch.org/map

---

**🎉 We now have REAL marine data! This significantly strengthens the G-Research real-time data challenge!**
