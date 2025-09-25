#!/usr/bin/env python3
"""
Meta Ad Accounts Access Checker
Lists all ad accounts the current user has access to.
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_accessible_ad_accounts():
    """Check what ad accounts the current user has access to"""
    access_token = os.getenv('META_ACCESS_TOKEN')
    
    if not access_token:
        print("❌ META_ACCESS_TOKEN not found in .env file")
        return
    
    print("🔍 Checking Accessible Ad Accounts...")
    print(f"🔑 Token: {access_token[:20]}...")
    print("-" * 60)
    
    # Get user's ad accounts
    url = "https://graph.facebook.com/v23.0/me/adaccounts"
    params = {
        'access_token': access_token,
        'fields': 'id,name,account_status,currency,timezone_name,business'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            ad_accounts = data.get('data', [])
            
            print(f"✅ Found {len(ad_accounts)} accessible ad account(s):")
            print()
            
            current_account_id = os.getenv('AD_ACCOUNT_ID', '')
            found_current = False
            
            for i, account in enumerate(ad_accounts, 1):
                account_id = account.get('id', 'Unknown')
                account_name = account.get('name', 'Unnamed Account')
                account_status = account.get('account_status', 'Unknown')
                currency = account.get('currency', 'Unknown')
                
                is_current = account_id == current_account_id
                if is_current:
                    found_current = True
                
                status_icon = "🟢" if account_status == "1" else "🔴"
                current_icon = "👈 CURRENT" if is_current else ""
                
                print(f"{i}. {status_icon} {account_name} {current_icon}")
                print(f"   🆔 ID: {account_id}")
                print(f"   📊 Status: {account_status}")
                print(f"   💰 Currency: {currency}")
                print()
            
            print("-" * 60)
            print(f"🎯 Current AD_ACCOUNT_ID in .env: {current_account_id}")
            
            if found_current:
                print("✅ Your current ad account ID is accessible!")
                print("🤔 The issue might be with account permissions or API app setup.")
            else:
                print("❌ Your current ad account ID is NOT in your accessible accounts!")
                print("💡 You need to use one of the account IDs listed above.")
                
                if ad_accounts:
                    print(f"\n🔧 Suggested fix: Update your .env file with:")
                    print(f'AD_ACCOUNT_ID="{ad_accounts[0].get("id")}"')
                    
        else:
            print(f"❌ Failed to get ad accounts: {response.status_code}")
            print(f"📝 Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Error checking ad accounts: {str(e)}")

def check_business_accounts():
    """Check user's business accounts"""
    access_token = os.getenv('META_ACCESS_TOKEN')
    
    print("\n🏢 Checking Business Accounts...")
    
    url = "https://graph.facebook.com/v23.0/me/businesses"
    params = {
        'access_token': access_token,
        'fields': 'id,name,created_time'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            businesses = data.get('data', [])
            
            print(f"✅ Found {len(businesses)} business account(s):")
            
            for i, business in enumerate(businesses, 1):
                business_id = business.get('id', 'Unknown')
                business_name = business.get('name', 'Unnamed Business')
                
                print(f"{i}. 🏢 {business_name}")
                print(f"   🆔 ID: {business_id}")
                print()
                
        else:
            print(f"❌ Failed to get business accounts: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking business accounts: {str(e)}")

def main():
    print("🔍 Meta Ad Account Access Diagnostic")
    print("=" * 60)
    
    check_accessible_ad_accounts()
    check_business_accounts()
    
    print("\n" + "=" * 60)
    print("📚 Troubleshooting Guide:")
    print("1. ✅ If your current account ID is accessible → Check app permissions")
    print("2. ❌ If your current account ID is NOT accessible → Use a different account ID")
    print("3. 🏢 Make sure your app is connected to the right business account")
    print("4. 🔧 Update AD_ACCOUNT_ID in .env file if needed")

if __name__ == "__main__":
    main()