"""
Real Google Analytics API integration for KPI Dashboard
This module fetches live data from Google Analytics API
"""

import os
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    Dimension,
    Metric,
    DateRange,
    Filter,
    FilterExpression
)
from google.oauth2 import service_account
from typing import Dict, List, Any

class GoogleAnalyticsDataFetcher:
    """Real Google Analytics API data fetcher"""
    
    def __init__(self, property_id: str = None, credentials_path: str = None):
        """Initialize with Google Analytics client"""
        try:
            # You need to replace this with your actual GA4 Property ID
            self.property_id = property_id or "478395445"  # Replace with your actual property ID
            
            if credentials_path and os.path.exists(credentials_path):
                # Use service account credentials
                credentials = service_account.Credentials.from_service_account_file(
                    credentials_path,
                    scopes=["https://www.googleapis.com/auth/analytics.readonly"]
                )
                self.client = BetaAnalyticsDataClient(credentials=credentials)
            else:
                # Try to use default credentials
                self.client = BetaAnalyticsDataClient()
            
            print(f"[GOOGLE-ANALYTICS] Client initialized successfully for property: {self.property_id}")
        except Exception as e:
            print(f"[GOOGLE-ANALYTICS] Failed to initialize client: {e}")
            self.client = None
    
    def fetch_analytics_data(self, days: int = 30) -> Dict[str, Any]:
        """
        Fetch real analytics data from Google Analytics API
        
        Args:
            days: Number of days to fetch data for
            
        Returns:
            Dictionary containing analytics data
        """
        if not self.client or self.property_id == "YOUR_GA4_PROPERTY_ID":
            print("[GOOGLE-ANALYTICS] Client not initialized or property ID not set, returning mock data")
            return self._get_mock_data()
        
        try:
            # Calculate date range
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            print(f"[GOOGLE-ANALYTICS] Fetching analytics data from {start_date} to {end_date}")
            
            # Main metrics request
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[
                    Dimension(name="date"),
                ],
                metrics=[
                    Metric(name="sessions"),
                    Metric(name="totalUsers"),
                    Metric(name="screenPageViews"),
                    Metric(name="bounceRate"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="conversions"),
                    Metric(name="totalRevenue"),
                ],
                date_ranges=[
                    DateRange(start_date=start_date.strftime("%Y-%m-%d"), 
                             end_date=end_date.strftime("%Y-%m-%d"))
                ],
                order_bys=[
                    {"dimension": {"dimension_name": "date", "order_type": "ALPHANUMERIC"}}
                ]
            )
            
            response = self.client.run_report(request)
            
            # Process the response
            total_sessions = 0
            total_users = 0
            total_page_views = 0
            total_bounce_rate = 0
            total_session_duration = 0
            total_conversions = 0
            total_revenue = 0
            daily_data = []
            valid_days = 0
            
            for row in response.rows:
                date_str = row.dimension_values[0].value
                sessions = int(row.metric_values[0].value) if row.metric_values[0].value else 0
                users = int(row.metric_values[1].value) if row.metric_values[1].value else 0
                page_views = int(row.metric_values[2].value) if row.metric_values[2].value else 0
                bounce_rate = float(row.metric_values[3].value) if row.metric_values[3].value else 0
                session_duration = float(row.metric_values[4].value) if row.metric_values[4].value else 0
                conversions = float(row.metric_values[5].value) if row.metric_values[5].value else 0
                revenue = float(row.metric_values[6].value) if row.metric_values[6].value else 0
                
                # Aggregate totals
                total_sessions += sessions
                total_users += users
                total_page_views += page_views
                total_bounce_rate += bounce_rate
                total_session_duration += session_duration
                total_conversions += conversions
                total_revenue += revenue
                
                if sessions > 0:  # Only count days with activity
                    valid_days += 1
                
                # Add to daily data
                daily_data.append({
                    'date': date_str,
                    'sessions': sessions,
                    'users': users,
                    'page_views': page_views,
                    'bounce_rate': bounce_rate,
                    'conversions': conversions,
                    'revenue': revenue
                })
            
            # Calculate averages
            avg_bounce_rate = (total_bounce_rate / valid_days) if valid_days > 0 else 0
            avg_session_duration = (total_session_duration / total_sessions) if total_sessions > 0 else 0
            conversion_rate = (total_conversions / total_sessions * 100) if total_sessions > 0 else 0
            
            # Get traffic sources
            traffic_sources = self._fetch_traffic_sources(start_date, end_date)
            
            # Get top pages
            top_pages = self._fetch_top_pages(start_date, end_date)
            
            # Format response
            result = {
                'total_sessions': int(total_sessions),
                'total_users': int(total_users),
                'page_views': int(total_page_views),
                'bounce_rate': round(avg_bounce_rate, 2),
                'avg_session_duration': round(avg_session_duration, 0),
                'conversion_rate': round(conversion_rate, 2),
                'revenue': round(total_revenue, 2),
                'traffic_sources': traffic_sources,
                'top_pages': top_pages,
                'historical_data': daily_data,
                'last_updated': datetime.now().isoformat(),
                'data_source': 'google_analytics_api'
            }
            
            print(f"[GOOGLE-ANALYTICS] Successfully fetched analytics data")
            print(f"[GOOGLE-ANALYTICS] ===== REAL GOOGLE ANALYTICS DATA =====")
            print(f"[GOOGLE-ANALYTICS] Total Sessions: {result['total_sessions']:,}")
            print(f"[GOOGLE-ANALYTICS] Total Users: {result['total_users']:,}")
            print(f"[GOOGLE-ANALYTICS] Page Views: {result['page_views']:,}")
            print(f"[GOOGLE-ANALYTICS] Bounce Rate: {result['bounce_rate']}%")
            print(f"[GOOGLE-ANALYTICS] Revenue: ${result['revenue']:.2f}")
            print(f"[GOOGLE-ANALYTICS] Conversion Rate: {result['conversion_rate']}%")
            print(f"[GOOGLE-ANALYTICS] Historical Data Points: {len(result['historical_data'])}")
            print(f"[GOOGLE-ANALYTICS] Data Source: {result['data_source']}")
            print(f"[GOOGLE-ANALYTICS] ===== END REAL GOOGLE ANALYTICS DATA =====")
            
            return result
            
        except Exception as e:
            print(f"[GOOGLE-ANALYTICS] Google Analytics API error: {e}")
            print(f"[GOOGLE-ANALYTICS] Falling back to mock data")
            return self._get_mock_data()
    
    def _fetch_traffic_sources(self, start_date, end_date) -> List[Dict]:
        """Fetch traffic source data"""
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[
                    Dimension(name="sessionSource"),
                ],
                metrics=[
                    Metric(name="sessions"),
                ],
                date_ranges=[
                    DateRange(start_date=start_date.strftime("%Y-%m-%d"), 
                             end_date=end_date.strftime("%Y-%m-%d"))
                ],
                limit=5
            )
            
            response = self.client.run_report(request)
            
            traffic_sources = []
            for row in response.rows:
                source = row.dimension_values[0].value
                sessions = int(row.metric_values[0].value) if row.metric_values[0].value else 0
                traffic_sources.append({
                    "source": source,
                    "sessions": sessions
                })
            
            return traffic_sources
            
        except Exception as e:
            print(f"[GOOGLE-ANALYTICS] Error fetching traffic sources: {e}")
            return []
    
    def _fetch_top_pages(self, start_date, end_date) -> List[Dict]:
        """Fetch top pages data"""
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[
                    Dimension(name="pagePath"),
                ],
                metrics=[
                    Metric(name="screenPageViews"),
                ],
                date_ranges=[
                    DateRange(start_date=start_date.strftime("%Y-%m-%d"), 
                             end_date=end_date.strftime("%Y-%m-%d"))
                ],
                limit=5
            )
            
            response = self.client.run_report(request)
            
            top_pages = []
            for row in response.rows:
                page = row.dimension_values[0].value
                page_views = int(row.metric_values[0].value) if row.metric_values[0].value else 0
                top_pages.append({
                    "page": page,
                    "page_views": page_views
                })
            
            return top_pages
            
        except Exception as e:
            print(f"[GOOGLE-ANALYTICS] Error fetching top pages: {e}")
            return []
    
    def _get_mock_data(self) -> Dict[str, Any]:
        """Fallback mock data when API is not available"""
        from services.data_fetcher import fetch_google_analytics_data
        mock_data = fetch_google_analytics_data()
        mock_data['data_source'] = 'mock_data'
        return mock_data

