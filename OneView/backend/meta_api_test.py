#!/usr/bin/env python3
"""
Meta Marketing API Test Script
Creates a new ad campaign to test Meta's Marketing API integration.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MetaMarketingAPITest:
    def __init__(self, api_version='v21.0'):
        self.access_token = os.getenv('META_ACCESS_TOKEN')
        self.ad_account_id = os.getenv('AD_ACCOUNT_ID')
        self.api_version = api_version
        self.base_url = f'https://graph.facebook.com/{api_version}'
        
        if not self.access_token:
            raise ValueError("META_ACCESS_TOKEN not found in environment variables")
        if not self.ad_account_id:
            raise ValueError("AD_ACCOUNT_ID not found in environment variables")
            
        print(f"✅ Initialized Meta API client")
        print(f"🌐 API Version: {self.api_version}")
        print(f"📱 Ad Account: {self.ad_account_id}")
        print(f"🔑 Token: {self.access_token[:20]}...")
    
    def test_connection(self):
        """Test basic API connection by fetching account info"""
        print("\n🔍 Testing API connection...")
        
        url = f"{self.base_url}/{self.ad_account_id}"
        params = {
            'access_token': self.access_token,
            'fields': 'id,name,account_status,currency,timezone_name'
        }
        
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Connection successful!")
                print(f"📊 Account Name: {data.get('name', 'N/A')}")
                print(f"💰 Currency: {data.get('currency', 'N/A')}")
                print(f"🌍 Timezone: {data.get('timezone_name', 'N/A')}")
                print(f"📈 Status: {data.get('account_status', 'N/A')}")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code}")
                print(f"📝 Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Connection error: {str(e)}")
            return False
    
    def create_campaign(self):
        """Create a new ad campaign for testing"""
        print("\n🚀 Creating test campaign...")
        
        # Campaign data
        campaign_data = {
            'name': f'My First API Campaign - {datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'objective': 'OUTCOME_TRAFFIC',
            'status': 'PAUSED',
            'special_ad_categories': '[]',
            'access_token': self.access_token
        }
        
        url = f"{self.base_url}/{self.ad_account_id}/campaigns"
        
        try:
            response = requests.post(url, data=campaign_data)
            
            print(f"📤 Request URL: {url}")
            print(f"📋 Campaign Data: {json.dumps({k: v for k, v in campaign_data.items() if k != 'access_token'}, indent=2)}")
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                campaign_id = result.get('id')
                print("✅ Campaign created successfully!")
                print(f"🆔 Campaign ID: {campaign_id}")
                print(f"📝 Full Response: {json.dumps(result, indent=2)}")
                return campaign_id
            else:
                print("❌ Campaign creation failed!")
                print(f"📝 Error Response: {response.text}")
                
                # Try to parse error details
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        error = error_data['error']
                        print(f"🚨 Error Code: {error.get('code')}")
                        print(f"🚨 Error Type: {error.get('type')}")
                        print(f"🚨 Error Message: {error.get('message')}")
                        
                        if 'error_subcode' in error:
                            print(f"🚨 Error Subcode: {error.get('error_subcode')}")
                except:
                    pass
                    
                return None
                
        except Exception as e:
            print(f"❌ Request error: {str(e)}")
            return None
    
    def get_campaigns(self, limit=5):
        """Fetch existing campaigns to verify creation"""
        print(f"\n📋 Fetching last {limit} campaigns...")
        
        url = f"{self.base_url}/{self.ad_account_id}/campaigns"
        params = {
            'access_token': self.access_token,
            'fields': 'id,name,objective,status,created_time,updated_time',
            'limit': limit
        }
        
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                campaigns = data.get('data', [])
                
                print(f"✅ Found {len(campaigns)} campaigns:")
                for i, campaign in enumerate(campaigns, 1):
                    print(f"\n{i}. 📊 {campaign.get('name', 'Unnamed Campaign')}")
                    print(f"   🆔 ID: {campaign.get('id')}")
                    print(f"   🎯 Objective: {campaign.get('objective', 'N/A')}")
                    print(f"   📈 Status: {campaign.get('status', 'N/A')}")
                    print(f"   📅 Created: {campaign.get('created_time', 'N/A')}")
                
                return campaigns
            else:
                print(f"❌ Failed to fetch campaigns: {response.status_code}")
                print(f"📝 Response: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching campaigns: {str(e)}")
            return []
    
    def run_full_test(self):
        """Run complete API test suite"""
        print("🚀 Meta Marketing API Test Suite")
        print("=" * 50)
        
        # Test 1: Connection
        if not self.test_connection():
            print("\n❌ Connection test failed. Stopping here.")
            print("\n🔧 TROUBLESHOOTING GUIDE:")
            print("1. 🔑 Check if your access token has the required permissions:")
            print("   - ads_management (for creating campaigns)")
            print("   - ads_read (for reading campaign data)")
            print("2. 🌐 Visit the Graph API Explorer: https://developers.facebook.com/tools/explorer/")
            print("3. 📋 Generate a new token with proper permissions")
            print("4. 🏢 Make sure you're the owner/admin of the ad account")
            print("5. ⚙️  Check your app's permissions in Facebook App Dashboard")
            return False
        
        # Test 2: List existing campaigns
        existing_campaigns = self.get_campaigns()
        
        # Test 3: Create new campaign
        campaign_id = self.create_campaign()
        
        if campaign_id:
            print(f"\n✅ All tests completed successfully!")
            print(f"🎉 New campaign created with ID: {campaign_id}")
            
            # Test 4: Verify creation by listing campaigns again
            print("\n🔄 Verifying campaign creation...")
            self.get_campaigns()
            
            return True
        else:
            print(f"\n❌ Campaign creation failed. Check the error messages above.")
            return False

def main():
    """Main execution function"""
    try:
        # Try different API versions if needed
        api_versions = ['v23.0', 'v21.0', 'v20.0', 'v19.0', 'v18.0']
        success = False
        
        for version in api_versions:
            print(f"\n🔄 Trying API version {version}...")
            try:
                # Create test instance
                api_test = MetaMarketingAPITest(api_version=version)
                
                # Test connection first
                if api_test.test_connection():
                    print(f"✅ API version {version} works! Proceeding with full test...")
                    # Run full test suite
                    success = api_test.run_full_test()
                    break
                else:
                    print(f"❌ API version {version} failed, trying next version...")
                    continue
                    
            except Exception as e:
                print(f"❌ Error with version {version}: {str(e)}")
                continue
        
        if success:
            print("\n🎊 Meta Marketing API test completed successfully!")
        else:
            print("\n💥 Meta Marketing API test encountered errors.")
            print("� Try checking your permissions and access token.")
            
    except Exception as e:
        print(f"\n💥 Critical error: {str(e)}")
        print("Please check your environment variables and try again.")

if __name__ == "__main__":
    main()