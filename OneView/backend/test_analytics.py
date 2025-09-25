#!/usr/bin/env python3
"""
Google Analytics API Test Script
Test your Google Analytics connection before integrating with the dashboard
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.google_analytics_real import GoogleAnalyticsDataFetcher

def test_google_analytics_connection():
    """Test Google Analytics API connection"""
    print("=" * 60)
    print("GOOGLE ANALYTICS API CONNECTION TEST")
    print("=" * 60)
    
    # Configuration
    property_id = "478395445"  # Your GA4 Property ID
    credentials_path = "google-ads.yaml"  # Path to your service account credentials
    
    print(f"Property ID: {property_id}")
    print(f"Credentials Path: {credentials_path}")
    print()
    
    if property_id == "YOUR_GA4_PROPERTY_ID":
        print("❌ ERROR: Please update the property_id in this script with your actual GA4 Property ID")
        print("\nTo get your GA4 Property ID:")
        print("1. Go to https://analytics.google.com/")
        print("2. Select your property")
        print("3. Go to Admin (gear icon)")
        print("4. Under Property column, click 'Property Settings'")
        print("5. Copy the Property ID (numeric value)")
        return False
    
    if not os.path.exists(credentials_path):
        print(f"❌ ERROR: Credentials file not found: {credentials_path}")
        print("\nMake sure you have:")
        print("1. Created a service account in Google Cloud Console")
        print("2. Downloaded the JSON key file")
        print("3. Placed it in the backend directory")
        return False
    
    try:
        # Initialize the fetcher
        print("🔄 Initializing Google Analytics client...")
        fetcher = GoogleAnalyticsDataFetcher(property_id=property_id, credentials_path=credentials_path)
        
        if not fetcher.client:
            print("❌ Failed to initialize Google Analytics client")
            return False
        
        print("✅ Google Analytics client initialized successfully")
        print()
        
        # Test API call
        print("🔄 Testing API call...")
        data = fetcher.fetch_analytics_data(days=7)  # Last 7 days
        
        if data.get('data_source') == 'google_analytics_api':
            print("✅ SUCCESS: Real Google Analytics data retrieved!")
            print()
            print("📊 Data Summary:")
            print(f"   Sessions: {data.get('total_sessions', 0):,}")
            print(f"   Users: {data.get('total_users', 0):,}")
            print(f"   Page Views: {data.get('page_views', 0):,}")
            print(f"   Revenue: ${data.get('revenue', 0):.2f}")
            print(f"   Bounce Rate: {data.get('bounce_rate', 0):.1f}%")
            print(f"   Conversion Rate: {data.get('conversion_rate', 0):.2f}%")
            print(f"   Historical Data Points: {len(data.get('historical_data', []))}")
            
            return True
        else:
            print("⚠️  API call completed but returned mock data")
            print("   This might indicate permissions or configuration issues")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nCommon issues:")
        print("1. Property ID is incorrect")
        print("2. Service account doesn't have access to the property")
        print("3. Google Analytics Data API is not enabled")
        print("4. Credentials file is invalid")
        return False

if __name__ == "__main__":
    success = test_google_analytics_connection()
    
    print()
    print("=" * 60)
    if success:
        print("✅ GOOGLE ANALYTICS API TEST PASSED")
        print("Your dashboard will now show real Analytics data!")
    else:
        print("❌ GOOGLE ANALYTICS API TEST FAILED")
        print("Please fix the issues above and try again.")
    print("=" * 60)