# Global function for use in the application
def get_real_google_analytics_data(user_role: str = None) -> Dict[str, Any]:
    """
    Get real Google Analytics data or fallback to mock data
    
    Args:
        user_role: User role for filtering (maintained for compatibility)
        
    Returns:
        Google Analytics data
    """
    try:
        # Use service account credentials for Google Analytics API
        credentials_path = os.path.join(os.path.dirname(__file__), "..", "service-account-key.json")
        
        # GA4 Property ID - already configured
        property_id = "478395445"
        
        print(f"[ANALYTICS-REAL] Attempting to fetch data with property ID: {property_id}")
        print(f"[ANALYTICS-REAL] Looking for credentials at: {credentials_path}")
        
        # Check if credentials file exists
        if not os.path.exists(credentials_path):
            print(f"[ANALYTICS-REAL] Service account key file not found at: {credentials_path}")
            raise FileNotFoundError("Service account key file not found. Please follow the setup guide.")
        
        fetcher = GoogleAnalyticsDataFetcher(property_id=property_id, credentials_path=credentials_path)
        
        if fetcher.client is None:
            raise Exception("Failed to initialize Google Analytics client")
            
        return fetcher.fetch_analytics_data()
    except Exception as e:
        print(f"[GOOGLE-ANALYTICS] Failed to fetch real data: {e}")
        # Fallback to mock data
        from services.data_fetcher import fetch_google_analytics_data
        return fetch_google_analytics_data(user_role)