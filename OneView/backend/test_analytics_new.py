#!/usr/bin/env python3
"""
Google Analytics API Test Script - Updated Version
Test your Google Analytics connection with proper service account credentials
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.google_analytics_real import GoogleAnalyticsDataFetcher

def test_analytics_connection():
    """Test Google Analytics API connection with proper service account"""
    print("=" * 60)
    print("GOOGLE ANALYTICS API CONNECTION TEST")
    print("=" * 60)
    
    # Check if credentials file exists
    credentials_path = os.path.join(os.path.dirname(__file__), 'service-account-key.json')
    property_id = "478395445"
    
    print(f"🔍 Looking for credentials at: {credentials_path}")
    print(f"🏢 Testing property ID: {property_id}")
    print()
    
    if not os.path.exists(credentials_path):
        print("❌ SERVICE ACCOUNT KEY FILE NOT FOUND!")
        print()
        print("To fix this issue:")
        print("1. 📋 Create a service account in Google Cloud Console")
        print("2. 📥 Download the JSON key file")
        print("3. 📝 Rename it to 'service-account-key.json'")
        print("4. 📂 Place it in the backend/ directory")
        print("5. 👥 Add the service account email to your Google Analytics property")
        print()
        print("📖 See ANALYTICS_SETUP_GUIDE.md for detailed instructions")
        return False
    
    print("✅ Service account key file found")
    
    try:
        # Initialize the fetcher with explicit credentials path
        print("🔄 Initializing Google Analytics client...")
        analytics = GoogleAnalyticsDataFetcher(
            property_id=property_id,
            credentials_path=credentials_path
        )
        
        if analytics.client is None:
            print("❌ Failed to initialize Google Analytics client")
            print("   Check your credentials and property access")
            return False
        
        print("✅ Google Analytics client initialized successfully")
        
        # Try to fetch data
        print("📊 Fetching analytics data (last 7 days)...")
        data = analytics.fetch_analytics_data(days=7)
        
        print()
        print("📈 ANALYTICS DATA RESULTS:")
        print("-" * 40)
        
        # Display key metrics
        key_metrics = [
            'total_sessions', 'total_users', 'total_page_views', 
            'total_revenue', 'avg_bounce_rate', 'avg_session_duration'
        ]
        
        for metric in key_metrics:
            if metric in data:
                value = data[metric]
                if isinstance(value, (int, float)):
                    if metric == 'total_revenue':
                        print(f"💰 {metric}: ${value:,.2f}")
                    elif metric == 'avg_bounce_rate':
                        print(f"⏭️  {metric}: {value:.1f}%")
                    elif metric == 'avg_session_duration':
                        print(f"⏱️  {metric}: {value:.1f} seconds")
                    else:
                        print(f"📊 {metric}: {value:,}")
                else:
                    print(f"📋 {metric}: {value}")
        
        print("-" * 40)
        print("✅ ANALYTICS TEST COMPLETED SUCCESSFULLY!")
        print("   You can now use real Analytics data in your dashboard")
        return True
                
    except Exception as e:
        print(f"❌ ERROR TESTING ANALYTICS: {e}")
        print()
        print("🔧 TROUBLESHOOTING TIPS:")
        print("1. Ensure the service account has 'Viewer' access to the Analytics property")
        print("2. Verify the property ID (478395445) is correct for your GA4 property")
        print("3. Check that the Google Analytics Data API is enabled in Google Cloud")
        print("4. Make sure the JSON file contains valid service account credentials")
        return False

def main():
    """Main test function"""
    success = test_analytics_connection()
    
    if success:
        print("\n🎉 Ready to integrate with your KPI dashboard!")
    else:
        print("\n🔧 Please fix the issues above and try again")
        print("📖 See ANALYTICS_SETUP_GUIDE.md for help")

if __name__ == "__main__":
    main()