# Meta Marketing API Test

This script tests the Meta Marketing API by creating a new ad campaign.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r meta_requirements.txt
   ```

2. **Environment Variables:**
   Make sure your `.env` file contains:
   ```
   META_ACCESS_TOKEN=your_access_token_here
   AD_ACCOUNT_ID=act_your_account_id_here
   ```

3. **Run the test:**
   ```bash
   python meta_api_test.py
   ```

## What the script does:

1. **Connection Test**: Verifies API connectivity by fetching account information
2. **List Campaigns**: Shows existing campaigns in your ad account
3. **Create Campaign**: Creates a new test campaign with these properties:
   - Name: "My First API Campaign - [timestamp]"
   - Objective: LINK_CLICKS
   - Status: PAUSED (safe for testing)
4. **Verify Creation**: Lists campaigns again to confirm the new one was created

## Expected Output:

```
🚀 Meta Marketing API Test Suite
==================================================
✅ Initialized Meta API client
📱 Ad Account: act_24596190633380263
🔑 Token: EAAP136xNSFQBPhXeM5...

🔍 Testing API connection...
✅ Connection successful!
📊 Account Name: Your Account Name
💰 Currency: USD
🌍 Timezone: America/New_York
📈 Status: 1

📋 Fetching last 5 campaigns...
✅ Found X campaigns:

🚀 Creating test campaign...
✅ Campaign created successfully!
🆔 Campaign ID: 123456789
```

## Troubleshooting:

- **401 Unauthorized**: Check your access token
- **403 Forbidden**: Verify account permissions
- **400 Bad Request**: Check the campaign parameters
- **Connection errors**: Verify internet connectivity

## API Reference:

- [Meta Marketing API Documentation](https://developers.facebook.com/docs/marketing-api)
- [Campaign Creation Guide](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)