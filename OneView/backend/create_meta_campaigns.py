#!/usr/bin/env python3
"""
Script to manually create Meta ad campaigns using the Marketing API
Run this from terminal to add campaigns to your Meta Ads account
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MetaCampaignCreator:
    def __init__(self):
        self.access_token = os.getenv('META_ACCESS_TOKEN')
        self.ad_account_id = os.getenv('AD_ACCOUNT_ID')
        self.base_url = 'https://graph.facebook.com/v23.0'
        
        if not self.access_token:
            raise ValueError("META_ACCESS_TOKEN not found in environment variables")
        if not self.ad_account_id:
            raise ValueError("AD_ACCOUNT_ID not found in environment variables")
            
        print(f"[META] Initialized with account ID: {self.ad_account_id}")
    
    def test_connection(self):
        """Test API connection and get account info"""
        try:
            print("[META] Testing API connection...")
            url = f"{self.base_url}/{self.ad_account_id}"
            params = {
                'access_token': self.access_token,
                'fields': 'id,name,account_status,currency,timezone_name,business'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                account_info = response.json()
                print(f"[META] ✅ Connected to account: {account_info.get('name', 'Unknown')}")
                print(f"[META] Account Status: {account_info.get('account_status', 'Unknown')}")
                print(f"[META] Currency: {account_info.get('currency', 'Unknown')}")
                return True
            else:
                print(f"[META] ❌ Connection failed: {response.status_code}")
                print(f"[META] Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"[META] ❌ Connection error: {str(e)}")
            return False
    
    def list_existing_campaigns(self):
        """List existing campaigns"""
        try:
            print("[META] Listing existing campaigns...")
            url = f"{self.base_url}/{self.ad_account_id}/campaigns"
            params = {
                'access_token': self.access_token,
                'fields': 'id,name,status,objective,created_time,updated_time',
                'limit': 50
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                campaigns = response.json().get('data', [])
                print(f"[META] Found {len(campaigns)} existing campaigns:")
                for i, campaign in enumerate(campaigns, 1):
                    print(f"  {i}. {campaign.get('name', 'Unknown')} (Status: {campaign.get('status', 'Unknown')})")
                return campaigns
            else:
                print(f"[META] Failed to list campaigns: {response.status_code}")
                print(f"[META] Response: {response.text}")
                return []
                
        except Exception as e:
            print(f"[META] Error listing campaigns: {str(e)}")
            return []
    
    def create_campaign(self, name, objective='LINK_CLICKS', status='PAUSED'):
        """Create a new campaign"""
        try:
            print(f"[META] Creating campaign: {name}")
            url = f"{self.base_url}/{self.ad_account_id}/campaigns"
            
            data = {
                'access_token': self.access_token,
                'name': name,
                'objective': objective,
                'status': status,
                'special_ad_categories': '[]'  # Required for some objectives
            }
            
            response = requests.post(url, data=data)
            if response.status_code == 200:
                campaign_info = response.json()
                campaign_id = campaign_info.get('id')
                print(f"[META] ✅ Campaign created successfully!")
                print(f"[META] Campaign ID: {campaign_id}")
                print(f"[META] Campaign Name: {name}")
                return campaign_id
            else:
                print(f"[META] ❌ Failed to create campaign: {response.status_code}")
                print(f"[META] Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"[META] ❌ Error creating campaign: {str(e)}")
            return None
    
    def create_multiple_campaigns(self):
        """Create multiple demo campaigns"""
        campaigns_to_create = [
            {
                'name': '🎯 Brand Awareness - Meta',
                'objective': 'OUTCOME_AWARENESS',
                'status': 'PAUSED'
            },
            {
                'name': '🚀 Product Launch - Meta',
                'objective': 'OUTCOME_SALES',
                'status': 'PAUSED'
            },
            {
                'name': '🔄 Retargeting Campaign - Meta',
                'objective': 'OUTCOME_SALES',
                'status': 'PAUSED'
            },
            {
                'name': '📱 Mobile App Install - Meta',
                'objective': 'OUTCOME_APP_PROMOTION',
                'status': 'PAUSED'
            },
            {
                'name': '🛒 E-commerce Sales - Meta',
                'objective': 'OUTCOME_SALES',
                'status': 'PAUSED'
            },
            {
                'name': '👥 Lead Generation - Meta',
                'objective': 'OUTCOME_LEADS',
                'status': 'PAUSED'
            },
            {
                'name': '🎥 Video Views Campaign - Meta',
                'objective': 'OUTCOME_ENGAGEMENT',
                'status': 'PAUSED'
            }
        ]
        
        created_campaigns = []
        
        print(f"[META] Creating {len(campaigns_to_create)} demo campaigns...")
        print("-" * 50)
        
        for campaign_info in campaigns_to_create:
            campaign_id = self.create_campaign(
                name=campaign_info['name'],
                objective=campaign_info['objective'],
                status=campaign_info['status']
            )
            
            if campaign_id:
                created_campaigns.append({
                    'id': campaign_id,
                    'name': campaign_info['name'],
                    'objective': campaign_info['objective'],
                    'status': campaign_info['status']
                })
            
            print("-" * 30)
        
        print(f"[META] ✅ Campaign creation completed!")
        print(f"[META] Successfully created {len(created_campaigns)} campaigns")
        
        return created_campaigns

def main():
    """Main function to run the campaign creator"""
    print("=" * 60)
    print("META MARKETING API - CAMPAIGN CREATOR")
    print("=" * 60)
    
    try:
        # Initialize the creator
        creator = MetaCampaignCreator()
        
        # Test connection
        if not creator.test_connection():
            print("[META] ❌ Cannot proceed - API connection failed")
            return
        
        print()
        
        # List existing campaigns
        existing_campaigns = creator.list_existing_campaigns()
        print()
        
        # Ask user what to do
        print("Options:")
        print("1. Create multiple demo campaigns")
        print("2. List existing campaigns only")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\n" + "=" * 50)
            print("CREATING DEMO CAMPAIGNS")
            print("=" * 50)
            
            # Confirm before creating
            confirm = input("This will create 7 demo campaigns. Continue? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                created = creator.create_multiple_campaigns()
                
                print("\n" + "=" * 50)
                print("CAMPAIGN CREATION SUMMARY")
                print("=" * 50)
                
                if created:
                    print(f"✅ Successfully created {len(created)} campaigns:")
                    for i, campaign in enumerate(created, 1):
                        print(f"  {i}. {campaign['name']} (ID: {campaign['id']})")
                    
                    print(f"\n🎉 All campaigns are created in PAUSED status for safety.")
                    print(f"📊 You can now see them in your Meta Ads dashboard!")
                    print(f"🔄 Refresh your KPI dashboard to see the new campaigns.")
                else:
                    print("❌ No campaigns were created successfully.")
            else:
                print("Operation cancelled.")
                
        elif choice == '2':
            print(f"\n📊 Found {len(existing_campaigns)} existing campaigns.")
            
        elif choice == '3':
            print("👋 Goodbye!")
            
        else:
            print("❌ Invalid choice.")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()