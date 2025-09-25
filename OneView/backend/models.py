from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and role-based access"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'marketing', 'finance', 'admin'
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

class KpiData(db.Model):
    """Model to store KPI metrics data from various sources"""
    __tablename__ = 'kpi_data'
    
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)  # 'google_ads', 'google_analytics', etc.
    metric_name = db.Column(db.String(255), nullable=False)
    metric_value = db.Column(db.Numeric(15, 2), nullable=False)
    metric_type = db.Column(db.String(50), nullable=False)  # 'currency', 'percentage', 'count', etc.
    date_recorded = db.Column(db.Date, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    campaign_id = db.Column(db.String(255), nullable=True)
    campaign_name = db.Column(db.String(255), nullable=True)
    additional_data = db.Column(db.JSON, nullable=True)  # For storing extra metadata
    
    def to_dict(self):
        """Convert KPI data object to dictionary"""
        return {
            'id': self.id,
            'source': self.source,
            'metric_name': self.metric_name,
            'metric_value': float(self.metric_value),
            'metric_type': self.metric_type,
            'date_recorded': self.date_recorded.isoformat(),
            'timestamp': self.timestamp.isoformat(),
            'campaign_id': self.campaign_id,
            'campaign_name': self.campaign_name,
            'additional_data': self.additional_data
        }

class CampaignPerformance(db.Model):
    """Model to store campaign performance data over time"""
    __tablename__ = 'campaign_performance'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.String(255), nullable=False)
    campaign_name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    impressions = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
    cost = db.Column(db.Numeric(10, 2), default=0)
    revenue = db.Column(db.Numeric(10, 2), default=0)
    ctr = db.Column(db.Numeric(5, 4), default=0)  # Click-through rate
    conversion_rate = db.Column(db.Numeric(5, 4), default=0)
    roas = db.Column(db.Numeric(10, 2), default=0)  # Return on ad spend
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert campaign performance object to dictionary"""
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'campaign_name': self.campaign_name,
            'date': self.date.isoformat(),
            'impressions': self.impressions,
            'clicks': self.clicks,
            'conversions': self.conversions,
            'cost': float(self.cost),
            'revenue': float(self.revenue),
            'ctr': float(self.ctr),
            'conversion_rate': float(self.conversion_rate),
            'roas': float(self.roas),
            'created_at': self.created_at.isoformat()
        }