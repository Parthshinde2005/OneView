#!/usr/bin/env python3
"""
Enhanced data fetcher that combines real API data with demo historical data
"""

from datetime import datetime, timedelta
import random

def enhance_historical_data(api_data, data_source_name=""):
    """
    Enhance API data with demo historical data and campaign data if empty
    This allows the charts and tables to display data even when real APIs return zero values
    """
    if not api_data or not isinstance(api_data, dict):
        return api_data
    
    # Check if historical_data is empty or missing
    if not api_data.get('historical_data') or len(api_data.get('historical_data', [])) == 0:
        print(f"[DATA-ENHANCER] {data_source_name} has no historical data, adding demo data for charts")
        
        # Generate demo historical data for the last 30 days
        demo_historical = []
        base_spend = 50 if data_source_name == "Google Ads" else 0
        base_clicks = 25 if data_source_name == "Google Ads" else 0
        
        for i in range(30, 0, -1):  # Last 30 days in chronological order
            date = datetime.now() - timedelta(days=i)
            
            # Create realistic demo data
            demo_historical.append({
                "date": date.strftime("%Y-%m-%d"),
                "spend": round(base_spend + random.uniform(-20, 40), 2),
                "clicks": base_clicks + random.randint(-10, 20),
                "impressions": random.randint(100, 500),
                "conversions": random.randint(0, 5)
            })
        
        # Add demo data to the API response
        api_data['historical_data'] = demo_historical
        api_data['data_source'] = f"{api_data.get('data_source', 'unknown')}_with_demo_charts"
        
        print(f"[DATA-ENHANCER] Added {len(demo_historical)} demo data points for {data_source_name}")
    
    # Check if campaigns data is empty for Google Ads (for demo purposes)
    if data_source_name == "Google Ads" and (not api_data.get('campaigns') or len(api_data.get('campaigns', [])) == 0):
        print(f"[DATA-ENHANCER] {data_source_name} has no campaigns, adding demo campaigns for table display")
        
        # Generate demo campaign data
        demo_campaigns = [
            {
                "name": "Brand Awareness Campaign",
                "spend": round(random.uniform(1500, 3000), 2),
                "clicks": random.randint(200, 500),
                "impressions": random.randint(8000, 15000),
                "conversions": random.randint(15, 40),
                "ctr": round(random.uniform(2.5, 6.0), 2),
                "status": "ENABLED"
            },
            {
                "name": "Product Launch Campaign",
                "spend": round(random.uniform(800, 2000), 2),
                "clicks": random.randint(150, 350),
                "impressions": random.randint(5000, 12000),
                "conversions": random.randint(10, 25),
                "ctr": round(random.uniform(1.8, 4.5), 2),
                "status": "ENABLED"
            },
            {
                "name": "Retargeting Campaign",
                "spend": round(random.uniform(400, 1200), 2),
                "clicks": random.randint(80, 200),
                "impressions": random.randint(2000, 6000),
                "conversions": random.randint(5, 15),
                "ctr": round(random.uniform(3.0, 7.5), 2),
                "status": "PAUSED"
            }
        ]
        
        # Add demo campaigns to the API response
        api_data['campaigns'] = demo_campaigns
        api_data['data_source'] = f"{api_data.get('data_source', 'unknown')}_with_demo_campaigns"
        
        print(f"[DATA-ENHANCER] Added {len(demo_campaigns)} demo campaigns for {data_source_name}")
    
    return api_data