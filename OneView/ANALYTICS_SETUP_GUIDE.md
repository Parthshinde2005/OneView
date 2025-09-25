## Google Analytics API Setup Guide

### The Problem
The Google Analytics API requires **Service Account credentials** (JSON format), not OAuth2 credentials (YAML format). The current `google-ads.yaml` file contains OAuth2 credentials which work for Google Ads but not for Google Analytics.

### Solution Steps

#### Step 1: Create a Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create a new one)
3. Navigate to **IAM & Admin > Service Accounts**
4. Click **"Create Service Account"**
5. Give it a name like "KPI Dashboard Analytics"
6. Click **"Create and Continue"**

#### Step 2: Generate Service Account Key
1. In the service accounts list, click on your newly created service account
2. Go to the **"Keys"** tab
3. Click **"Add Key" > "Create new key"**
4. Select **"JSON"** format
5. Click **"Create"** - this will download a JSON file

#### Step 3: Place the Key File
1. Rename the downloaded JSON file to `service-account-key.json`
2. Place it in the `backend/` directory: `G:\KPI\backend\service-account-key.json`

#### Step 4: Enable APIs
1. In Google Cloud Console, go to **APIs & Services > Library**
2. Enable **"Google Analytics Data API"**
3. Enable **"Google Analytics Reporting API"** (if not already enabled)

#### Step 5: Grant Analytics Access
1. Go to [Google Analytics](https://analytics.google.com/)
2. Navigate to **Admin** (gear icon)
3. In the **Property** column, click **"Property Access Management"**
4. Click **"+"** to add a user
5. Enter the **service account email** (from the JSON file, looks like: `name@project.iam.gserviceaccount.com`)
6. Select **"Viewer"** role
7. Click **"Add"**

### File Structure Should Look Like:
```
G:\KPI\backend\
├── app.py
├── google-ads.yaml          (for Google Ads API)
├── service-account-key.json (for Google Analytics API)
└── services/
    ├── google_ads_real.py
    └── google_analytics_real.py
```

### Testing
After completing these steps, run:
```bash
python test_analytics.py
```

### Sample service-account-key.json Format:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

### Important Notes:
- **Never commit the service account JSON file to version control**
- Add `service-account-key.json` to your `.gitignore` file
- The service account email must be added as a user in Google Analytics
- Make sure your GA4 property ID (478395445) is correct