#!/usr/bin/env python3
"""
Test script to verify the complete API flow
"""

import requests
import json

# Test configuration
BASE_URL = "http://127.0.0.1:5000/api"
TEST_USER = {
    "email": "admin@company.com",
    "password": "admin123"
}

def test_login_and_data():
    """Test login and data retrieval"""
    print("=" * 60)
    print("TESTING COMPLETE API FLOW")
    print("=" * 60)
    
    # Step 1: Login
    print("🔐 Step 1: Testing login...")
    try:
        login_response = requests.post(
            f"{BASE_URL}/login",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            access_token = login_data.get("access_token")
            user_data = login_data.get("user")
            
            print(f"✅ Login successful!")
            print(f"   User: {user_data.get('email')} ({user_data.get('role')})")
            print(f"   Token: {access_token[:20]}...")
            
            # Step 2: Get KPI Data
            print("\n📊 Step 2: Testing KPI data retrieval...")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            kpi_response = requests.get(f"{BASE_URL}/kpi-data", headers=headers)
            
            if kpi_response.status_code == 200:
                kpi_data = kpi_response.json()
                print("✅ KPI data retrieved successfully!")
                
                # Show the raw response for debugging
                print(f"\n🔍 RAW API RESPONSE:")
                print(json.dumps(kpi_data, indent=2))
                
                # Show key metrics
                print("\n📈 KEY METRICS:")
                print("-" * 40)
                
                # Google Ads data
                if 'google_ads' in kpi_data:
                    ads_data = kpi_data['google_ads']
                    print(f"💰 Google Ads Spend: ${ads_data.get('total_spend', 0):,.2f}")
                    print(f"👆 Total Clicks: {ads_data.get('total_clicks', 0):,}")
                    print(f"🎯 Total Conversions: {ads_data.get('total_conversions', 0):,}")
                else:
                    print("❌ No 'google_ads' data in response")
                
                # Google Analytics data
                if 'google_analytics' in kpi_data:
                    analytics_data = kpi_data['google_analytics']
                    print(f"👥 Total Sessions: {analytics_data.get('total_sessions', 0):,}")
                    print(f"👤 Total Users: {analytics_data.get('total_users', 0):,}")
                    print(f"💸 Total Revenue: ${analytics_data.get('total_revenue', 0):,.2f}")
                else:
                    print("❌ No 'google_analytics' data in response")
                
                # Data source info
                print(f"\n🔍 Data Sources:")
                if 'google_ads' in kpi_data:
                    ads_source = kpi_data['google_ads'].get('data_source', 'unknown')
                    print(f"   Google Ads: {ads_source}")
                if 'google_analytics' in kpi_data:
                    analytics_source = kpi_data['google_analytics'].get('data_source', 'unknown')
                    print(f"   Google Analytics: {analytics_source}")
                
                print("\n✅ COMPLETE API TEST SUCCESSFUL!")
                print("   The dashboard should now display this data")
                
            else:
                print(f"❌ KPI data request failed: {kpi_response.status_code}")
                print(f"   Response: {kpi_response.text}")
                
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    test_login_and_data()