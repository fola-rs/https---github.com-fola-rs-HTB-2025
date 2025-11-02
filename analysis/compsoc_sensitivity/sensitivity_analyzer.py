"""
CompSoc Challenge: Modelling Mayhem
===================================

Demonstrating how small changes in assumptions drastically affect predictions.

SUCCESS CRITERIA:
- Minimal assumption change → Maximum result variance
- Clear documentation of each assumption
- Side-by-side comparison of outcomes
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class SensitivityAnalyzer:
    """
    Analyze how small modelling assumptions create large output differences
    """
    
    def __init__(self):
        self.results = {}
        
    def assumption_1_turtle_nesting_success(
        self, 
        base_rate: float = 0.65,
        variations: List[float] = [0.05, 0.10, 0.15]
    ) -> pd.DataFrame:
        """
        ASSUMPTION 1: Sea Turtle Nesting Success Rate
        
        Base assumption: 65% nesting success rate
        Small changes: ±5%, ±10%, ±15%
        
        Impact chain:
        Nesting success → Turtle population → Seaweed grazing → 
        Seaweed health → Harvest volume → Whisky production stability
        """
        
        results = []
        
        for variation in variations:
            # Positive variation
            adjusted_rate_high = base_rate * (1 + variation)
            impact_high = self._calculate_cascade_impact(adjusted_rate_high)
            results.append({
                'assumption': f'+{variation*100:.0f}% nesting success',
                'nesting_rate': adjusted_rate_high,
                'turtle_population_change_%': variation * 100,
                'seaweed_harvest_change_%': impact_high['seaweed_change'],
                'whisky_production_impact_%': impact_high['whisky_impact'],
                'edinburgh_economic_impact_£M': impact_high['economic_impact']
            })
            
            # Negative variation
            adjusted_rate_low = base_rate * (1 - variation)
            impact_low = self._calculate_cascade_impact(adjusted_rate_low)
            results.append({
                'assumption': f'-{variation*100:.0f}% nesting success',
                'nesting_rate': adjusted_rate_low,
                'turtle_population_change_%': -variation * 100,
                'seaweed_harvest_change_%': impact_low['seaweed_change'],
                'whisky_production_impact_%': impact_low['whisky_impact'],
                'edinburgh_economic_impact_£M': impact_low['economic_impact']
            })
        
        # Add baseline
        baseline_impact = self._calculate_cascade_impact(base_rate)
        results.insert(0, {
            'assumption': 'Baseline (65%)',
            'nesting_rate': base_rate,
            'turtle_population_change_%': 0,
            'seaweed_harvest_change_%': baseline_impact['seaweed_change'],
            'whisky_production_impact_%': baseline_impact['whisky_impact'],
            'edinburgh_economic_impact_£M': baseline_impact['economic_impact']
        })
        
        df = pd.DataFrame(results)
        self.results['nesting_success'] = df
        return df
    
    def assumption_2_temperature_threshold(
        self,
        thresholds: List[float] = [0.5, 1.0, 2.0]
    ) -> pd.DataFrame:
        """
        ASSUMPTION 2: Temperature Anomaly Threshold
        
        What constitutes a "significant" temperature change?
        Small threshold changes create different alert frequencies
        
        Impact: 0.5°C vs 1.0°C vs 2.0°C threshold for warehouse cooling alerts
        """
        
        results = []
        
        # Simulate monthly temperature data
        np.random.seed(42)
        monthly_temps = 15 + 3 * np.sin(np.linspace(0, 2*np.pi, 12)) + np.random.normal(0, 0.8, 12)
        
        for threshold in thresholds:
            alerts_triggered = np.sum(np.abs(monthly_temps - 15) > threshold)
            cooling_cost = alerts_triggered * 5000  # £5k per alert response
            
            results.append({
                'assumption': f'Threshold: {threshold}°C',
                'threshold_celsius': threshold,
                'alerts_per_year': alerts_triggered,
                'cooling_cost_£': cooling_cost,
                'whisky_quality_risk': 'High' if alerts_triggered > 6 else 'Medium' if alerts_triggered > 3 else 'Low'
            })
        
        df = pd.DataFrame(results)
        self.results['temperature_threshold'] = df
        return df
    
    def assumption_3_seaweed_regrowth_coefficient(
        self,
        base_coefficient: float = 0.12,
        variations: List[float] = [0.02, 0.04, 0.06]
    ) -> pd.DataFrame:
        """
        ASSUMPTION 3: Seaweed Biological Growth Rate
        
        Base assumption: 12% monthly regrowth rate
        Small changes: ±2%, ±4%, ±6% absolute
        
        Impact: Sustainable harvest volumes and ecosystem stability
        """
        
        results = []
        initial_biomass = 1000  # kg
        months = 12
        
        for var in variations:
            # Higher growth rate
            rate_high = base_coefficient + var
            biomass_high = initial_biomass * (1 + rate_high) ** months
            
            results.append({
                'assumption': f'+{var*100:.0f}% growth rate',
                'monthly_growth_rate': rate_high,
                'annual_biomass_kg': biomass_high,
                'sustainable_harvest_%': min(rate_high * 100 * 0.8, 80),  # 80% of growth
                'ecosystem_status': 'Thriving' if rate_high > 0.14 else 'Stable'
            })
            
            # Lower growth rate
            rate_low = base_coefficient - var
            biomass_low = initial_biomass * (1 + rate_low) ** months
            
            results.append({
                'assumption': f'-{var*100:.0f}% growth rate',
                'monthly_growth_rate': rate_low,
                'annual_biomass_kg': biomass_low,
                'sustainable_harvest_%': min(rate_low * 100 * 0.8, 80),
                'ecosystem_status': 'At Risk' if rate_low < 0.10 else 'Stable'
            })
        
        # Baseline
        biomass_base = initial_biomass * (1 + base_coefficient) ** months
        results.insert(0, {
            'assumption': 'Baseline (12%)',
            'monthly_growth_rate': base_coefficient,
            'annual_biomass_kg': biomass_base,
            'sustainable_harvest_%': base_coefficient * 100 * 0.8,
            'ecosystem_status': 'Stable'
        })
        
        df = pd.DataFrame(results)
        self.results['seaweed_growth'] = df
        return df
    
    def assumption_4_whisky_aging_sensitivity(
        self,
        base_sensitivity: float = 0.03,
        variations: List[float] = [0.01, 0.02, 0.03]
    ) -> pd.DataFrame:
        """
        ASSUMPTION 4: Whisky Aging Temperature Sensitivity
        
        How much does 1°C ambient temperature change affect aging rate?
        Base: 3% change per °C
        Variations: ±1%, ±2%, ±3% absolute
        
        Impact: Maturation time, quality, and inventory management
        """
        
        results = []
        target_temp = 15  # °C optimal
        actual_temps = [14, 15, 16, 17]  # Range of warehouse temps
        
        for var in variations:
            # Higher sensitivity
            sens_high = base_sensitivity + var
            
            aging_impacts_high = []
            for temp in actual_temps:
                deviation = temp - target_temp
                aging_rate_change = deviation * sens_high * 100
                aging_impacts_high.append(aging_rate_change)
            
            results.append({
                'assumption': f'+{var*100:.1f}% sensitivity',
                'sensitivity_per_celsius': sens_high,
                'avg_aging_impact_%': np.mean(np.abs(aging_impacts_high)),
                'quality_variance': 'High' if sens_high > 0.04 else 'Medium',
                'inventory_risk_£M': sens_high * 100 * 0.5  # Rough estimate
            })
            
            # Lower sensitivity
            sens_low = base_sensitivity - var
            
            aging_impacts_low = []
            for temp in actual_temps:
                deviation = temp - target_temp
                aging_rate_change = deviation * sens_low * 100
                aging_impacts_low.append(aging_rate_change)
            
            results.append({
                'assumption': f'-{var*100:.1f}% sensitivity',
                'sensitivity_per_celsius': sens_low,
                'avg_aging_impact_%': np.mean(np.abs(aging_impacts_low)),
                'quality_variance': 'Low' if sens_low < 0.02 else 'Medium',
                'inventory_risk_£M': sens_low * 100 * 0.5
            })
        
        # Baseline
        aging_impacts_base = [abs((temp - target_temp) * base_sensitivity * 100) for temp in actual_temps]
        results.insert(0, {
            'assumption': 'Baseline (3%)',
            'sensitivity_per_celsius': base_sensitivity,
            'avg_aging_impact_%': np.mean(aging_impacts_base),
            'quality_variance': 'Medium',
            'inventory_risk_£M': base_sensitivity * 100 * 0.5
        })
        
        df = pd.DataFrame(results)
        self.results['aging_sensitivity'] = df
        return df
    
    def _calculate_cascade_impact(self, nesting_rate: float) -> Dict[str, float]:
        """
        Calculate cascade effects through the system
        
        Causal chain:
        Nesting rate → Population → Grazing → Seaweed → Coastal temp proxy → Whisky storage
        """
        
        # Simplified causal model (replace with actual fitted model)
        baseline_nesting = 0.65
        rate_change = (nesting_rate - baseline_nesting) / baseline_nesting
        
        # Cascade multipliers (based on domain knowledge / fitted parameters)
        seaweed_elasticity = 0.8  # 1% turtle change → 0.8% seaweed change
        whisky_elasticity = 0.3   # 1% seaweed change → 0.3% whisky impact
        economic_multiplier = 62  # £62M per 1% whisky production change (£6.2B base)
        
        seaweed_change = rate_change * 100 * seaweed_elasticity
        whisky_impact = seaweed_change * whisky_elasticity
        economic_impact = whisky_impact * economic_multiplier / 100
        
        return {
            'seaweed_change': seaweed_change,
            'whisky_impact': whisky_impact,
            'economic_impact': economic_impact
        }
    
    def generate_comparison_report(self) -> str:
        """
        Generate CompSoc challenge report showing side-by-side comparisons
        """
        
        report = """
        ╔════════════════════════════════════════════════════════════════════╗
        ║          COMPSOC CHALLENGE: MODELLING MAYHEM ANALYSIS              ║
        ║   Demonstrating How Small Assumptions Create Large Differences    ║
        ╚════════════════════════════════════════════════════════════════════╝
        
        PROJECT: Tides & Tomes - Sea Turtle → Whisky Production Model
        
        """
        
        for name, df in self.results.items():
            report += f"\n{'='*70}\n"
            report += f"ASSUMPTION: {name.replace('_', ' ').title()}\n"
            report += f"{'='*70}\n\n"
            report += df.to_string(index=False)
            report += "\n\n"
            
            # Calculate variance
            if len(df) > 1:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    first_numeric = numeric_cols[0]
                    variance = df[first_numeric].std() / df[first_numeric].mean() * 100
                    report += f"📊 Coefficient of Variation: {variance:.1f}%\n"
                    report += f"🎯 Result Spread: {df[first_numeric].max() - df[first_numeric].min():.2f}\n\n"
        
        return report
    
    def plot_sensitivity_comparison(self, save_path: str = None):
        """
        Create visual comparison of assumption impacts
        """
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('CompSoc Challenge: Small Assumptions, Big Differences', 
                     fontsize=16, fontweight='bold')
        
        # Plot 1: Nesting Success Impact
        if 'nesting_success' in self.results:
            df = self.results['nesting_success']
            ax = axes[0, 0]
            ax.bar(df['assumption'], df['edinburgh_economic_impact_£M'], 
                   color=['red' if x < 0 else 'green' if x > 0 else 'gray' 
                          for x in df['turtle_population_change_%']])
            ax.set_title('Assumption 1: Nesting Success Rate\n(Small Biological Change → Large Economic Impact)')
            ax.set_ylabel('Edinburgh Economic Impact (£M)')
            ax.tick_params(axis='x', rotation=45)
            ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
            ax.grid(axis='y', alpha=0.3)
        
        # Plot 2: Temperature Threshold
        if 'temperature_threshold' in self.results:
            df = self.results['temperature_threshold']
            ax = axes[0, 1]
            ax.plot(df['threshold_celsius'], df['alerts_per_year'], 
                   marker='o', linewidth=3, markersize=10, color='orange')
            ax.set_title('Assumption 2: Temperature Alert Threshold\n(0.5°C vs 2.0°C Definition Changes Everything)')
            ax.set_xlabel('Threshold (°C)')
            ax.set_ylabel('Alerts Triggered per Year')
            ax.grid(True, alpha=0.3)
        
        # Plot 3: Seaweed Growth
        if 'seaweed_growth' in self.results:
            df = self.results['seaweed_growth']
            ax = axes[1, 0]
            ax.bar(df['assumption'], df['annual_biomass_kg'], color='teal', alpha=0.7)
            ax.set_title('Assumption 3: Seaweed Regrowth Coefficient\n(±2% Growth Rate → Drastically Different Harvests)')
            ax.set_ylabel('Annual Biomass (kg)')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(axis='y', alpha=0.3)
        
        # Plot 4: Whisky Aging Sensitivity
        if 'aging_sensitivity' in self.results:
            df = self.results['aging_sensitivity']
            ax = axes[1, 1]
            ax.scatter(df['sensitivity_per_celsius'], df['inventory_risk_£M'], 
                      s=200, alpha=0.6, c=range(len(df)), cmap='RdYlGn_r')
            ax.set_title('Assumption 4: Whisky Aging Temperature Sensitivity\n(Small Parameter Change → High Financial Risk)')
            ax.set_xlabel('Sensitivity per °C')
            ax.set_ylabel('Inventory Risk (£M)')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Saved sensitivity comparison to {save_path}")
        
        return fig


# Example usage for CompSoc challenge submission
if __name__ == "__main__":
    print("🎯 CompSoc Challenge: Modelling Mayhem")
    print("=" * 70)
    
    analyzer = SensitivityAnalyzer()
    
    # Run all assumption analyses
    print("\n📊 Analyzing Assumption 1: Turtle Nesting Success...")
    df1 = analyzer.assumption_1_turtle_nesting_success()
    print(df1)
    
    print("\n📊 Analyzing Assumption 2: Temperature Threshold...")
    df2 = analyzer.assumption_2_temperature_threshold()
    print(df2)
    
    print("\n📊 Analyzing Assumption 3: Seaweed Growth Rate...")
    df3 = analyzer.assumption_3_seaweed_regrowth_coefficient()
    print(df3)
    
    print("\n📊 Analyzing Assumption 4: Whisky Aging Sensitivity...")
    df4 = analyzer.assumption_4_whisky_aging_sensitivity()
    print(df4)
    
    # Generate report
    report = analyzer.generate_comparison_report()
    print("\n" + report)
    
    # Create visualization
    analyzer.plot_sensitivity_comparison('compsoc_sensitivity_analysis.png')
