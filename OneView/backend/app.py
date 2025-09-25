from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Import local modules
from config import Config
from models import db, User, KpiData
from services.data_fetcher import get_combined_kpi_data, clear_cache, get_cache_stats

# Load environment variables
load_dotenv()

# Initialize JWT manager globally
from flask_jwt_extended import JWTManager
jwt = JWTManager()

# Add JWT callbacks for better debugging
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print(f"[JWT-EXPIRED] Token expired for user: {jwt_payload.get('sub')}")
    return jsonify({'error': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    print(f"[JWT-INVALID] Invalid token: {error}")
    return jsonify({'error': 'Invalid token'}), 422

@jwt.unauthorized_loader
def missing_token_callback(error):
    print(f"[JWT-MISSING] Missing token: {error}")
    return jsonify({'error': 'Authorization token is required'}), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    print(f"[JWT-NOT-FRESH] Token not fresh for user: {jwt_payload.get('sub')}")
    return jsonify({'error': 'Fresh token required'}), 401

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    print(f"[INIT] JWT Secret Key configured: {bool(app.config.get('JWT_SECRET_KEY'))}")
    print(f"[INIT] JWT Token expires in: {app.config.get('JWT_ACCESS_TOKEN_EXPIRES')}")
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)  # Use the global JWT instance with callbacks
    CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:3000"], supports_credentials=True)  # Support multiple frontend ports
    
    return app

app = create_app()

# JWT error handlers for better debugging
@app.after_request
def after_request(response):
    # Log all requests for debugging
    print(f"[REQUEST] {request.method} {request.path} -> {response.status_code}")
    return response

# Additional JWT error handling
from flask_jwt_extended.exceptions import JWTExtendedException

@app.errorhandler(JWTExtendedException)
def handle_jwt_exceptions(error):
    print(f"[JWT-EXCEPTION] JWT Error: {str(error)}")
    return jsonify({'error': f'JWT Error: {str(error)}'}), 422

def create_mock_users():
    """Create mock users for testing"""
    # Check if users already exist
    if User.query.first():
        return
    
    mock_users = [
        {
            'email': 'admin@company.com',
            'password': 'admin123',
            'role': 'admin',
            'first_name': 'Admin',
            'last_name': 'User'
        },
        {
            'email': 'marketing@company.com',
            'password': 'marketing123',
            'role': 'marketing',
            'first_name': 'Marketing',
            'last_name': 'Manager'
        },
        {
            'email': 'finance@company.com',
            'password': 'finance123',
            'role': 'finance',
            'first_name': 'Finance',
            'last_name': 'Manager'
        }
    ]
    
    for user_data in mock_users:
        user = User(
            email=user_data['email'],
            role=user_data['role'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        user.set_password(user_data['password'])
        db.session.add(user)
    
    db.session.commit()
    print("Mock users created successfully")

def init_database():
    """Initialize database tables and mock data"""
    try:
        print(f"[INIT] Initializing database with URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()
        create_mock_users()
        print("[INIT] Database tables created successfully")
    except Exception as e:
        print(f"[INIT] Error creating database tables: {e}")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    print("[HEALTH] Health check requested")
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/test-auth', methods=['GET'])
def test_auth():
    """Test endpoint to check if requests are reaching the server"""
    print("[TEST-AUTH] Test auth endpoint called")
    print(f"[TEST-AUTH] Headers: {dict(request.headers)}")
    auth_header = request.headers.get('Authorization')
    if auth_header:
        print(f"[TEST-AUTH] Authorization header present: {auth_header[:50]}...")
        return jsonify({'message': 'Authorization header received', 'has_token': True})
    else:
        print("[TEST-AUTH] No Authorization header found")
        return jsonify({'message': 'No authorization header', 'has_token': False})

@app.route('/api/data-source-status', methods=['GET'])
def data_source_status():
    """Check what data source is currently being used"""
    print("[DATA-SOURCE] Checking data source status")
    try:
        from services.google_ads_real import get_real_google_ads_data
        test_data = get_real_google_ads_data()
        data_source = test_data.get('data_source', 'unknown')
        
        return jsonify({
            'google_ads_api_enabled': data_source == 'google_ads_api',
            'current_source': data_source,
            'message': 'Real Google Ads API' if data_source == 'google_ads_api' else 'Mock data (API not enabled)',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        print(f"[DATA-SOURCE] Error checking data source: {e}")
        return jsonify({
            'google_ads_api_enabled': False,
            'current_source': 'mock_data',
            'message': f'Using mock data - Error: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        })

@app.route('/api/login', methods=['POST'])
def login():
    """
    User authentication endpoint
    Expected JSON: {"email": "user@example.com", "password": "password"}
    """
    try:
        data = request.get_json()
        print(f"[LOGIN] Received login request: {data}")
        
        if not data or not data.get('email') or not data.get('password'):
            print("[LOGIN] Missing email or password")
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data.get('email').lower().strip()
        password = data.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Create access token
        print(f"[LOGIN] Creating JWT token for user: {user.email} (role: {user.role}, id: {user.id})")
        access_token = create_access_token(
            identity=str(user.id),  # Convert to string for JWT subject
            additional_claims={
                'role': user.role,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        )
        print(f"[LOGIN] JWT token created successfully")
        
        print(f"[LOGIN] Login successful for {user.email}")
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict(),
            'expires_in': app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
        }), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/kpi-data', methods=['GET'])
@jwt_required()
def get_kpi_data():
    """
    Protected endpoint to fetch KPI data based on user role
    Requires valid JWT token in Authorization header
    """
    try:
        print(f"[KPI-DATA] Received KPI data request")
        print(f"[KPI-DATA] Request headers: {dict(request.headers)}")
        auth_header = request.headers.get('Authorization')
        print(f"[KPI-DATA] Authorization header: {auth_header[:50] + '...' if auth_header and len(auth_header) > 50 else auth_header}")
        
        # Get current user identity from JWT
        current_user_id = get_jwt_identity()
        print(f"[KPI-DATA] JWT user ID (string): {current_user_id}")
        # Convert string back to integer for database query
        user_id_int = int(current_user_id)
        print(f"[KPI-DATA] JWT user ID (int): {user_id_int}")
        user = User.query.get(user_id_int)
        print(f"[KPI-DATA] Found user: {user.email if user else 'None'} (role: {user.role if user else 'None'})")
        
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 404
        
        # Get query parameters
        force_refresh = request.args.get('force_refresh', 'false').lower() == 'true'
        
        if force_refresh:
            clear_cache()
        
        # Fetch data based on user role
        print(f"[KPI-DATA] Fetching data for user role: {user.role}")
        kpi_data = get_combined_kpi_data(user.role)
        
        # Print the fetched data to console
        print(f"[KPI-DATA] ===== FETCHED DATA SUMMARY =====")
        print(f"[KPI-DATA] User Role: {user.role}")
        print(f"[KPI-DATA] Data Source (Google Ads): {kpi_data.get('google_ads', {}).get('data_source', 'unknown')}")
        print(f"[KPI-DATA] Google Ads - Total Spend: ${kpi_data.get('google_ads', {}).get('total_spend', 0)}")
        print(f"[KPI-DATA] Google Ads - Total Impressions: {kpi_data.get('google_ads', {}).get('total_impressions', 0):,}")
        print(f"[KPI-DATA] Google Ads - Total Clicks: {kpi_data.get('google_ads', {}).get('total_clicks', 0):,}")
        print(f"[KPI-DATA] Google Ads - Total Conversions: {kpi_data.get('google_ads', {}).get('total_conversions', 0)}")
        print(f"[KPI-DATA] Google Ads - CTR: {kpi_data.get('google_ads', {}).get('ctr', 0)}%")
        print(f"[KPI-DATA] Google Ads - Campaigns Count: {len(kpi_data.get('google_ads', {}).get('campaigns', []))}")
        
        if kpi_data.get('google_ads', {}).get('campaigns'):
            print(f"[KPI-DATA] Campaign Details:")
            for campaign in kpi_data.get('google_ads', {}).get('campaigns', []):
                print(f"[KPI-DATA]   - {campaign.get('name', 'Unknown')}: ${campaign.get('cost', 0):.2f} spend, {campaign.get('clicks', 0)} clicks")
        
        print(f"[KPI-DATA] Google Analytics - Sessions: {kpi_data.get('google_analytics', {}).get('total_sessions', 0):,}")
        print(f"[KPI-DATA] Google Analytics - Revenue: ${kpi_data.get('google_analytics', {}).get('revenue', 0):.2f}")
        print(f"[KPI-DATA] Key Metrics: {list(kpi_data.get('key_metrics', {}).keys())}")
        print(f"[KPI-DATA] ===== END DATA SUMMARY =====")
        
        # Add user context to response
        response_data = {
            'success': True,
            'user_role': user.role,
            'user_name': f"{user.first_name} {user.last_name}",
            'data': kpi_data,
            'cache_stats': get_cache_stats()
        }
        
        print(f"[KPI-DATA] ===== RESPONSE DATA =====")
        print(f"[KPI-DATA] Response Success: {response_data['success']}")
        print(f"[KPI-DATA] Response User: {response_data['user_name']} ({response_data['user_role']})")
        print(f"[KPI-DATA] Response Data Keys: {list(response_data['data'].keys())}")
        print(f"[KPI-DATA] Cache Stats: {response_data['cache_stats']}")
        print(f"[KPI-DATA] ===== END RESPONSE DATA =====")
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"KPI data fetch error: {e}")
        return jsonify({'error': 'Failed to fetch KPI data'}), 500

@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Get current user's profile information"""
    try:
        current_user_id = get_jwt_identity()
        user_id_int = int(current_user_id)  # Convert string to int
        user = User.query.get(user_id_int)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Profile fetch error: {e}")
        return jsonify({'error': 'Failed to fetch profile'}), 500

@app.route('/api/cache/clear', methods=['POST'])
@jwt_required()
def clear_data_cache():
    """Clear data cache (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        user_id_int = int(current_user_id)  # Convert string to int
        user = User.query.get(user_id_int)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        clear_cache()
        
        return jsonify({
            'success': True,
            'message': 'Cache cleared successfully'
        }), 200
        
    except Exception as e:
        print(f"Cache clear error: {e}")
        return jsonify({'error': 'Failed to clear cache'}), 500

@app.route('/api/cache/stats', methods=['GET'])
@jwt_required()
def get_cache_statistics():
    """Get cache statistics (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        user_id_int = int(current_user_id)  # Convert string to int
        user = User.query.get(user_id_int)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        stats = get_cache_stats()
        
        return jsonify({
            'success': True,
            'cache_stats': stats
        }), 200
        
    except Exception as e:
        print(f"Cache stats error: {e}")
        return jsonify({'error': 'Failed to fetch cache stats'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(422)
def unprocessable_entity(error):
    """Handle JWT errors"""
    print(f"[JWT-ERROR] JWT token validation failed: {error}")
    return jsonify({'error': 'Invalid token'}), 422

if __name__ == '__main__':
    # For development only
    with app.app_context():
        try:
            init_database()
            print("Application initialized successfully")
            print("\nMock Users for Testing:")
            print("Admin: admin@company.com / admin123")
            print("Marketing: marketing@company.com / marketing123")
            print("Finance: finance@company.com / finance123")
        except Exception as e:
            print(f"Initialization error: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)