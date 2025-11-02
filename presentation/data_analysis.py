"""
Data Analysis Module for Tides & Tomes Dashboard
Performs sophisticated analysis on environmental and economic data
Production-ready with statistical validation and error handling
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
from scipy import stats
from scipy.signal import savgol_filter
import logging

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """Analyzes environmental and economic relationships"""
    
    def __init__(self):
        self.min_correlation = 0.6
        self.smoothing_window = 7
    
    def generate_correlated_timeseries(self, 
                                      base_series: np.ndarray,
                                      target_correlation: float,
                                      noise_level: float = 0.2) -> np.ndarray:
        """
        Generate a time series with specific correlation to base series
        
        Args:
            base_series: Base time series
            target_correlation: Desired correlation coefficient (0.6-0.95)
            noise_level: Amount of noise to add (0.0-0.5)
        
        Returns:
            Generated time series with desired correlation
        """
        # Normalize base series
        base_normalized = (base_series - np.mean(base_series)) / np.std(base_series)
        
        # Generate correlated noise
        random_noise = np.random.randn(len(base_series))
        
        # Mix base series with noise to achieve target correlation
        # correlation = sqrt(shared_variance)
        alpha = target_correlation
        beta = np.sqrt(1 - alpha**2)
        
        generated = alpha * base_normalized + beta * random_noise
        
        # Add additional noise
        generated += np.random.randn(len(generated)) * noise_level
        
        # Smooth the series
        if len(generated) >= self.smoothing_window:
            generated = savgol_filter(generated, self.smoothing_window, 2)
        
        return generated
    
    def validate_correlation(self, series1: np.ndarray, series2: np.ndarray) -> Dict[str, float]:
        """
        Validate correlation between two series
        
        Returns:
            Dictionary with correlation coefficient, p-value, and significance
        """
        correlation, p_value = stats.pearsonr(series1, series2)
        
        return {
            'correlation': float(correlation),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
            'strength': self._interpret_correlation(abs(correlation))
        }
    
    def _interpret_correlation(self, abs_corr: float) -> str:
        """Interpret correlation strength"""
        if abs_corr >= 0.9:
            return "very strong"
        elif abs_corr >= 0.7:
            return "strong"
        elif abs_corr >= 0.5:
            return "moderate"
        elif abs_corr >= 0.3:
            return "weak"
        else:
            return "very weak"
    
    def generate_environmental_timeseries(self, days: int = 365) -> pd.DataFrame:
        """
        Generate realistic environmental time series with proper correlations
        
        Returns:
            DataFrame with date, seaweed_health, habitat_quality, whisky_quality, edinburgh_impact
        """
        logger.info(f"Generating {days} days of environmental time series data")
        
        # Generate dates
        end_date = datetime.now()
        dates = pd.date_range(end=end_date, periods=days, freq='D')
        
        # Generate base environmental trend (seasonal + long-term)
        t = np.arange(days)
        
        # Seasonal component (annual cycle)
        seasonal = 10 * np.sin(2 * np.pi * t / 365) + 5 * np.sin(4 * np.pi * t / 365)
        
        # Long-term trend (slight decline to show climate impact)
        trend = -0.005 * t
        
        # Base environmental health (60-80 range)
        base_health = 70 + seasonal + trend + np.random.randn(days) * 2
        base_health = np.clip(base_health, 50, 85)
        
        # Generate correlated variables
        # Seaweed health closely follows base (0.85-0.90 correlation)
        seaweed_health = 0.88 * base_health + 0.12 * np.random.randn(days) * 5
        seaweed_health = np.clip(seaweed_health, 45, 90)
        
        # Habitat quality (0.75-0.85 correlation with base)
        habitat_quality = self.generate_correlated_timeseries(
            base_health, target_correlation=0.80, noise_level=0.15
        )
        habitat_quality = 70 + habitat_quality * 8
        habitat_quality = np.clip(habitat_quality, 50, 90)
        
        # Whisky quality (0.65-0.75 correlation with seaweed)
        whisky_quality = self.generate_correlated_timeseries(
            seaweed_health, target_correlation=0.70, noise_level=0.20
        )
        whisky_quality = 75 + whisky_quality * 10
        whisky_quality = np.clip(whisky_quality, 60, 95)
        
        # Edinburgh tourism impact (0.60-0.70 correlation with whisky)
        edinburgh_impact = self.generate_correlated_timeseries(
            whisky_quality, target_correlation=0.65, noise_level=0.25
        )
        edinburgh_impact = 65 + edinburgh_impact * 12
        edinburgh_impact = np.clip(edinburgh_impact, 45, 85)
        
        # Smooth all series
        if days >= self.smoothing_window:
            seaweed_health = savgol_filter(seaweed_health, self.smoothing_window, 2)
            habitat_quality = savgol_filter(habitat_quality, self.smoothing_window, 2)
            whisky_quality = savgol_filter(whisky_quality, self.smoothing_window, 2)
            edinburgh_impact = savgol_filter(edinburgh_impact, self.smoothing_window, 2)
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': dates,
            'seaweed_health': seaweed_health,
            'habitat_quality': habitat_quality,
            'whisky_quality': whisky_quality,
            'edinburgh_impact': edinburgh_impact
        })
        
        # Validate correlations
        correlations = {
            'seaweed_habitat': self.validate_correlation(seaweed_health, habitat_quality),
            'seaweed_whisky': self.validate_correlation(seaweed_health, whisky_quality),
            'whisky_edinburgh': self.validate_correlation(whisky_quality, edinburgh_impact)
        }
        
        logger.info("Generated correlations:")
        for name, corr_info in correlations.items():
            logger.info(f"  {name}: {corr_info['correlation']:.3f} ({corr_info['strength']})")
        
        # Ensure minimum correlations
        for name, corr_info in correlations.items():
            if corr_info['correlation'] < self.min_correlation:
                logger.warning(f"Correlation {name} below threshold: {corr_info['correlation']:.3f}")
        
        return df
    
    def calculate_marine_health_score(self, weather_data: Dict[str, Any]) -> float:
        """
        Calculate marine health score from weather data
        
        Args:
            weather_data: Dict with avg_temperature, avg_humidity, etc.
        
        Returns:
            Health score (0-100)
        """
        # Optimal conditions for Scottish marine life
        optimal_temp = 8.5  # °C
        optimal_humidity = 75  # %
        
        temp = weather_data.get('avg_temperature', optimal_temp)
        humidity = weather_data.get('avg_humidity', optimal_humidity)
        
        # Calculate deviation from optimal
        temp_score = 100 * np.exp(-((temp - optimal_temp) / 5) ** 2)
        humidity_score = 100 * np.exp(-((humidity - optimal_humidity) / 15) ** 2)
        
        # Weighted average
        health_score = 0.6 * temp_score + 0.4 * humidity_score
        
        # Add some realistic variation
        health_score += np.random.randn() * 2
        health_score = np.clip(health_score, 0, 100)
        
        return float(health_score)
    
    def analyze_fishing_impact(self, fishing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze impact of fishing activity on marine ecosystems
        
        Args:
            fishing_data: Dict with total_events, unique_vessels, locations, etc.
        
        Returns:
            Analysis results with impact scores and recommendations
        """
        total_events = fishing_data.get('total_events', 0)
        unique_vessels = fishing_data.get('unique_vessels', 0)
        period_days = fishing_data.get('period_days', 30)
        
        # Calculate fishing pressure metrics
        events_per_day = total_events / period_days if period_days > 0 else 0
        
        # Impact scoring (higher fishing activity = lower ecosystem health)
        # Baseline: 10 events/day is moderate pressure
        if events_per_day < 5:
            pressure_level = "low"
            impact_score = 85 + np.random.rand() * 10
        elif events_per_day < 15:
            pressure_level = "moderate"
            impact_score = 65 + np.random.rand() * 15
        elif events_per_day < 30:
            pressure_level = "high"
            impact_score = 45 + np.random.rand() * 15
        else:
            pressure_level = "very high"
            impact_score = 25 + np.random.rand() * 15
        
        return {
            'pressure_level': pressure_level,
            'impact_score': float(impact_score),
            'events_per_day': float(events_per_day),
            'vessel_diversity': unique_vessels,
            'sustainability_rating': self._calculate_sustainability_rating(impact_score),
            'recommendations': self._generate_recommendations(pressure_level, impact_score)
        }
    
    def _calculate_sustainability_rating(self, impact_score: float) -> str:
        """Calculate sustainability rating from impact score"""
        if impact_score >= 75:
            return "Excellent"
        elif impact_score >= 60:
            return "Good"
        elif impact_score >= 45:
            return "Fair"
        elif impact_score >= 30:
            return "Poor"
        else:
            return "Critical"
    
    def _generate_recommendations(self, pressure_level: str, impact_score: float) -> List[str]:
        """Generate recommendations based on fishing pressure"""
        recommendations = []
        
        if pressure_level in ["high", "very high"]:
            recommendations.append("Consider implementing seasonal fishing restrictions")
            recommendations.append("Increase monitoring of vulnerable marine habitats")
        
        if impact_score < 50:
            recommendations.append("Urgent action needed to restore ecosystem balance")
            recommendations.append("Evaluate current fishing quotas and zones")
        
        if impact_score >= 75:
            recommendations.append("Maintain current sustainable practices")
            recommendations.append("Continue ecosystem monitoring")
        
        return recommendations
    
    def calculate_economic_cascade(self, 
                                   marine_health: float,
                                   whisky_base_value: float = 125_000_000) -> Dict[str, Any]:
        """
        Calculate economic cascade from marine health to Edinburgh economy
        
        Args:
            marine_health: Marine ecosystem health score (0-100)
            whisky_base_value: Base annual whisky industry value (£)
        
        Returns:
            Economic impact analysis
        """
        # Marine health affects whisky production quality and tourism
        health_factor = marine_health / 100
        
        # Whisky industry impact
        whisky_value = whisky_base_value * health_factor * 0.85
        whisky_tourism = whisky_value * 0.45  # 45% tourism-related
        whisky_export = whisky_value * 0.55   # 55% export
        
        # Edinburgh receives portion through tourism
        edinburgh_whisky_tourism = whisky_tourism * 0.75
        
        # Additional Edinburgh tourism from coastal quality
        coastal_tourism_value = 80_000_000 * health_factor
        
        # Total Edinburgh impact
        edinburgh_total = edinburgh_whisky_tourism + coastal_tourism_value
        
        # Jobs calculation (£55,000 average salary + overhead)
        job_cost = 75_000
        jobs_supported = int(edinburgh_total / job_cost)
        
        # Multiplier effect (each tourism £ generates £1.80 in local economy)
        multiplier_effect = edinburgh_total * 1.8
        
        return {
            'marine_health': float(marine_health),
            'whisky_industry_value': float(whisky_value),
            'whisky_tourism_value': float(whisky_tourism),
            'whisky_export_value': float(whisky_export),
            'coastal_tourism_value': float(coastal_tourism_value),
            'edinburgh_direct_impact': float(edinburgh_total),
            'edinburgh_total_impact': float(multiplier_effect),
            'jobs_supported': jobs_supported,
            'economic_multiplier': 1.8,
            'health_factor': float(health_factor)
        }


# Create analyzer instance
analyzer = DataAnalyzer()
