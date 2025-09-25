"""
Real Google Ads API integration for KPI Dashboard
This module fetches live data from Google Ads API
"""

import os
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from typing import Dict, List, Any

class GoogleAdsDataFetcher:
    """Real Google Ads API data fetcher"""
    
    def __init__(self, config_path: str = None):
        """Initialize with Google Ads client"""
        try:
            if config_path:
                self.client = GoogleAdsClient.load_from_storage(path=config_path)
            else:
                # Try to load from default location
                self.client = GoogleAdsClient.load_from_storage()
            self.customer_id = "7217957631"  # Your customer ID (updated to correct ID)
            print(f"[GOOGLE-ADS] Client initialized successfully")
        except Exception as e:
            print(f"[GOOGLE-ADS] Failed to initialize client: {e}")
            self.client = None
    
    def fetch_campaign_performance(self, days: int = 90) -> Dict[str, Any]:
        """
        Fetch real campaign performance data from Google Ads API
        
        Args:
            days: Number of days to fetch data for
            
        Returns:
            Dictionary containing campaign performance data
        """
        if not self.client:
            print("[GOOGLE-ADS] Client not initialized, returning mock data")
            return self._get_mock_data()
        
        try:
            googleads_service = self.client.get_service("GoogleAdsService")
            
            # Calculate date range
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            # Query for campaign performance data - check all statuses and longer date range
            query = f"""
                SELECT
                    campaign.id,
                    campaign.name,
                    campaign.status,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.cost_micros,
                    metrics.conversions,
                    segments.date
                FROM campaign
                WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
                ORDER BY segments.date DESC
            """
            
            print(f"[GOOGLE-ADS] Fetching campaign data from {start_date} to {end_date} (last {days} days)")
            print(f"[GOOGLE-ADS] Query: {query}")
            
            # Execute the search request
            stream = googleads_service.search_stream(
                customer_id=self.customer_id, 
                query=query
            )
            
            # Process results
            campaigns_data = {}
            daily_data = []
            total_metrics = {
                'impressions': 0,
                'clicks': 0,
                'cost': 0,
                'conversions': 0
            }
            
            row_count = 0
            for batch in stream:
                for row in batch.results:
                    row_count += 1
                    print(f"[GOOGLE-ADS] Processing row {row_count}: Campaign {row.campaign.name} ({row.campaign.id}) - Status: {row.campaign.status.name} - Date: {row.segments.date}")
                    print(f"[GOOGLE-ADS] Row data - Impressions: {row.metrics.impressions}, Clicks: {row.metrics.clicks}, Cost: {row.metrics.cost_micros/1000000:.2f}, Conversions: {row.metrics.conversions}")
                    campaign_id = str(row.campaign.id)
                    campaign_name = row.campaign.name
                    date_str = row.segments.date
                    
                    # Convert cost from micros to dollars
                    cost_dollars = row.metrics.cost_micros / 1_000_000
                    
                    # Aggregate campaign data
                    if campaign_id not in campaigns_data:
                        campaigns_data[campaign_id] = {
                            'id': campaign_id,
                            'name': campaign_name,
                            'impressions': 0,
                            'clicks': 0,
                            'cost': 0,
                            'conversions': 0,
                            'ctr': 0,
                            'conversion_rate': 0
                        }
                    
                    # Add to campaign totals
                    campaigns_data[campaign_id]['impressions'] += row.metrics.impressions
                    campaigns_data[campaign_id]['clicks'] += row.metrics.clicks
                    campaigns_data[campaign_id]['cost'] += cost_dollars
                    campaigns_data[campaign_id]['conversions'] += row.metrics.conversions
                    
                    # Calculate rates
                    if campaigns_data[campaign_id]['impressions'] > 0:
                        campaigns_data[campaign_id]['ctr'] = (
                            campaigns_data[campaign_id]['clicks'] / 
                            campaigns_data[campaign_id]['impressions'] * 100
                        )
                    
                    if campaigns_data[campaign_id]['clicks'] > 0:
                        campaigns_data[campaign_id]['conversion_rate'] = (
                            campaigns_data[campaign_id]['conversions'] / 
                            campaigns_data[campaign_id]['clicks'] * 100
                        )
                    
                    # Calculate CTR for this row
                    row_ctr = (row.metrics.clicks / row.metrics.impressions * 100) if row.metrics.impressions > 0 else 0
                    
                    # Add to daily data
                    daily_data.append({
                        'date': date_str,
                        'campaign_id': campaign_id,
                        'campaign_name': campaign_name,
                        'impressions': row.metrics.impressions,
                        'clicks': row.metrics.clicks,
                        'cost': cost_dollars,
                        'conversions': row.metrics.conversions,
                        'ctr': round(row_ctr, 2)
                    })
                    
                    # Add to totals
                    total_metrics['impressions'] += row.metrics.impressions
                    total_metrics['clicks'] += row.metrics.clicks
                    total_metrics['cost'] += cost_dollars
                    total_metrics['conversions'] += row.metrics.conversions
            
            # Calculate overall rates
            overall_ctr = (total_metrics['clicks'] / total_metrics['impressions'] * 100) if total_metrics['impressions'] > 0 else 0
            overall_conversion_rate = (total_metrics['conversions'] / total_metrics['clicks'] * 100) if total_metrics['clicks'] > 0 else 0
            average_cpc = (total_metrics['cost'] / total_metrics['clicks']) if total_metrics['clicks'] > 0 else 0
            
            # Format response
            result = {
                'total_spend': round(total_metrics['cost'], 2),
                'total_impressions': total_metrics['impressions'],
                'total_clicks': total_metrics['clicks'],
                'total_conversions': int(total_metrics['conversions']),
                'ctr': round(overall_ctr, 2),
                'conversion_rate': round(overall_conversion_rate, 2),
                'average_cpc': round(average_cpc, 2),
                'campaigns': list(campaigns_data.values()),
                'historical_data': self._aggregate_daily_data(daily_data),
                'last_updated': datetime.now().isoformat(),
                'data_source': 'google_ads_api'
            }
            
            print(f"[GOOGLE-ADS] Successfully fetched data for {len(campaigns_data)} campaigns")
            print(f"[GOOGLE-ADS] ===== REAL GOOGLE ADS DATA =====")
            print(f"[GOOGLE-ADS] Total Spend: ${result['total_spend']}")
            print(f"[GOOGLE-ADS] Total Impressions: {result['total_impressions']:,}")
            print(f"[GOOGLE-ADS] Total Clicks: {result['total_clicks']:,}")
            print(f"[GOOGLE-ADS] Total Conversions: {result['total_conversions']}")
            print(f"[GOOGLE-ADS] CTR: {result['ctr']}%")
            print(f"[GOOGLE-ADS] Conversion Rate: {result['conversion_rate']}%")
            print(f"[GOOGLE-ADS] Average CPC: ${result['average_cpc']}")
            print(f"[GOOGLE-ADS] Historical Data Points: {len(result['historical_data'])}")
            print(f"[GOOGLE-ADS] Data Source: {result['data_source']}")
            
            for campaign in result['campaigns']:
                print(f"[GOOGLE-ADS] Campaign: {campaign['name']} (ID: {campaign['id']})")
                print(f"[GOOGLE-ADS]   - Impressions: {campaign['impressions']:,}")
                print(f"[GOOGLE-ADS]   - Clicks: {campaign['clicks']:,}")
                print(f"[GOOGLE-ADS]   - Cost: ${campaign['cost']:.2f}")
                print(f"[GOOGLE-ADS]   - Conversions: {campaign['conversions']}")
                print(f"[GOOGLE-ADS]   - CTR: {campaign['ctr']:.2f}%")
                print(f"[GOOGLE-ADS]   - Conversion Rate: {campaign['conversion_rate']:.2f}%")
            
            print(f"[GOOGLE-ADS] ===== END REAL GOOGLE ADS DATA =====")
            return result
            
        except GoogleAdsException as ex:
            print(f"[GOOGLE-ADS] Google Ads API error: {ex}")
            print(f"[GOOGLE-ADS] Request ID: {ex.request_id}")
            print(f"[GOOGLE-ADS] Falling back to mock data")
            return self._get_mock_data()
        
        except Exception as e:
            print(f"[GOOGLE-ADS] Unexpected error: {e}")
            print(f"[GOOGLE-ADS] Falling back to mock data")
            return self._get_mock_data()
    
    def _aggregate_daily_data(self, daily_data: List[Dict]) -> List[Dict]:
        """Aggregate daily data by date"""
        daily_aggregates = {}
        
        for record in daily_data:
            date = record['date']
            if date not in daily_aggregates:
                daily_aggregates[date] = {
                    'date': date,
                    'spend': 0,
                    'clicks': 0,
                    'impressions': 0,
                    'conversions': 0
                }
            
            daily_aggregates[date]['spend'] += record['cost']
            daily_aggregates[date]['clicks'] += record['clicks']
            daily_aggregates[date]['impressions'] += record['impressions']
            daily_aggregates[date]['conversions'] += record['conversions']
        
        # Sort by date and return
        return sorted(daily_aggregates.values(), key=lambda x: x['date'])
    
    def _get_mock_data(self) -> Dict[str, Any]:
        """Fallback mock data when API is not available"""
        from services.data_fetcher import fetch_google_ads_data
        mock_data = fetch_google_ads_data()
        mock_data['data_source'] = 'mock_data'
        return mock_data

# Global instance for use in the application
def get_real_google_ads_data(user_role: str = None) -> Dict[str, Any]:
    """
    Get real Google Ads data or fallback to mock data
    
    Args:
        user_role: User role for filtering (maintained for compatibility)
        
    Returns:
        Google Ads performance data
    """
    try:
        # Try to initialize with local config file
        config_path = os.path.join(os.path.dirname(__file__), "..", "google-ads.yaml")
        fetcher = GoogleAdsDataFetcher(config_path)
        return fetcher.fetch_campaign_performance()
    except Exception as e:
        print(f"[GOOGLE-ADS] Failed to fetch real data: {e}")
        # Fallback to mock data
        from services.data_fetcher import fetch_google_ads_data
        return fetch_google_ads_data(user_role)