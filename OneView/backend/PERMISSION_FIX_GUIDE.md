# 🚨 Meta API Permissions Issue Detected

## The Issue:
Your access token doesn't have the required permissions for the Meta Marketing API.

**Error Code:** 200 (OAuthException)  
**Message:** "Ad account owner has NOT grant ads_management or ads_read permission"

## 🔧 How to Fix:

### Step 1: Get Proper Permissions
1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app from the dropdown
3. Click "Get Token" → "Get User Access Token"
4. Make sure to select these permissions:
   - ✅ `ads_management` (required for creating campaigns)
   - ✅ `ads_read` (required for reading campaign data)
   - ✅ `business_management` (recommended)

### Step 2: Generate New Token
1. After selecting permissions, click "Generate Access Token"
2. Copy the new token
3. Replace the old token in your `.env` file

### Step 3: Verify Account Access
Make sure you have admin/owner access to the ad account:
- Account ID: `24596190633380263`
- Visit: [Business Manager](https://business.facebook.com/)
- Check your ad account permissions

### Step 4: App Review (If Needed)
For production use, your app may need Facebook's review for advanced permissions:
- Visit your [Facebook App Dashboard](https://developers.facebook.com/apps/)
- Go to "App Review" section
- Submit for `ads_management` permission

## 🧪 Test Again:
Once you have the proper permissions, run:
```bash
python meta_api_test.py
```

## 📚 References:
- [Marketing API Permissions](https://developers.facebook.com/docs/marketing-api/get-started/authorization/#permissions-and-features)
- [Access Token Tool](https://developers.facebook.com/tools/accesstoken/)
- [App Dashboard](https://developers.facebook.com/apps/)