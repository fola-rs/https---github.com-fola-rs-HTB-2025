"""
FastAPI Server for Model Predictions
====================================

Serves predictions and real-time analytics via REST API
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import uvicorn
import asyncio
import json

app = FastAPI(
    title="Tides & Tomes API",
    description="Cross-domain prediction API linking sea turtles, seaweed, and whisky",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class PredictionRequest(BaseModel):
    turtle_nesting_rate: float
    sea_temperature: float
    location: str
    forecast_days: int = 7


class PredictionResponse(BaseModel):
    timestamp: str
    seaweed_harvest_change_percent: float
    whisky_production_impact_percent: float
    edinburgh_economic_impact_gbp: float
    confidence_interval: Dict[str, float]
    recommendations: List[str]


class AlertSubscription(BaseModel):
    email: Optional[str] = None
    webhook_url: Optional[str] = None
    alert_types: List[str] = ["TURTLE_ANOMALY", "WAREHOUSE_TEMPERATURE", "SEAWEED_DECLINE"]
    severity_threshold: str = "MEDIUM"


# In-memory storage (replace with database)
active_connections: List[WebSocket] = []
alert_subscriptions: List[AlertSubscription] = []


@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "healthy",
        "service": "Tides & Tomes API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/v1/status")
async def get_status():
    """Get system status"""
    return {
        "data_streams": {
            "turtle": {"status": "PLACEHOLDER", "last_update": datetime.utcnow().isoformat()},
            "seaweed": {"status": "PLACEHOLDER", "last_update": datetime.utcnow().isoformat()},
            "whisky": {"status": "PLACEHOLDER", "last_update": datetime.utcnow().isoformat()}
        },
        "models": {
            "baseline": "loaded",
            "ensemble": "loaded",
            "causal": "loaded"
        },
        "active_websockets": len(active_connections),
        "alert_subscriptions": len(alert_subscriptions)
    }


@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Generate prediction based on current conditions
    
    PLACEHOLDER: Replace with actual model inference
    """
    
    # Simplified prediction model (replace with actual trained model)
    base_nesting = 0.65
    rate_change = (request.turtle_nesting_rate - base_nesting) / base_nesting
    
    seaweed_change = rate_change * 100 * 0.8
    whisky_impact = seaweed_change * 0.3
    economic_impact = whisky_impact * 62  # £62M per 1%
    
    # Generate recommendations
    recommendations = []
    if abs(seaweed_change) > 5:
        recommendations.append(f"Adjust seaweed harvest schedule by {int(abs(seaweed_change))} days")
    if abs(whisky_impact) > 2:
        recommendations.append("Review warehouse cooling capacity")
    if abs(economic_impact) > 50:
        recommendations.append("Alert Edinburgh stakeholders of potential impact")
    
    return PredictionResponse(
        timestamp=datetime.utcnow().isoformat(),
        seaweed_harvest_change_percent=round(seaweed_change, 2),
        whisky_production_impact_percent=round(whisky_impact, 2),
        edinburgh_economic_impact_gbp=round(economic_impact * 1e6, 2),
        confidence_interval={
            "lower": round(economic_impact * 0.85, 2),
            "upper": round(economic_impact * 1.15, 2)
        },
        recommendations=recommendations if recommendations else ["No action required"]
    )


@app.post("/api/v1/alerts/subscribe")
async def subscribe_alerts(subscription: AlertSubscription):
    """Subscribe to alert notifications"""
    alert_subscriptions.append(subscription)
    return {
        "status": "subscribed",
        "subscription_id": len(alert_subscriptions) - 1,
        "alert_types": subscription.alert_types
    }


@app.get("/api/v1/alerts/recent")
async def get_recent_alerts(limit: int = 10):
    """Get recent alerts"""
    
    # PLACEHOLDER: Replace with actual alert history
    sample_alerts = [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "TURTLE_ANOMALY",
            "severity": "HIGH",
            "message": "Unusual turtle count detected",
            "location": "North Sea"
        }
    ]
    
    return {"alerts": sample_alerts[:limit]}


@app.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time data streaming
    
    PLACEHOLDER: Connect to actual data streams when format is ready
    """
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Simulate real-time data (replace with actual stream)
            data = {
                "timestamp": datetime.utcnow().isoformat(),
                "streams": {
                    "turtle": {"count": 15, "temp": 18.5},
                    "seaweed": {"biomass": 4.2, "health": 0.85},
                    "whisky": {"temp": 15.5, "humidity": 65.0}
                }
            }
            
            await websocket.send_json(data)
            await asyncio.sleep(2)  # Update every 2 seconds
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.get("/api/v1/compsoc/sensitivity")
async def get_sensitivity_analysis(
    parameter: str = "nesting_rate",
    variation: float = 0.1
):
    """
    CompSoc Challenge: Get sensitivity analysis for a parameter
    
    Args:
        parameter: One of 'nesting_rate', 'temperature_threshold', 'seaweed_growth', 'aging_sensitivity'
        variation: Variation amount (e.g., 0.1 for ±10%)
    """
    
    results = []
    
    if parameter == "nesting_rate":
        base = 0.65
        for v in [-variation, 0, variation]:
            adjusted = base * (1 + v)
            economic = v * 100 * 0.8 * 0.3 * 62
            results.append({
                "variation": f"{v*100:+.1f}%",
                "nesting_rate": adjusted,
                "economic_impact_gbp_millions": round(economic, 2)
            })
    
    return {
        "parameter": parameter,
        "results": results,
        "interpretation": "Small assumption changes create large outcome differences"
    }


@app.get("/api/v1/hoppers/edinburgh-impact")
async def get_edinburgh_impact(scenario: str = "baseline"):
    """
    Hoppers Challenge: Get Edinburgh resident impact for a scenario
    
    Args:
        scenario: One of 'baseline', 'mild', 'moderate', 'severe', 'positive'
    """
    
    impacts = {
        "baseline": {"jobs": 0, "income": 0, "tourism": 0, "quality_of_life": 7.5},
        "mild": {"jobs": 90, "income": -45000, "tourism": -2.4, "quality_of_life": 7.2},
        "moderate": {"jobs": 180, "income": -90000, "tourism": -4.8, "quality_of_life": 6.8},
        "severe": {"jobs": 270, "income": -135000, "tourism": -7.2, "quality_of_life": 6.0},
        "positive": {"jobs": -150, "income": 75000, "tourism": 4.0, "quality_of_life": 8.5}
    }
    
    if scenario not in impacts:
        raise HTTPException(status_code=400, detail="Invalid scenario")
    
    return {
        "scenario": scenario,
        "impacts": impacts[scenario],
        "residents_affected": 524930,
        "interpretation": "Environmental changes directly affect Edinburgh residents through the whisky industry"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
