import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';

/**
 * LoginPage Component
 * Handles user authentication with email and password
 */
const LoginPage = () => {
  const navigate = useNavigate();
  
  // Form state
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  
  // UI state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  /**
   * Handle input changes
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (error) {
      setError('');
    }
  };
  
  /**
   * Handle form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Basic validation
    if (!formData.email.trim() || !formData.password.trim()) {
      setError('Please fill in all fields');
      return;
    }
    
    if (!isValidEmail(formData.email)) {
      setError('Please enter a valid email address');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      await authAPI.login(formData.email, formData.password);
      
      // Redirect to dashboard on successful login
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  /**
   * Email validation helper
   */
  const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };
  
  /**
   * Fill demo credentials
   */
  const fillDemoCredentials = (role) => {
    const credentials = {
      admin: { email: 'admin@company.com', password: 'admin123' },
      marketing: { email: 'marketing@company.com', password: 'marketing123' },
      finance: { email: 'finance@company.com', password: 'finance123' }
    };
    
    setFormData(credentials[role]);
    setError('');
  };
  
  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">KPI Dashboard</h1>
        <p className="text-center mb-4" style={{ color: '#a0aec0' }}>
          Sign in to access your personalized dashboard
        </p>
        
        {/* Error Alert */}
        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}
        
        {/* Login Form */}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email" className="form-label">
              Email Address
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="form-input"
              placeholder="Enter your email"
              disabled={loading}
              autoComplete="email"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="form-input"
              placeholder="Enter your password"
              disabled={loading}
              autoComplete="current-password"
            />
          </div>
          
          <button
            type="submit"
            className="btn btn-primary w-full"
            disabled={loading}
          >
            {loading ? (
              <>
                <div className="spinner" style={{ width: '16px', height: '16px' }}></div>
                Signing in...
              </>
            ) : (
              'Sign In'
            )}
          </button>
        </form>
        
        {/* Demo Credentials */}
        <div className="mt-4">
          <hr style={{ margin: '1.5rem 0', border: 'none', borderTop: '1px solid rgba(74, 85, 104, 0.3)' }} />
          <p className="text-center mb-3" style={{ color: '#a0aec0', fontSize: '0.9rem' }}>
            Demo Accounts (Click to auto-fill)
          </p>
          
          <div className="flex flex-col gap-2">
            <button
              type="button"
              onClick={() => fillDemoCredentials('admin')}
              className="btn btn-secondary"
              disabled={loading}
              style={{ fontSize: '0.8rem', padding: '0.5rem 1rem' }}
            >
              Admin User (Full Access)
            </button>
            
            <button
              type="button"
              onClick={() => fillDemoCredentials('marketing')}
              className="btn btn-secondary"
              disabled={loading}
              style={{ fontSize: '0.8rem', padding: '0.5rem 1rem' }}
            >
              Marketing Manager (Engagement Data)
            </button>
            
            <button
              type="button"
              onClick={() => fillDemoCredentials('finance')}
              className="btn btn-secondary"
              disabled={loading}
              style={{ fontSize: '0.8rem', padding: '0.5rem 1rem' }}
            >
              Finance Manager (Cost & Revenue Data)
            </button>
          </div>
        </div>
        
        {/* Additional Info */}
        <div className="mt-4 text-center">
          <p style={{ color: '#718096', fontSize: '0.8rem' }}>
            This is a demo application. Use the buttons above to quickly test different user roles.
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;