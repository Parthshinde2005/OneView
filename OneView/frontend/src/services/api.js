import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout to allow API calls to complete
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors globally
api.interceptors.response.use(
  (response) => {
    console.log('[AXIOS] Response interceptor - success:', {
      url: response.config.url,
      status: response.status,
      dataKeys: Object.keys(response.data || {})
    });
    return response;
  },
  (error) => {
    console.error('[AXIOS] Response interceptor - error:', {
      url: error.config?.url,
      status: error.response?.status,
      statusText: error.response?.statusText,
      message: error.message,
      data: error.response?.data
    });
    
    if (error.response?.status === 401) {
      // Token expired or invalid, redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_data');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Auth API functions
 */
export const authAPI = {
  /**
   * Login user with email and password
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise} Response with token and user data
   */
  login: async (email, password) => {
    try {
      const response = await api.post('/login', {
        email: email.toLowerCase().trim(),
        password,
      });
      
      const { access_token, user } = response.data;
      
      // Store token and user data in localStorage
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_data', JSON.stringify(user));
      
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.error || 'Login failed. Please try again.'
      );
    }
  },

  /**
   * Logout user by clearing stored data
   */
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_data');
  },

  /**
   * Check if user is authenticated
   * @returns {boolean} Authentication status
   */
  isAuthenticated: () => {
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user_data');
    return !!(token && userData);
  },

  /**
   * Get stored user data
   * @returns {Object|null} User data or null if not found
   */
  getUserData: () => {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
  },

  /**
   * Get user profile from server
   * @returns {Promise} User profile data
   */
  getProfile: async () => {
    try {
      const response = await api.get('/user/profile');
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.error || 'Failed to fetch user profile'
      );
    }
  },
};

/**
 * KPI Data API functions
 */
export const kpiAPI = {
  /**
   * Fetch KPI data based on user role
   * @param {boolean} forceRefresh - Force refresh cached data
   * @returns {Promise} KPI data
   */
  getKPIData: async (forceRefresh = false) => {
    try {
      const params = forceRefresh ? { force_refresh: 'true' } : {};
      console.log('[API] Making request to /kpi-data with params:', params);
      const response = await api.get('/kpi-data', { params });
      console.log('[API] Response received:', {
        status: response.status,
        statusText: response.statusText,
        headers: response.headers,
        dataKeys: Object.keys(response.data || {}),
        dataType: typeof response.data
      });
      return response.data;
    } catch (error) {
      console.error('[API] KPI data fetch error:', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        config: error.config
      });
      const errorMessage = error.code === 'ECONNABORTED' && error.message.includes('timeout')
        ? 'Request timed out. The API is fetching data from multiple sources (Google Ads, Meta Ads, Google Analytics). Please try refreshing the page.'
        : error.response?.data?.error || error.message || 'Failed to fetch KPI data';
      throw new Error(errorMessage);
    }
  },

  /**
   * Clear data cache (admin only)
   * @returns {Promise} Success message
   */
  clearCache: async () => {
    try {
      const response = await api.post('/cache/clear');
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.error || 'Failed to clear cache'
      );
    }
  },

  /**
   * Get cache statistics (admin only)
   * @returns {Promise} Cache statistics
   */
  getCacheStats: async () => {
    try {
      const response = await api.get('/cache/stats');
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.error || 'Failed to fetch cache statistics'
      );
    }
  },
};

/**
 * Health check API function
 */
export const healthAPI = {
  /**
   * Check API health status
   * @returns {Promise} Health status
   */
  checkHealth: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('API health check failed');
    }
  },
};

/**
 * Generic API error handler
 * @param {Error} error - The error object
 * @returns {string} User-friendly error message
 */
export const handleAPIError = (error) => {
  if (error.response) {
    // Server responded with error status
    return error.response.data?.error || 'Server error occurred';
  } else if (error.request) {
    // Request was made but no response received
    return 'Unable to connect to server. Please check your connection.';
  } else {
    // Something else happened
    return error.message || 'An unexpected error occurred';
  }
};

// Export the axios instance for custom requests
export default api;