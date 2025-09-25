import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import time

# Import real API data fetchers
try:
    from .meta_ads_real import get_meta_ads_data
except ImportError:
    print("[DATA-FETCHER] Meta ads fetcher not available")
    get_meta_ads_data = None

class DataCache:
    """Simple in-memory cache for API data"""
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
        self.ttl = 300  # 5 minutes TTL
    
    def get(self, key: str) -> Any:
        """Get data from cache if not expired"""
        if key in self.cache and key in self.timestamps:
            if time.time() - self.timestamps[key] < self.ttl:
                return self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set data in cache with timestamp"""
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def clear_expired(self) -> None:
        """Clear expired cache entries"""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.timestamps.items()
            if current_time - timestamp >= self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
            del self.timestamps[key]

# Global cache instance
cache = DataCache()

def fetch_google_ads_data(user_role: str = None) -> Dict[str, Any]:
    """
    Fetch mock Google Ads data. In production, this would call the Google Ads API.
    
    Args:
        user_role: User's role to filter relevant data
    
    Returns:
        Dictionary containing Google Ads metrics
    """
    cache_key = f"google_ads_{user_role}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        print("Returning cached Google Ads data")
        return cached_data
    
    print("Fetching fresh Google Ads data")
    
    # TODO: Replace with actual Google Ads API call
    # Example of what the real API call would look like:
    # from google.ads.googleads.client import GoogleAdsClient
    # client = GoogleAdsClient.load_from_storage()
    # ga_service = client.get_service("GoogleAdsService")
    # query = """
    #     SELECT
    #         campaign.id,
    #         campaign.name,
    #         metrics.impressions,
    #         metrics.clicks,
    #         metrics.cost_micros,
    #         metrics.conversions
    #     FROM campaign
    #     WHERE segments.date DURING LAST_30_DAYS
    # """
    # response = ga_service.search_stream(customer_id="YOUR_CUSTOMER_ID", query=query)
    
    # Mock data generation
    campaigns = [
        "Summer Sale Campaign",
        "Holiday Promotion",
        "Brand Awareness Drive",
        "Product Launch Campaign",
        "Retargeting Campaign"
    ]
    
    mock_data = {
        "total_spend": round(random.uniform(10000, 50000), 2),
        "total_impressions": random.randint(100000, 500000),
        "total_clicks": random.randint(5000, 25000),
        "total_conversions": random.randint(200, 1000),
        "average_cpc": round(random.uniform(1.5, 3.5), 2),
        "ctr": round(random.uniform(2.0, 8.0), 2),
        "conversion_rate": round(random.uniform(3.0, 12.0), 2),
        "campaigns": []
    }
    
    # Generate campaign-specific data
    for i, campaign in enumerate(campaigns):
        campaign_data = {
            "id": f"camp_{i+1}",
            "name": campaign,
            "spend": round(random.uniform(2000, 10000), 2),
            "impressions": random.randint(20000, 100000),
            "clicks": random.randint(1000, 5000),
            "conversions": random.randint(40, 200),
            "cpc": round(random.uniform(1.0, 4.0), 2),
            "ctr": round(random.uniform(1.5, 9.0), 2),
            "conversion_rate": round(random.uniform(2.5, 15.0), 2)
        }
        mock_data["campaigns"].append(campaign_data)
    
    # Add historical data for charts (last 30 days)
    historical_data = []
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        historical_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "spend": round(random.uniform(300, 1500), 2),
            "clicks": random.randint(150, 800),
            "impressions": random.randint(5000, 20000),
            "conversions": random.randint(10, 50)
        })
    
    mock_data["historical_data"] = historical_data
    mock_data["last_updated"] = datetime.now().isoformat()
    
    # Cache the data
    cache.set(cache_key, mock_data)
    
    return mock_data

