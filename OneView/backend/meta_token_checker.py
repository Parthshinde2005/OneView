#!/usr/bin/env python3
"""
Meta Access Token Permission Checker
Checks what permissions your current access token has.
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_token_permissions():
    """Check what permissions the current access token has"""
    access_token = os.getenv('META_ACCESS_TOKEN')
    
    if not access_token:
        print("❌ META_ACCESS_TOKEN not found in .env file")
        return
    
    print("🔍 Checking Meta Access Token Permissions...")
    print(f"🔑 Token: {access_token[:20]}...")
    print("-" * 60)
    
    # Check token info
    url = "https://graph.facebook.com/v23.0/me/permissions"
    params = {
        'access_token': access_token
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            permissions = data.get('data', [])
            
            print(f"✅ Token is valid! Found {len(permissions)} permissions:")
            print()
            
            # Check for required permissions
            required_perms = ['ads_management', 'ads_read', 'business_management']
            has_required = []
            
            for perm in permissions:
                perm_name = perm.get('permission', 'Unknown')
                perm_status = perm.get('status', 'Unknown')
                
                status_icon = "✅" if perm_status == "granted" else "❌"
                print(f"{status_icon} {perm_name}: {perm_status}")
                
                if perm_name in required_perms and perm_status == "granted":
                    has_required.append(perm_name)
            
            print()
            print("📊 Required Permissions Analysis:")
            for req_perm in required_perms:
                has_it = req_perm in has_required
                icon = "✅" if has_it else "❌"
                print(f"{icon} {req_perm}: {'GRANTED' if has_it else 'MISSING'}")
            
            print()
            if len(has_required) >= 2:  # ads_management and ads_read are most important
                print("🎉 Your token has the main required permissions!")
                print("🚀 The Meta API test should work now.")
            else:
                print("⚠️  Your token is missing required permissions.")
                print("📋 You need to regenerate your token with:")
                print("   - ads_management (to create campaigns)")
                print("   - ads_read (to read campaign data)")
                
        else:
            print(f"❌ Failed to check permissions: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
            if response.status_code == 403:
                print("\n💡 This might mean your token is invalid or expired.")
            elif response.status_code == 400:
                print("\n💡 There might be an issue with the token format.")
                
    except Exception as e:
        print(f"❌ Error checking permissions: {str(e)}")

def check_token_info():
    """Get basic info about the access token"""
    access_token = os.getenv('META_ACCESS_TOKEN')
    
    print("\n🔍 Checking Token Info...")
    
    url = "https://graph.facebook.com/v23.0/me"
    params = {
        'access_token': access_token,
        'fields': 'id,name,email'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Token belongs to: {data.get('name', 'Unknown')}")
            print(f"📧 Email: {data.get('email', 'Not available')}")
            print(f"🆔 User ID: {data.get('id', 'Unknown')}")
        else:
            print(f"❌ Cannot get token info: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error getting token info: {str(e)}")

def main():
    print("🔐 Meta Access Token Diagnostic Tool")
    print("=" * 60)
    
    check_token_info()
    check_token_permissions()
    
    print("\n" + "=" * 60)
    print("📚 Next Steps:")
    print("1. If permissions are missing, go to: https://developers.facebook.com/tools/explorer/")
    print("2. Select your app and click 'Get Token' → 'Get User Access Token'")
    print("3. Check these permissions: ads_management, ads_read, business_management")  
    print("4. Generate new token and update your .env file")
    print("5. Run the meta_api_test.py script again")

if __name__ == "__main__":
    main()