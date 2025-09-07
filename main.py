#!/usr/bin/env python3
"""
Main entry point for the CRM Auto Backend API
Optimized for Replit deployment
"""

import os
from app import app, db

def create_tables():
    """Create database tables if they don't exist"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check customer count
            from app import Customer, Loan, CustomerInteraction
            customer_count = Customer.query.count()
            print(f"📊 Found {customer_count} customers in database")
            if customer_count == 0:
                print("📝 No customers found. You can create customers via the API.")
                
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")

if __name__ == '__main__':
    # Set up environment for Replit
    os.environ.setdefault('FLASK_ENV', 'production')
    
    print("🚀 Starting CRM Auto Backend API...")
    print("📍 API Documentation:")
    print("   - GET /api/customers - List all customers")
    print("   - GET /api/loans - List all loans") 
    print("   - GET /api/fetch_user_profile_pre_call/?caller_number=<number> - Get customer profile")
    print("   - POST /api/post_call_outcomes/ - Update call outcomes")
    print("   - Full API examples in API_EXAMPLES.md")
    
    # Create database tables
    create_tables()
    
    # Configure for Replit deployment
    host = '0.0.0.0'  # Allow external connections
    port = 5000  # Default to port 5000
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    # Special handling for Replit environment
    if os.environ.get('REPL_SLUG'):
        print(f"🔧 Detected Replit environment: {os.environ.get('REPL_SLUG')}")
        print(f"🌍 Your API will be available at: https://{os.environ.get('REPL_SLUG')}.{os.environ.get('REPL_OWNER', 'your-username')}.repl.co")
    
    print(f"🌐 Starting server on {host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    try:
        # Run the Flask application
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True  # Enable threading for better performance
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("💡 If you're on Replit, make sure the port is configured correctly")
        print("💡 Try restarting the Repl if issues persist") 