def fetch_meta_ads_data(user_role: str = None) -> Dict[str, Any]:
    """
    Fetch mock Meta ads data. In production, this would use the real Meta Marketing API.
    
    Args:
        user_role: User's role to filter relevant data
    
    Returns:
        Dictionary containing Meta ads metrics
    """
    cache_key = f"meta_ads_{user_role}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        print("Returning cached Meta ads data")
        return cached_data
    
    print("Fetching fresh Meta ads data")
    
    # Mock Meta ads data structure
    mock_data = {
        "account_info": {
            "name": "Meta Ads Account",
            "currency": "USD",
            "timezone_name": "UTC"
        },
        "campaigns": [
            {
                "id": "120234091337580024",
                "name": "Meta Brand Campaign",
                "objective": "OUTCOME_TRAFFIC",
                "status": "ACTIVE"
            },
            {
                "id": "120234091337580025", 
                "name": "Meta Retargeting Campaign",
                "objective": "OUTCOME_ENGAGEMENT",
                "status": "ACTIVE"
            }
        ],
        "summary_metrics": {
            "total_impressions": random.randint(50000, 150000),
            "total_clicks": random.randint(2000, 8000),
            "total_spend": round(random.uniform(1000, 5000), 2),
            "total_conversions": random.randint(50, 200),
            "ctr": round(random.uniform(2.0, 6.0), 2),
            "cpc": round(random.uniform(0.5, 3.0), 2),
            "cost_per_conversion": round(random.uniform(10, 50), 2),
            "reach": random.randint(30000, 100000)
        },
        "historical_data": [],
        "data_source": "meta_marketing_api_mock",
        "last_updated": datetime.now().isoformat()
    }
    
    # Add historical data for charts (last 30 days)
    historical_data = []
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        historical_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "spend": round(random.uniform(50, 200), 2),
            "clicks": random.randint(50, 300),
            "impressions": random.randint(2000, 8000),
            "conversions": random.randint(2, 15)
        })
    
    mock_data["historical_data"] = historical_data
    
    # Cache the data
    cache.set(cache_key, mock_data)
    
    return mock_data

def fetch_google_analytics_data(user_role: str = None) -> Dict[str, Any]:
    """
    Fetch mock Google Analytics data. In production, this would call the Google Analytics API.
    
    Args:
        user_role: User's role to filter relevant data
    
    Returns:
        Dictionary containing Google Analytics metrics
    """
    cache_key = f"google_analytics_{user_role}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        print("Returning cached Google Analytics data")
        return cached_data
    
    print("Fetching fresh Google Analytics data")
    
    # TODO: Replace with actual Google Analytics API call
    # Example of what the real API call would look like:
    # from google.analytics.data_v1beta import BetaAnalyticsDataClient
    # from google.analytics.data_v1beta.types import RunReportRequest, Dimension, Metric
    # client = BetaAnalyticsDataClient()
    # request = RunReportRequest(
    #     property=f"properties/{PROPERTY_ID}",
    #     dimensions=[Dimension(name="date")],
    #     metrics=[
    #         Metric(name="sessions"),
    #         Metric(name="totalUsers"),
    #         Metric(name="bounceRate"),
    #         Metric(name="sessionDuration")
    #     ],
    #     date_ranges=[DateRange(start_date="30daysAgo", end_date="today")]
    # )
    # response = client.run_report(request)
    
    # Mock data generation
    mock_data = {
        "total_sessions": random.randint(15000, 75000),
        "total_users": random.randint(12000, 60000),
        "page_views": random.randint(50000, 200000),
        "bounce_rate": round(random.uniform(25.0, 65.0), 2),
        "avg_session_duration": round(random.uniform(120, 300), 0),
        "conversion_rate": round(random.uniform(2.0, 8.0), 2),
        "revenue": round(random.uniform(25000, 100000), 2)
    }
    
    # Generate traffic source data
    traffic_sources = [
        {"source": "organic", "sessions": random.randint(5000, 25000)},
        {"source": "direct", "sessions": random.randint(3000, 15000)},
        {"source": "social", "sessions": random.randint(2000, 10000)},
        {"source": "paid", "sessions": random.randint(4000, 20000)},
        {"source": "referral", "sessions": random.randint(1000, 5000)}
    ]
    mock_data["traffic_sources"] = traffic_sources
    
    # Generate top pages data
    top_pages = [
        {"page": "/", "page_views": random.randint(8000, 25000)},
        {"page": "/products", "page_views": random.randint(5000, 15000)},
        {"page": "/about", "page_views": random.randint(2000, 8000)},
        {"page": "/contact", "page_views": random.randint(1500, 6000)},
        {"page": "/blog", "page_views": random.randint(3000, 12000)}
    ]
    mock_data["top_pages"] = top_pages
    
    # Add historical data for charts (last 30 days)
    historical_data = []
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        historical_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "sessions": random.randint(400, 2000),
            "users": random.randint(300, 1500),
            "page_views": random.randint(1200, 6000),
            "bounce_rate": round(random.uniform(20.0, 70.0), 2)
        })
    
    mock_data["historical_data"] = historical_data
    mock_data["last_updated"] = datetime.now().isoformat()
    
    # Cache the data
    cache.set(cache_key, mock_data)
    
    return mock_data

