import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

/**
 * CampaignChart Component
 * Displays campaign performance data using Chart.js
 * 
 * @param {Array} data - Chart data points
 * @param {Array} labels - Chart labels (x-axis)
 * @param {string} title - Chart title
 * @param {string} type - Chart type ('line' or 'bar')
 * @param {string} dataKey - Key to extract data values
 * @param {string} color - Primary color for the chart
 */
const CampaignChart = ({ 
  data = [], 
  labels = [], 
  title = 'Campaign Performance',
  type = 'line',
  dataKey = 'value',
  color = '#63b3ed',
  yAxisLabel = '',
  height = 350
}) => {
  
  /**
   * Generate chart colors based on primary color
   */
  const generateColors = (baseColor, alpha = 0.8) => {
    // Convert hex to rgb for alpha manipulation
    const hexToRgb = (hex) => {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
      } : null;
    };
    
    const rgb = hexToRgb(baseColor);
    if (!rgb) return baseColor;
    
    return {
      solid: baseColor,
      transparent: `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${alpha})`,
      gradient: `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.1)`
    };
  };
  
  const colors = generateColors(color);
  
  /**
   * Prepare chart data
   */
  const chartData = {
    labels: labels.length > 0 ? labels : data.map((_, index) => `Item ${index + 1}`),
    datasets: [
      {
        label: title,
        data: data.map(item => 
          typeof item === 'object' ? item[dataKey] : item
        ),
        borderColor: colors.solid,
        backgroundColor: type === 'line' ? colors.gradient : colors.transparent,
        borderWidth: 2,
        fill: type === 'line',
        tension: type === 'line' ? 0.4 : 0,
        pointBackgroundColor: colors.solid,
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: type === 'line' ? 4 : 0,
        pointHoverRadius: type === 'line' ? 6 : 0,
        hoverBackgroundColor: colors.solid,
        hoverBorderColor: '#ffffff',
      }
    ]
  };
  
  /**
   * Chart configuration options
   */
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#e2e8f0',
          font: {
            size: 12,
            weight: '600'
          },
          padding: 20,
          usePointStyle: true,
        }
      },
      tooltip: {
        backgroundColor: 'rgba(26, 32, 44, 0.95)',
        titleColor: '#e2e8f0',
        bodyColor: '#e2e8f0',
        borderColor: colors.solid,
        borderWidth: 1,
        cornerRadius: 8,
        padding: 12,
        displayColors: true,
        callbacks: {
          label: function(context) {
            const label = context.dataset.label || '';
            const value = context.parsed.y;
            
            if (dataKey === 'cost' || dataKey === 'revenue') {
              return `${label}: $${value.toLocaleString()}`;
            } else if (dataKey === 'ctr' || dataKey === 'conversion_rate') {
              return `${label}: ${value.toFixed(2)}%`;
            } else {
              return `${label}: ${value.toLocaleString()}`;
            }
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(74, 85, 104, 0.3)',
          borderColor: 'rgba(74, 85, 104, 0.5)',
        },
        ticks: {
          color: '#a0aec0',
          font: {
            size: 11
          },
          maxRotation: 45,
          minRotation: 0
        }
      },
      y: {
        grid: {
          color: 'rgba(74, 85, 104, 0.3)',
          borderColor: 'rgba(74, 85, 104, 0.5)',
        },
        ticks: {
          color: '#a0aec0',
          font: {
            size: 11
          },
          callback: function(value) {
            if (dataKey === 'cost' || dataKey === 'revenue') {
              return '$' + value.toLocaleString();
            } else if (dataKey === 'ctr' || dataKey === 'conversion_rate') {
              return value.toFixed(1) + '%';
            } else {
              return value.toLocaleString();
            }
          }
        },
        title: {
          display: !!yAxisLabel,
          text: yAxisLabel,
          color: '#a0aec0',
          font: {
            size: 12,
            weight: '600'
          }
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index'
    },
    animation: {
      duration: 750,
      easing: 'easeInOutQuart'
    }
  };
  
  // Handle empty data
  if (!data || data.length === 0) {
    return (
      <div className="card">
        <h3 className="chart-title">{title}</h3>
        <div className="chart-container">
          <div className="loading">
            <p>No data available</p>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="card">
      <h3 className="chart-title">{title}</h3>
      <div className="chart-container" style={{ height: `${height}px` }}>
        {type === 'line' ? (
          <Line data={chartData} options={options} />
        ) : (
          <Bar data={chartData} options={options} />
        )}
      </div>
    </div>
  );
};

export default CampaignChart;