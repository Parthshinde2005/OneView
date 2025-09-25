#!/usr/bin/env python3
"""
Meta Marketing API Data Fetcher
Fetches real campaign and performance data from Meta Marketing API
"""

import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MetaAdsFetcher:
    def __init__(self):
        self.access_token = os.getenv('META_ACCESS_TOKEN')
        self.ad_account_id = os.getenv('AD_ACCOUNT_ID')
        self.base_url = 'https://graph.facebook.com/v23.0'
        
        if not self.access_token:
            raise ValueError("META_ACCESS_TOKEN not found in environment variables")
        if not self.ad_account_id:
            raise ValueError("AD_ACCOUNT_ID not found in environment variables")
    
    def get_account_info(self):
        """Get ad account basic information"""
        try:
            url = f"{self.base_url}/{self.ad_account_id}"
            params = {
                'access_token': self.access_token,
                'fields': 'id,name,account_status,currency,timezone_name,business'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[META] Failed to get account info: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[META] Error getting account info: {str(e)}")
            return None
    
    def get_campaigns(self, limit=50):
        """Get campaigns with basic metrics"""
        try:
            url = f"{self.base_url}/{self.ad_account_id}/campaigns"
            params = {
                'access_token': self.access_token,
                'fields': 'id,name,objective,status,created_time,updated_time',
                'limit': limit
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                print(f"[META] Failed to get campaigns: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"[META] Error getting campaigns: {str(e)}")
            return []
    
    def get_campaign_insights(self, campaign_ids=None, date_preset='last_30d'):
        """Get campaign performance insights"""
        try:
            # If no specific campaigns, get insights for the account
            if campaign_ids:
                # Get insights for specific campaigns (batch request)
                insights_data = []
                for campaign_id in campaign_ids:
                    insight = self._get_single_campaign_insights(campaign_id, date_preset)
                    if insight:
                        insights_data.extend(insight)
                return insights_data
            else:
                # Get account-level insights
                return self._get_account_insights(date_preset)
                
        except Exception as e:
            print(f"[META] Error getting campaign insights: {str(e)}")
            return []
    
    def _get_single_campaign_insights(self, campaign_id, date_preset):
        """Get insights for a single campaign"""
        try:
            url = f"{self.base_url}/{campaign_id}/insights"
            params = {
                'access_token': self.access_token,
                'fields': 'campaign_id,campaign_name,impressions,clicks,spend,ctr,cpc,cpp,cpm,reach,frequency,actions,conversions,cost_per_conversion',
                'date_preset': date_preset
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                print(f"[META] Failed to get insights for campaign {campaign_id}: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"[META] Error getting insights for campaign {campaign_id}: {str(e)}")
            return []
    
    def _get_account_insights(self, date_preset):
        """Get account-level insights"""
        try:
            url = f"{self.base_url}/{self.ad_account_id}/insights"
            params = {
                'access_token': self.access_token,
                'fields': 'impressions,clicks,spend,ctr,cpc,cpp,cpm,reach,frequency,actions,conversions,cost_per_conversion',
                'date_preset': date_preset,
                'level': 'account'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                print(f"[META] Failed to get account insights: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"[META] Error getting account insights: {str(e)}")
            return []
    
    def get_daily_insights(self, days_back=30):
        """Get daily performance data for the last N days"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            url = f"{self.base_url}/{self.ad_account_id}/insights"
            params = {
                'access_token': self.access_token,
                'fields': 'impressions,clicks,spend,ctr,cpc,conversions,cost_per_conversion,reach',
                'time_range': json.dumps({
                    'since': start_date.strftime('%Y-%m-%d'),
                    'until': end_date.strftime('%Y-%m-%d')
                }),
                'time_increment': 1,  # Daily breakdown
                'level': 'account'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                print(f"[META] Failed to get daily insights: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"[META] Error getting daily insights: {str(e)}")
            return []
    
    def get_comprehensive_data(self):
        """Get comprehensive Meta ads data for dashboard"""
        print("[META] Fetching comprehensive Meta ads data...")
        
        try:
            # Get account info
            account_info = self.get_account_info()
            print(f"[META] Account info: {account_info.get('name', 'Unknown') if account_info else 'Failed'}")
            
            # Get campaigns
            campaigns = self.get_campaigns()
            print(f"[META] Found {len(campaigns)} campaigns")
            
            # Get campaign insights
            campaign_insights = []
            if campaigns:
                campaign_ids = [c['id'] for c in campaigns]
                campaign_insights = self.get_campaign_insights(campaign_ids)
                print(f"[META] Found {len(campaign_insights)} campaign insights")
            
            # Get account-level insights
            account_insights = self._get_account_insights('last_30d')
            print(f"[META] Found {len(account_insights)} account insights")
            
            # Get daily data for charts
            daily_data = self.get_daily_insights(30)
            print(f"[META] Found {len(daily_data)} daily data points")
            
            # Calculate summary metrics
            summary_metrics = self._calculate_summary_metrics(account_insights, daily_data)
            
            # Structure the response
            result = {
                'account_info': account_info,
                'campaigns': campaigns,
                'campaign_insights': campaign_insights,
                'summary_metrics': summary_metrics,
                'historical_data': daily_data,
                'data_source': 'meta_marketing_api',
                'last_updated': datetime.now().isoformat()
            }
            
            print(f"[META] Successfully compiled comprehensive data")
            return result
            
        except Exception as e:
            print(f"[META] Error getting comprehensive data: {str(e)}")
            return self._get_fallback_data()
    
    def _calculate_summary_metrics(self, account_insights, daily_data):
        """Calculate summary metrics from insights data"""
        try:
            if not account_insights and not daily_data:
                return self._get_default_metrics()
            
            # Use account insights if available, otherwise aggregate daily data
            data_source = account_insights[0] if account_insights else None
            
            if not data_source and daily_data:
                # Aggregate daily data
                data_source = {
                    'impressions': sum(float(d.get('impressions', 0)) for d in daily_data),
                    'clicks': sum(float(d.get('clicks', 0)) for d in daily_data),
                    'spend': sum(float(d.get('spend', 0)) for d in daily_data),
                    'conversions': sum(float(d.get('conversions', 0)) for d in daily_data),
                    'reach': max(float(d.get('reach', 0)) for d in daily_data) if daily_data else 0
                }
                
                # Calculate derived metrics
                if data_source['impressions'] > 0:
                    data_source['ctr'] = (data_source['clicks'] / data_source['impressions']) * 100
                if data_source['clicks'] > 0:
                    data_source['cpc'] = data_source['spend'] / data_source['clicks']
                if data_source['conversions'] > 0:
                    data_source['cost_per_conversion'] = data_source['spend'] / data_source['conversions']
            
            if data_source:
                return {
                    'total_impressions': int(float(data_source.get('impressions', 0))),
                    'total_clicks': int(float(data_source.get('clicks', 0))),
                    'total_spend': float(data_source.get('spend', 0)),
                    'total_conversions': int(float(data_source.get('conversions', 0))),
                    'ctr': float(data_source.get('ctr', 0)),
                    'cpc': float(data_source.get('cpc', 0)),
                    'cost_per_conversion': float(data_source.get('cost_per_conversion', 0)),
                    'reach': int(float(data_source.get('reach', 0)))
                }
            else:
                return self._get_default_metrics()
                
        except Exception as e:
            print(f"[META] Error calculating summary metrics: {str(e)}")
            return self._get_default_metrics()
    
    def _get_default_metrics(self):
        """Get default metrics when no data is available"""
        return {
            'total_impressions': 0,
            'total_clicks': 0,
            'total_spend': 0.0,
            'total_conversions': 0,
            'ctr': 0.0,
            'cpc': 0.0,
            'cost_per_conversion': 0.0,
            'reach': 0
        }
    
    def _get_fallback_data(self):
        """Get fallback data when API fails"""
        print("[META] Using fallback data due to API failure")
        return {
            'account_info': {
                'name': 'Meta Ads Account',
                'currency': 'USD',
                'timezone_name': 'UTC'
            },
            'campaigns': [],
            'campaign_insights': [],
            'summary_metrics': self._get_default_metrics(),
            'historical_data': [],
            'data_source': 'meta_marketing_api_fallback',
            'last_updated': datetime.now().isoformat(),
            'error': 'API connection failed'
        }

def get_meta_ads_data():
    """Main function to get Meta ads data"""
    try:
        fetcher = MetaAdsFetcher()
        return fetcher.get_comprehensive_data()
    except Exception as e:
        print(f"[META] Critical error: {str(e)}")
        return MetaAdsFetcher()._get_fallback_data()

if __name__ == "__main__":
    # Test the fetcher
    data = get_meta_ads_data()
    print(json.dumps(data, indent=2, default=str))