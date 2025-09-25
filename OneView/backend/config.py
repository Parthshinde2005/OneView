import os
from datetime import timedelta

class Config:
    """Configuration class for Flask application"""
    
    # Database configuration
    # Using SQLite for development (easier setup, no separate server needed)
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'kpi_dashboard.db')
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # For production, you can switch back to MySQL by setting environment variables:
    # MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    # MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    # MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    # MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
    # MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'kpi_dashboard')
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API configuration
    GOOGLE_ADS_API_KEY = os.environ.get('GOOGLE_ADS_API_KEY', 'mock-ads-key')
    GOOGLE_ANALYTICS_API_KEY = os.environ.get('GOOGLE_ANALYTICS_API_KEY', 'mock-analytics-key')
    
    # Cache configuration
    CACHE_TIMEOUT = 300  # 5 minutes in seconds