import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, kpiAPI } from '../services/api';
import MetricCard from '../components/MetricCard';
import CampaignChart from '../components/CampaignChart';

/**
 * DashboardPage Component
 * Main dashboard displaying KPI data based on user role
 */
const DashboardPage = () => {
  const navigate = useNavigate();
  
  // State management
  const [userData, setUserData] = useState(null);
  const [kpiData, setKpiData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [refreshing, setRefreshing] = useState(false);
  
  // Load user data on component mount
  useEffect(() => {
    const user = authAPI.getUserData();
    if (user) {
      setUserData(user);
    } else {
      navigate('/login');
    }
  }, [navigate]);
  
  // Load KPI data on component mount
  useEffect(() => {
    if (userData) {
      console.log('[FRONTEND] User data found, loading KPI data for user:', userData);
      loadKPIData();
    }
  }, [userData]);
  
  /**
   * Load KPI data from API
   */
  const loadKPIData = async (forceRefresh = false) => {
    try {
      if (forceRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      
      setError('');
      
      console.log('[FRONTEND] Making API request for KPI data, forceRefresh:', forceRefresh);
      const response = await kpiAPI.getKPIData(forceRefresh);
      console.log('[FRONTEND] Received API response:', response);
      console.log('[FRONTEND] Response structure:', {
        success: response.success,
        user_role: response.user_role,
        user_name: response.user_name,
        data_keys: Object.keys(response.data || {}),
        cache_stats: response.cache_stats
      });
      // The actual KPI data is in the 'data' property of the response
      setKpiData(response.data);
      console.log('[FRONTEND] KPI data set successfully');
      
    } catch (err) {
      console.error('[FRONTEND] Failed to load KPI data:', err);
      console.error('[FRONTEND] Error details:', err.response);
      setError(err.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };
  
  /**
   * Handle user logout
   */
  const handleLogout = () => {
    authAPI.logout();
    navigate('/login');
  };
  
  /**
   * Handle data refresh
   */
  const handleRefresh = () => {
    loadKPIData(true);
  };
  
  /**
   * Get role-specific greeting
   */
  const getRoleGreeting = (role) => {
    const greetings = {
      admin: 'Administrator Dashboard',
      marketing: 'Marketing Performance Dashboard',
      finance: 'Financial Metrics Dashboard'
    };
    return greetings[role] || 'KPI Dashboard';
  };
  
  /**
   * Get role-specific metrics to display
   */
  const getRoleMetrics = (data, role) => {
    console.log('[FRONTEND] getRoleMetrics called with data:', data, 'role:', role);
    if (!data || !data.key_metrics) {
      console.log('[FRONTEND] No data or key_metrics found, returning empty array');
      return [];
    }
    
    const metrics = data.key_metrics;
    console.log('[FRONTEND] Processing metrics:', metrics);
    const commonProps = { change: Math.random() * 20 - 10 }; // Mock change data
    
    switch (role) {
      case 'finance':
        return [
          {
            title: 'Total Ad Spend',
            value: metrics.total_ad_spend,
            type: 'currency',
            icon: '💰',
            ...commonProps
          },
          {
            title: 'Total Revenue',
            value: metrics.total_revenue,
            type: 'currency',
            icon: '📈',
            ...commonProps
          },
          {
            title: 'ROAS',
            value: metrics.roas,
            type: 'decimal',
            icon: '🎯',
            subtitle: 'Return on Ad Spend',
            ...commonProps
          },
          {
            title: 'Cost per Conversion',
            value: metrics.cost_per_conversion,
            type: 'currency',
            icon: '🔄',
            ...commonProps
          }
        ];
        
      case 'marketing':
        return [
          {
            title: 'Total Impressions',
            value: metrics.total_impressions,
            type: 'count',
            icon: '👁️',
            ...commonProps
          },
          {
            title: 'Total Clicks',
            value: metrics.total_clicks,
            type: 'count',
            icon: '👆',
            ...commonProps
          },
          {
            title: 'Click-Through Rate',
            value: metrics.ctr,
            type: 'percentage',
            icon: '📊',
            ...commonProps
          },
          {
            title: 'Total Sessions',
            value: metrics.total_sessions,
            type: 'count',
            icon: '🌐',
            ...commonProps
          },
          {
            title: 'Bounce Rate',
            value: metrics.bounce_rate,
            type: 'percentage',
            icon: '🏃',
            ...commonProps
          },
          {
            title: 'Conversion Rate',
            value: metrics.conversion_rate,
            type: 'percentage',
            icon: '✅',
            ...commonProps
          }
        ];
        
      default: // admin
        return [
          {
            title: 'Total Ad Spend',
            value: metrics.total_ad_spend,
            type: 'currency',
            icon: '💰',
            ...commonProps
          },
          {
            title: 'Total Revenue',
            value: metrics.total_revenue,
            type: 'currency',
            icon: '📈',
            ...commonProps
          },
          {
            title: 'Total Impressions',
            value: metrics.total_impressions,
            type: 'count',
            icon: '👁️',
            ...commonProps
          },
          {
            title: 'Total Clicks',
            value: metrics.total_clicks,
            type: 'count',
            icon: '👆',
            ...commonProps
          },
          {
            title: 'Total Sessions',
            value: metrics.total_sessions,
            type: 'count',
            icon: '🌐',
            ...commonProps
          },
          {
            title: 'ROAS',
            value: metrics.roas,
            type: 'decimal',
            icon: '🎯',
            subtitle: 'Return on Ad Spend',
            ...commonProps
          }
        ];
    }
  };
  
  // Show loading state
  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading dashboard data...</p>
        <p style={{ fontSize: '0.9rem', color: '#a0aec0', marginTop: '1rem' }}>
          Fetching data from Google Ads, Meta Ads, and Google Analytics...
        </p>
      </div>
    );
  }
  
  // Show error state
  if (error) {
    return (
      <div className="container" style={{ paddingTop: '2rem' }}>
        <div className="alert alert-error">
          <h3>Failed to load dashboard</h3>
          <p>{error}</p>
          <button onClick={() => loadKPIData()} className="btn btn-primary mt-3">
            Try Again
          </button>
        </div>
      </div>
    );
  }
  
  // Prepare data for charts
  console.log('[FRONTEND] Preparing chart data from kpiData:', kpiData);
  const chartData = kpiData?.google_ads?.historical_data || [];
  console.log('[FRONTEND] Chart data:', chartData);
  const last30Days = chartData.slice(-30).reverse(); // Show last 30 days in chronological order
  console.log('[FRONTEND] Last 30 days data:', last30Days);
  
  const metricsToShow = getRoleMetrics(kpiData, userData?.role);
  console.log('[FRONTEND] Metrics to show:', metricsToShow);
  
  return (
    <div>
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div>
            <h1 className="header-title">
              {getRoleGreeting(userData?.role)}
            </h1>
            <p style={{ color: '#a0aec0', marginTop: '0.25rem' }}>
              Welcome back, {userData?.first_name}!
            </p>
          </div>
          
          <div className="header-actions">
            <div className="user-info">
              <span className="user-role">{userData?.role}</span>
              <span style={{ margin: '0 0.5rem' }}>•</span>
              <span>{userData?.email}</span>
            </div>
            
            <div className="flex gap-2">
              <button
                onClick={handleRefresh}
                className="btn btn-secondary"
                disabled={refreshing}
              >
                {refreshing ? (
                  <>
                    <div className="spinner" style={{ width: '14px', height: '14px' }}></div>
                    Refreshing
                  </>
                ) : (
                  <>🔄 Refresh</>
                )}
              </button>
              
              <button
                onClick={handleLogout}
                className="btn btn-danger"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <div className="container">
        {/* Last Updated Info */}
        {kpiData?.last_updated && (
          <div className="mb-4">
            <p style={{ color: '#a0aec0', fontSize: '0.9rem' }}>
              Last updated: {new Date(kpiData.last_updated).toLocaleString()}
            </p>
          </div>
        )}
        
        {/* Metrics Grid */}
        <div className="dashboard-grid">
          {metricsToShow.map((metric, index) => (
            <MetricCard
              key={index}
              title={metric.title}
              value={metric.value}
              change={metric.change}
              type={metric.type}
              icon={metric.icon}
              subtitle={metric.subtitle}
            />
          ))}
        </div>
        
        {/* Charts Section */}
        <div className="chart-grid">
          {/* Spend/Revenue Chart */}
          {(userData?.role === 'admin' || userData?.role === 'finance') && (
            <CampaignChart
              data={last30Days}
              labels={last30Days.map(item => new Date(item.date).toLocaleDateString())}
              title="Daily Ad Spend"
              type="line"
              dataKey="spend"
              color="#f56565"
              yAxisLabel="Amount ()"
            />
          )}
          
          {/* Clicks/Traffic Chart */}
          {(userData?.role === 'admin' || userData?.role === 'marketing') && (
            <CampaignChart
              data={last30Days}
              labels={last30Days.map(item => new Date(item.date).toLocaleDateString())}
              title="Daily Clicks"
              type="line"
              dataKey="clicks"
              color="#48bb78"
              yAxisLabel="Clicks"
            />
          )}
          
          {/* Impressions Chart for Marketing */}
          {userData?.role === 'marketing' && (
            <CampaignChart
              data={last30Days}
              labels={last30Days.map(item => new Date(item.date).toLocaleDateString())}
              title="Daily Impressions"
              type="bar"
              dataKey="impressions"
              color="#63b3ed"
              yAxisLabel="Impressions"
            />
          )}
          
          {/* Conversions Chart */}
          <CampaignChart
            data={last30Days}
            labels={last30Days.map(item => new Date(item.date).toLocaleDateString())}
            title="Daily Conversions"
            type="bar"
            dataKey="conversions"
            color="#ed8936"
            yAxisLabel="Conversions"
          />
        </div>
        
        {/* Campaign Performance Table (for admin only) */}
        {userData?.role === 'admin' && (
          <div className="card mt-4">
            <h3 className="chart-title">Campaign Performance Summary</h3>
            <div style={{ overflowX: 'auto' }}>
              {(() => {
                // Get campaigns from both Google Ads and Meta Ads
                const googleAdsCampaigns = (kpiData?.google_ads?.campaigns || []).map(campaign => ({
                  ...campaign,
                  platform: 'Google Ads',
                  cost: campaign.cost || campaign.spend || 0
                }));
                
                const metaAdsCampaigns = (kpiData?.meta_ads?.campaigns || []).map(campaign => ({
                  ...campaign,
                  platform: 'Meta Ads',
                  cost: campaign.cost || campaign.spend || 0
                }));
                
                const apiCampaigns = [...googleAdsCampaigns, ...metaAdsCampaigns];
                const mockCampaigns = [
                  {
                    name: "🎯 Brand Awareness Campaign",
                    spend: 2485.67,
                    clicks: 312,
                    impressions: 8945,
                    conversions: 28,
                    ctr: 3.49,
                    status: "ENABLED"
                  },
                  {
                    name: "🚀 Product Launch Campaign",
                    spend: 1876.23,
                    clicks: 245,
                    impressions: 7256,
                    conversions: 19,
                    ctr: 3.38,
                    status: "ENABLED"
                  },
                  {
                    name: "🔄 Retargeting Campaign",
                    spend: 892.45,
                    clicks: 156,
                    impressions: 3890,
                    conversions: 22,
                    ctr: 4.01,
                    status: "ENABLED"
                  },
                  {
                    name: "🏷️ Black Friday Sale",
                    spend: 3254.89,
                    clicks: 423,
                    impressions: 12456,
                    conversions: 67,
                    ctr: 3.40,
                    status: "PAUSED"
                  },
                  {
                    name: "📱 Mobile App Install",
                    spend: 567.34,
                    clicks: 89,
                    impressions: 2134,
                    conversions: 12,
                    ctr: 4.17,
                    status: "ENABLED"
                  },
                  {
                    name: "🌟 Holiday Promotion",
                    spend: 1456.78,
                    clicks: 198,
                    impressions: 5432,
                    conversions: 31,
                    ctr: 3.64,
                    status: "PAUSED"
                  }
                ];
                
                const campaignsToShow = apiCampaigns.length > 0 ? apiCampaigns : mockCampaigns;
                const isUsingMockData = apiCampaigns.length === 0;
                
                return (
                  <>
                    {isUsingMockData && (
                      <div style={{ 
                        marginBottom: '1rem', 
                        padding: '0.75rem', 
                        backgroundColor: 'rgba(66, 153, 225, 0.1)', 
                        borderRadius: '0.5rem',
                        border: '1px solid rgba(66, 153, 225, 0.3)',
                        color: '#63b3ed'
                      }}>
                        <small>
                          📊 <strong>Demo Data:</strong> Showing example campaigns for demonstration purposes
                        </small>
                      </div>
                    )}
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                      <thead>
                        <tr style={{ borderBottom: '1px solid rgba(74, 85, 104, 0.3)' }}>
                          <th style={{ padding: '1rem', textAlign: 'left', color: '#a0aec0' }}>Campaign</th>
                          <th style={{ padding: '1rem', textAlign: 'left', color: '#a0aec0' }}>Platform</th>
                          <th style={{ padding: '1rem', textAlign: 'right', color: '#a0aec0' }}>Spend</th>
                          <th style={{ padding: '1rem', textAlign: 'right', color: '#a0aec0' }}>Clicks</th>
                          <th style={{ padding: '1rem', textAlign: 'right', color: '#a0aec0' }}>CTR</th>
                          <th style={{ padding: '1rem', textAlign: 'right', color: '#a0aec0' }}>Conversions</th>
                          <th style={{ padding: '1rem', textAlign: 'right', color: '#a0aec0' }}>Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {campaignsToShow.map((campaign, index) => (
                          <tr key={index} style={{ borderBottom: '1px solid rgba(74, 85, 104, 0.2)' }}>
                            <td style={{ padding: '1rem', color: '#e2e8f0' }}>{campaign.name}</td>
                            <td style={{ padding: '1rem', color: '#e2e8f0' }}>
                              <span style={{ 
                                backgroundColor: campaign.platform === 'Google Ads' ? '#4285f4' : '#1877f2',
                                color: 'white',
                                padding: '0.25rem 0.5rem',
                                borderRadius: '0.25rem',
                                fontSize: '0.75rem'
                              }}>
                                {campaign.platform || 'Unknown'}
                              </span>
                            </td>
                            <td style={{ padding: '1rem', textAlign: 'right', color: '#e2e8f0' }}>
                              ${(campaign.cost || campaign.spend || 0).toLocaleString()}
                            </td>
                            <td style={{ padding: '1rem', textAlign: 'right', color: '#e2e8f0' }}>
                              {(campaign.clicks || 0).toLocaleString()}
                            </td>
                            <td style={{ padding: '1rem', textAlign: 'right', color: '#e2e8f0' }}>
                              {(campaign.ctr || 0).toFixed(2)}%
                            </td>
                            <td style={{ padding: '1rem', textAlign: 'right', color: '#e2e8f0' }}>
                              {(campaign.conversions || 0).toLocaleString()}
                            </td>
                            <td style={{ padding: '1rem', textAlign: 'right', color: '#e2e8f0' }}>
                              <span style={{ 
                                backgroundColor: (campaign.status === 'ENABLED' || campaign.status === 'ACTIVE') ? '#48bb78' : '#f56565',
                                color: 'white',
                                padding: '0.25rem 0.5rem',
                                borderRadius: '0.25rem',
                                fontSize: '0.75rem'
                              }}>
                                {campaign.status || 'UNKNOWN'}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </>
                );
              })()}
            </div>
            <div style={{ 
              marginTop: '1rem', 
              padding: '0.75rem', 
              backgroundColor: 'rgba(72, 187, 120, 0.1)', 
              borderRadius: '0.5rem',
              color: '#68d391',
              fontSize: '0.85rem',
              textAlign: 'center'
            }}>
              <div style={{ marginBottom: '0.5rem' }}>
                ✅ Google Ads API: {kpiData?.google_ads?.data_source?.includes('google_ads_api') ? 'Connected' : 'Demo'} - 
                {' '}{(kpiData?.google_ads?.campaigns || []).length} campaigns
              </div>
              <div>
                🔵 Meta Ads API: {kpiData?.meta_ads?.campaigns?.length > 0 ? 'Connected' : 'Demo'} - 
                {' '}{(kpiData?.meta_ads?.campaigns || []).length} campaigns
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
};

export default DashboardPage;