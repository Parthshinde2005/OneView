import React from 'react';

/**
 * MetricCard Component
 * Displays a single KPI metric in a visually appealing card
 * 
 * @param {string} title - The metric title/name
 * @param {string|number} value - The metric value
 * @param {number} change - The percentage change (can be positive, negative, or zero)
 * @param {string} type - The type of metric (currency, percentage, count)
 * @param {string} icon - Optional icon component or emoji
 */
const MetricCard = ({ 
  title, 
  value, 
  change = null, 
  type = 'count',
  icon = null,
  subtitle = null
}) => {
  console.log('[FRONTEND] MetricCard rendering:', { title, value, change, type, icon });
  
  /**
   * Format the display value based on type
   */
  const formatValue = (val, metricType) => {
    if (val === null || val === undefined) return 'N/A';
    
    const numValue = typeof val === 'string' ? parseFloat(val) : val;
    
    if (isNaN(numValue)) return val;
    
    switch (metricType) {
      case 'currency':
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        }).format(numValue);
        
      case 'percentage':
        return `${numValue.toFixed(1)}%`;
        
      case 'decimal':
        return numValue.toFixed(2);
        
      case 'count':
      default:
        return new Intl.NumberFormat('en-US').format(numValue);
    }
  };
  
  /**
   * Determine change indicator class and icon
   */
  const getChangeInfo = (changeValue) => {
    if (changeValue === null || changeValue === undefined) {
      return { className: 'neutral', indicator: '', text: '' };
    }
    
    const numChange = typeof changeValue === 'string' ? parseFloat(changeValue) : changeValue;
    
    if (isNaN(numChange)) {
      return { className: 'neutral', indicator: '', text: '' };
    }
    
    if (numChange > 0) {
      return {
        className: 'positive',
        indicator: '↗',
        text: `+${numChange.toFixed(1)}%`
      };
    } else if (numChange < 0) {
      return {
        className: 'negative',
        indicator: '↙',
        text: `${numChange.toFixed(1)}%`
      };
    } else {
      return {
        className: 'neutral',
        indicator: '→',
        text: '0.0%'
      };
    }
  };
  
  const changeInfo = getChangeInfo(change);
  const formattedValue = formatValue(value, type);
  
  return (
    <div className="card metric-card">
      {/* Icon */}
      {icon && (
        <div style={{ 
          fontSize: '1.5rem', 
          marginBottom: '0.5rem',
          opacity: 0.7
        }}>
          {icon}
        </div>
      )}
      
      {/* Title */}
      <div className="metric-title">
        {title}
      </div>
      
      {/* Value */}
      <div className="metric-value">
        {formattedValue}
      </div>
      
      {/* Subtitle */}
      {subtitle && (
        <div style={{ 
          fontSize: '0.8rem', 
          color: '#a0aec0', 
          marginTop: '0.25rem' 
        }}>
          {subtitle}
        </div>
      )}
      
      {/* Change Indicator */}
      {/* {change !== null && change !== undefined && (
        <div className={`metric-change ${changeInfo.className}`}>
          <span style={{ fontSize: '1rem' }}>
            {changeInfo.indicator}
          </span>
          <span>
            {changeInfo.text}
          </span>
        </div>
      )} */}
    </div>
  );
};

export default MetricCard;