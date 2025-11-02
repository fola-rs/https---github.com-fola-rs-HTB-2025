# Tides & Tomes: A Cross-Domain Predictor

## Project Overview
A data-driven system linking sea turtle populations, seaweed harvests, and whisky aging conditions through predictive modeling and real-time data analysis.

## Challenge Linkages

### 🎯 CompSoc Challenge: Modelling Mayhem
**Focus**: Demonstrating how small changes in sea turtle population assumptions drastically affect whisky production predictions in Edinburgh.

**Success Criteria**: Minimal assumption change → Maximum result variance

**Key Assumptions to Explore**:
- Sea turtle nesting success rate variations (±5%, ±10%, ±15%)
- Temperature anomaly thresholds (0.5°C vs 1.0°C vs 2.0°C)
- Seaweed regrowth coefficients (biological growth rate assumptions)
- Whisky aging temperature sensitivity parameters

### 📊 G-Research Challenge: Real-Time Data
**Focus**: Real-time monitoring and analytics of sea turtle populations, seaweed harvesting, and whisky storage conditions.

**Implementation**: Live dashboards with streaming data ingestion (currently using placeholders)

### 🏙️ Hoppers Edinburgh Challenge
**Focus**: Impact on Edinburgh residents through whisky industry stability and economic forecasting.

**Key Impacts**:
- Whisky is Scotland's largest food & drink export (£6.2B annually)
- Edinburgh is home to major distilleries and warehouses
- Tourism and local employment heavily tied to whisky heritage
- Predictive alerts help stabilize supply chains and pricing

## Project Structure

```
htb67/
├── data/                          # Data ingestion and storage
│   ├── raw/                       # Raw data feeds (placeholders)
│   ├── processed/                 # Cleaned and harmonized data
│   └── connectors/                # API and sensor connectors
├── models/                        # Predictive models
│   ├── baseline/                  # Simple time series models
│   ├── causal/                    # Causal inference models
│   └── ensemble/                  # Production models
├── analysis/                      # Challenge-specific analysis
│   ├── compsoc_sensitivity/       # Parameter sensitivity analysis
│   ├── greesearch_realtime/       # Real-time analytics demos
│   └── hoppers_impact/            # Edinburgh impact assessment
├── dashboard/                     # Web interface
├── api/                          # Model serving API
├── notebooks/                     # Jupyter notebooks for EDA
├── tests/                        # Unit and integration tests
├── docs/                         # Documentation
└── deployment/                   # Docker and deployment configs
```

## Quick Start

### Installation
```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Run Dashboard
```powershell
streamlit run dashboard/app.py
```

### Run API
```powershell
uvicorn api.main:app --reload
```

## Development Status

⚠️ **Real-time data handling**: Currently using placeholders. Awaiting final data format and preferred ingestion method.

## Team
Hack the Burgh 12 - Team Tides & Tomes

## License
MIT License (Hackathon Project)
