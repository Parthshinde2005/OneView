// Test script to verify API connection from frontend
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

async function testConnection() {
  try {
    console.log('Testing API connection...');
    
    // Test login first
    const loginResponse = await api.post('/login', {
      email: 'admin@company.com',
      password: 'admin123'
    });
    
    console.log('Login successful:', {
      status: loginResponse.status,
      token: loginResponse.data.access_token ? 'Token received' : 'No token',
      user: loginResponse.data.user
    });
    
    // Set token for next request
    const token = loginResponse.data.access_token;
    api.defaults.headers.Authorization = `Bearer ${token}`;
    
    // Test KPI data fetch
    const kpiResponse = await api.get('/kpi-data');
    console.log('KPI data fetch successful:', {
      status: kpiResponse.status,
      dataKeys: Object.keys(kpiResponse.data || {}),
      hasData: !!kpiResponse.data.data,
      userRole: kpiResponse.data.user_role
    });
    
    console.log('All tests passed! API connection is working.');
    
  } catch (error) {
    console.error('API test failed:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      config: {
        url: error.config?.url,
        method: error.config?.method,
        baseURL: error.config?.baseURL
      }
    });
  }
}

// Run the test
testConnection();