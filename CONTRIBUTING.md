# Contributing to Tides & Tomes

## Welcome!

Thank you for your interest in contributing to Tides & Tomes! This project was created for Hack the Burgh and addresses three challenges: CompSoc (Modelling Mayhem), G-Research (Real-Time Data), and Hoppers (Edinburgh Impact).

## How to Contribute

### 1. Improve Data Connectors

**Status**: Currently using placeholders awaiting real data formats

**How to help**:
- Implement actual API connections to NOAA, Marine Scotland, etc.
- Add authentication and rate limiting
- Improve error handling and retry logic
- Add data validation schemas

**Files**: `data/connectors/base.py`

### 2. Enhance Models

**Current**: Simplified cascade models for demonstration

**Improvements needed**:
- Train on historical data
- Implement ensemble methods (XGBoost + Prophet)
- Add uncertainty quantification
- Improve causal inference (use DoWhy or EconML)

**Files**: `models/` directory (to be created)

### 3. Expand Analytics

**Ideas**:
- Add more sensitivity analyses for CompSoc challenge
- Implement spatial clustering for sensor networks
- Create historical playback feature
- Add seasonality decomposition

**Files**: `analysis/` subdirectories

### 4. Improve Dashboard

**Current**: Streamlit prototype

**Enhancements**:
- Migrate to React + Plotly Dash for production
- Add user authentication
- Implement role-based views
- Create mobile-responsive design
- Add data export features

**Files**: `dashboard/app.py`

### 5. Documentation

**Always appreciated**:
- Fix typos and improve clarity
- Add code examples
- Create tutorials
- Document edge cases

**Files**: `docs/` and inline comments

## Development Setup

```powershell
# Clone repository
git clone <repository-url>
cd htb67

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies (testing, linting)
pip install pytest pytest-cov black flake8 mypy
```

## Code Style

- **Python**: Follow PEP 8
- **Comments**: Explain WHY, not WHAT
- **Docstrings**: Use Google style
- **Type hints**: Encouraged for new code

**Format before committing**:
```powershell
black .
flake8 .
```

## Testing

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

**Please add tests for**:
- New data connectors
- Analytics functions
- API endpoints
- Utility functions

## Pull Request Process

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make changes** with clear commit messages
4. **Test thoroughly**
5. **Update documentation** if needed
6. **Submit PR** with description of changes

## Priority Areas Post-Hackathon

### High Priority
1. 🔴 Integrate real data sources (waiting on partnerships)
2. 🔴 Deploy to cloud (Azure or AWS)
3. 🔴 Add comprehensive test suite

### Medium Priority
1. 🟡 Improve model accuracy with historical data
2. 🟡 Create mobile app for alerts
3. 🟡 Add multi-language support (Gaelic!)

### Low Priority
1. 🟢 Migrate dashboard to React
2. 🟢 Add admin panel
3. 🟢 Create public API with rate limiting

## Questions?

Open an issue or contact the team!

## Code of Conduct

Be kind, be respectful, be constructive. We're all here to learn and build something meaningful for Edinburgh.

## License

MIT License - See LICENSE file for details

---

**Thank you for contributing to Tides & Tomes! 🌊🐢🥃**
