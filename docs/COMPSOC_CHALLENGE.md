# Tides & Tomes - Challenge Documentation

## CompSoc Challenge: Modelling Mayhem

### Objective
Demonstrate how small modelling assumptions drastically alter results in our cross-domain prediction system.

### Success Criteria
- **Minimal assumption change → Maximum result variance**
- Clear documentation of each assumption
- Side-by-side comparison of outcomes
- Reflection on real-world implications

### Our Approach

#### Assumption 1: Sea Turtle Nesting Success Rate
**Base Assumption**: 65% nesting success rate

**Variations Tested**: ±5%, ±10%, ±15%

**Why This Matters**:
- Nesting success is a biological parameter with natural variation
- Small changes in methodology (counting period, site selection) can shift this percentage
- Yet this seemingly minor change cascades through the entire system

**Results**:
- ±5% nesting change → ±£31M economic impact
- ±10% nesting change → ±£62M economic impact  
- ±15% nesting change → ±£93M economic impact

**Key Insight**: A 5% biological assumption change (well within measurement uncertainty) creates a £31M economic swing for Edinburgh.

#### Assumption 2: Temperature Anomaly Threshold
**Question**: What constitutes a "significant" temperature change?

**Thresholds Tested**: 0.5°C, 1.0°C, 1.5°C, 2.0°C, 2.5°C

**Why This Matters**:
- Same temperature data, different thresholds
- Affects alert frequency and operational response
- Changes perception of risk severity

**Results**:
- 0.5°C threshold → 10 alerts/year, £50k cost
- 1.0°C threshold → 6 alerts/year, £30k cost
- 2.0°C threshold → 2 alerts/year, £10k cost

**Key Insight**: The choice of what counts as "significant" dramatically changes operational behavior and costs, even though the underlying data is identical.

#### Assumption 3: Seaweed Biological Growth Rate
**Base Assumption**: 12% monthly regrowth rate

**Variations Tested**: ±2%, ±4%, ±6% absolute

**Why This Matters**:
- Biological growth rates are difficult to measure precisely
- Seasonal variation, measurement methodology affect estimates
- Determines sustainable harvest levels

**Results**:
- -6% growth assumption → 1,234 kg annual biomass (ecosystem at risk)
- Baseline (12%) → 3,896 kg annual biomass (stable)
- +6% growth assumption → 12,023 kg annual biomass (thriving)

**Key Insight**: A 6% absolute difference in growth rate assumption (well within biological variability) changes ecosystem assessment from "at risk" to "thriving".

#### Assumption 4: Whisky Aging Temperature Sensitivity
**Question**: How much does 1°C ambient temperature change affect aging rate?

**Base Assumption**: 3% change per °C

**Variations Tested**: ±1%, ±2%, ±3% absolute

**Why This Matters**:
- Industrial parameter based on expert knowledge
- Difficult to isolate from other factors
- Affects multi-million pound inventory valuation

**Results**:
- 0% sensitivity → Minimal aging impact, low inventory risk
- 3% sensitivity → Moderate impacts, medium risk
- 6% sensitivity → High volatility, £3M inventory risk

**Key Insight**: Same warehouse temperature readings produce vastly different aging predictions based on this single sensitivity parameter.

### Reflection: Why This Matters

Our analysis demonstrates that:

1. **Hidden Assumptions Have Visible Consequences**: Small modelling choices (often buried in methodology sections) can swing results by tens of millions of pounds.

2. **Same Data, Different Stories**: The 0.5°C vs 2.0°C threshold example shows how identical datasets can justify opposite conclusions about urgency and risk.

3. **Cascade Effects Amplify Uncertainty**: In interconnected systems like ours, small uncertainties in one domain (turtle biology) propagate and amplify through each subsequent link (seaweed → temperature → whisky → economy).

4. **Policy Implications**: Decision-makers relying on our predictions need to understand:
   - Which assumptions drive the results
   - How sensitive conclusions are to those assumptions
   - The uncertainty ranges, not just point estimates

5. **Transparency Is Critical**: By explicitly showing our assumptions and their impacts, we enable:
   - Informed policy decisions
   - Productive scientific debate
   - Trust in the modelling process

### How to Run the Analysis

```powershell
# Navigate to analysis directory
cd c:\htb67\analysis\compsoc_sensitivity

# Run sensitivity analysis
python sensitivity_analyzer.py

# Output:
# - Console report showing all comparisons
# - compsoc_sensitivity_analysis.png visualization
```

### Files
- `analysis/compsoc_sensitivity/sensitivity_analyzer.py` - Main analysis code
- `docs/COMPSOC_CHALLENGE.md` - This document
- Results will be saved to workspace root

---

## Datasets Used

We analyze relationships between:

1. **Sea Turtle Data** (NOAA-style data)
   - Nesting counts and success rates
   - Temperature monitoring
   - Population dynamics

2. **Seaweed Monitoring** (Marine Scotland-style data)
   - Biomass measurements
   - Health indices
   - Harvest records

3. **Whisky Storage** (Industrial sensor data)
   - Warehouse temperature logs
   - Humidity readings
   - Cooling system load

4. **Economic Data**
   - Edinburgh employment statistics
   - Tourism revenue (VisitScotland data)
   - Whisky export values (Scotch Whisky Association)

### Transparency Note

All assumptions are documented in code comments and can be reviewed. We encourage:
- Questioning our parameter choices
- Testing alternative assumptions
- Suggesting improvements based on domain expertise

This is science in the open, showing both the power and fragility of data-driven models.
