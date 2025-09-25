#!/usr/bin/env python3
"""
Test the KPI Dashboard API endpoints to verify they work correctly
"""

import requests
import json

def test_login():
    """Test the login endpoint"""
    print("🔐 Testing login endpoint...")
    
    url = "http://localhost:5000/api/login"
    data = {
        "email": "admin@company.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print("❌ Login failed")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None

def test_kpi_data(token):
    """Test the KPI data endpoint"""
    print("\n📊 Testing KPI data endpoint...")
    
    url = "http://localhost:5000/api/kpi-data"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ KPI data retrieved successfully!")
            print(f"User Role: {data.get('user_role')}")
            print(f"User Name: {data.get('user_name')}")
            print(f"Data Keys: {list(data.get('data', {}).keys())}")
            
            # Check if Meta ads data is included
            meta_data = data.get('data', {}).get('meta_ads')
            if meta_data:
                print("✅ Meta ads data found!")
                print(f"Meta campaigns: {len(meta_data.get('campaigns', []))}")
                print(f"Meta spend: ${meta_data.get('summary_metrics', {}).get('total_spend', 0)}")
            else:
                print("❌ Meta ads data missing")
                
        else:
            print(f"❌ KPI data failed: {response.text}")
            
    except Exception as e:
        print(f"❌ KPI data error: {str(e)}")

def main():
    print("🚀 Testing KPI Dashboard API")
    print("=" * 50)
    
    # Test login
    token = test_login()
    
    if token:
        print("✅ Login successful")
        # Test KPI data
        test_kpi_data(token)
    else:
        print("❌ Cannot test KPI data without valid token")

if __name__ == "__main__":
    main()