def get_combined_kpi_data(user_role: str = None) -> Dict[str, Any]:
    """
    Combine data from multiple sources and filter based on user role.
    
    Args:
        user_role: User's role to determine what data to return
    
    Returns:
        Combined KPI data filtered by user role
    """
    # Import data enhancer
    from services.data_enhancer import enhance_historical_data
    
    # Try to get real Google Ads data first, fallback to mock
    try:
        from services.google_ads_real import get_real_google_ads_data
        ads_data = get_real_google_ads_data(user_role)
        print("[DATA-FETCHER] Using real Google Ads data")
        # Enhance with demo historical data if needed
        ads_data = enhance_historical_data(ads_data, "Google Ads")
    except Exception as e:
        print(f"[DATA-FETCHER] Real Google Ads data unavailable: {e}")
        ads_data = fetch_google_ads_data(user_role)
        print("[DATA-FETCHER] Using mock Google Ads data")
    
    # Try to get real Meta ads data first, fallback to mock
    try:
        if get_meta_ads_data:
            meta_data = get_meta_ads_data()
            print("[DATA-FETCHER] Using real Meta ads data")
            # Enhance with demo historical data if needed
            from .data_enhancer import enhance_historical_data
            meta_data = enhance_historical_data(meta_data, "Meta Ads")
        else:
            print("[DATA-FETCHER] Meta ads fetcher not available")
            meta_data = fetch_meta_ads_data(user_role)
    except Exception as e:
        print(f"[DATA-FETCHER] Real Meta ads data unavailable: {e}")
        meta_data = fetch_meta_ads_data(user_role)
        print("[DATA-FETCHER] Using mock Meta ads data")
    
    # Try to get real Google Analytics data first, fallback to mock
    try:
        from services.google_analytics_real import get_real_google_analytics_data
        analytics_data = get_real_google_analytics_data(user_role)
        print("[DATA-FETCHER] Using real Google Analytics data")
        # Enhance with demo historical data if needed
        analytics_data = enhance_historical_data(analytics_data, "Google Analytics")
    except Exception as e:
        print(f"[DATA-FETCHER] Real Google Analytics data unavailable: {e}")
        analytics_data = fetch_google_analytics_data(user_role)
        print("[DATA-FETCHER] Using mock Google Analytics data")
    
    combined_data = {
        "user_role": user_role,
        "last_updated": datetime.now().isoformat(),
        "google_ads": ads_data,
        "meta_ads": meta_data,
        "google_analytics": analytics_data
    }
    
    # Calculate combined metrics from Google Ads and Meta Ads
    total_ad_spend = ads_data.get("total_spend", 0) + meta_data.get("summary_metrics", {}).get("total_spend", 0)
    total_impressions = ads_data.get("total_impressions", 0) + meta_data.get("summary_metrics", {}).get("total_impressions", 0)
    total_clicks = ads_data.get("total_clicks", 0) + meta_data.get("summary_metrics", {}).get("total_clicks", 0)
    total_conversions = ads_data.get("total_conversions", 0) + meta_data.get("summary_metrics", {}).get("total_conversions", 0)
    
    # Calculate combined CTR
    combined_ctr = round((total_clicks / total_impressions) * 100, 2) if total_impressions > 0 else 0
    
    # Filter data based on user role
    if user_role == "finance":
        # Finance users see cost and revenue focused data
        combined_data["key_metrics"] = {
            "total_ad_spend": total_ad_spend,
            "total_revenue": analytics_data["revenue"],
            "roas": round(analytics_data["revenue"] / total_ad_spend, 2) if total_ad_spend > 0 else 0,
            "cost_per_conversion": round(total_ad_spend / total_conversions, 2) if total_conversions > 0 else 0,
            "conversion_value": round(analytics_data["revenue"] / total_conversions, 2) if total_conversions > 0 else 0
        }
    elif user_role == "marketing":
        # Marketing users see engagement and performance data
        combined_data["key_metrics"] = {
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "ctr": combined_ctr,
            "total_sessions": analytics_data["total_sessions"],
            "bounce_rate": analytics_data["bounce_rate"],
            "conversion_rate": analytics_data["conversion_rate"]
        }
    else:
        # Admin users see all data
        combined_data["key_metrics"] = {
            "total_ad_spend": total_ad_spend,
            "total_revenue": analytics_data["revenue"],
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "total_sessions": analytics_data["total_sessions"],
            "conversion_rate": analytics_data["conversion_rate"],
            "roas": round(analytics_data["revenue"] / total_ad_spend, 2) if total_ad_spend > 0 else 0
        }
    
    return combined_data

def clear_cache():
    """Clear all cached data"""
    cache.cache.clear()
    cache.timestamps.clear()
    print("Cache cleared")

def get_cache_stats():
    """Get cache statistics"""
    cache.clear_expired()
    return {
        "cached_items": len(cache.cache),
        "cache_keys": list(cache.cache.keys())
    }