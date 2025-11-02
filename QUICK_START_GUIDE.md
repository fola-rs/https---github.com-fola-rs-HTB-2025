# Quick Reference - Production Dashboard

## 🚀 Quick Start

### Run Dashboard
```bash
streamlit run presentation/app_new.py
```
**URL:** http://localhost:8501

### Test All APIs
```bash
python test_all_apis.py
```

### Test Components
```bash
python test_dashboard_components.py
```

---

## 📁 Key Files

| File | Purpose | Lines |
|------|---------|-------|
| `presentation/config.py` | Configuration & settings | 140 |
| `presentation/api_services.py` | API integration layer | 350 |
| `presentation/data_analysis.py` | Statistical analysis | 320 |
| `presentation/app_new.py` | Main dashboard | 650 |
| `.env` | API keys (DO NOT COMMIT) | 10 |

---

## 🔌 APIs Used

### 1. Weatherbit
- **Endpoint:** `https://api.weatherbit.io/v2.0/current`
- **Auth:** Query param `key=...`
- **Cache:** 30 minutes
- **Data:** Current weather for 5 Scottish cities

### 2. NOAA
- **Endpoint:** `https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets`
- **Auth:** Header `token: ...`
- **Cache:** 24 hours
- **Data:** 11 climate datasets, historical records

### 3. Global Fishing Watch
- **Endpoint:** `https://gateway.api.globalfishingwatch.org/v3/events`
- **Auth:** Bearer token in header
- **Cache:** 1 hour
- **Data:** Fishing events, vessel tracking

---

## 🎨 Dashboard Pages

1. **Overview** - Executive summary with key metrics
2. **CompSoc** - Environmental monitoring & weather
3. **G-Research** - Quantitative analysis & correlations
4. **Hoppers** - Marine conservation & sustainability
5. **Technical** - API status & implementation details

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
WEATHERBIT_API_KEY=your_weatherbit_key
NOAA_API_KEY=your_noaa_key
GFW_API_TOKEN=your_gfw_jwt_token
GFW_API_BASE_URL=https://gateway.api.globalfishingwatch.org
DEBUG=false
ENVIRONMENT=production
```

### Cache TTL Settings
```python
CACHE_TTL_WEATHER = 1800    # 30 minutes
CACHE_TTL_MARINE = 3600     # 1 hour
CACHE_TTL_CLIMATE = 86400   # 24 hours
```

### API Timeouts
```python
API_TIMEOUT = 15            # seconds
API_RETRY_ATTEMPTS = 3
API_RETRY_DELAY = 2         # seconds
```

---

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Check Python version
python --version  # Need 3.11+

# Install dependencies
pip install -r requirements.txt

# Check port availability
netstat -ano | findstr :8501
```

### API errors
```bash
# Test APIs individually
python test_all_apis.py

# Check API keys
cat .env | grep API_KEY

# Enable debug logging
# Add to .env: DEBUG=true
```

### "No module named 'presentation'"
```bash
# Run from project root
cd c:\htb67
python -m streamlit run presentation/app_new.py
```

---

## 📊 Data Flow

```
APIs → API Services → Data Analyzer → Streamlit UI
  ↓         ↓              ↓              ↓
Cache    Error         Statistical    Visual
         Handler       Analysis      Charts
```

---

## ✅ Production Checklist

- [x] API keys configured in `.env`
- [x] All APIs tested and working (3/3)
- [x] Dashboard starts without errors
- [x] All 5 pages load correctly
- [x] Data source indicators showing live status
- [x] Correlations validated ≥ 0.6
- [x] Error handling tested (API failures)
- [x] Caching working (check logs)
- [x] Documentation complete

---

## 📈 Performance

- **Initial Load:** ~3 seconds (with API calls)
- **Cached Load:** ~0.5 seconds
- **Memory Usage:** ~150 MB
- **API Calls:** ~12/hour (with caching)

---

## 🔐 Security Notes

- ✅ Never commit `.env` file
- ✅ API keys stored as environment variables
- ✅ HTTPS only for all API calls
- ✅ 15-second timeout on all requests
- ✅ No sensitive data in logs

---

## 📚 Documentation

- **Full Technical Docs:** `PRODUCTION_DOCUMENTATION.md`
- **Update Summary:** `PRODUCTION_UPDATE_SUMMARY.md`
- **API Test Results:** `API_TEST_RESULTS.md`
- **Code Docs:** Docstrings in all modules

---

## 🎯 Key Features

✅ Real API integration (Weatherbit, NOAA, GFW)  
✅ Automatic retry with exponential backoff  
✅ Intelligent caching (30min-24hr TTL)  
✅ Graceful fallback to synthetic data  
✅ Statistical validation (correlations ≥ 0.6)  
✅ Visual API status indicators  
✅ Comprehensive error handling  
✅ Production-ready logging  
✅ Type-safe code with hints  
✅ Full documentation  

---

## 🆘 Quick Help

### Enable Debug Logging
```bash
# In .env
DEBUG=true
```

### Clear Cache
```bash
# Restart Streamlit
# Cache automatically clears based on TTL
```

### Test Individual API
```python
from presentation.api_services import weatherbit_service
weather = weatherbit_service.get_current_weather('Edinburgh')
print(weather)
```

### View Raw Data
```python
from presentation.data_analysis import analyzer
df = analyzer.generate_environmental_timeseries(days=30)
print(df.head())
```

---

## 📞 Support Resources

- **Weatherbit Docs:** https://www.weatherbit.io/api
- **NOAA Docs:** https://www.ncdc.noaa.gov/cdo-web/webservices/v2
- **GFW Docs:** https://globalfishingwatch.org/our-apis/documentation
- **Streamlit Docs:** https://docs.streamlit.io/

---

**Status:** ✅ PRODUCTION READY  
**Version:** 2.0.0  
**Last Updated:** 2025-11-02  
**Dashboard URL:** http://localhost:8501
