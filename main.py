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
            
            # Check if we need to populate with dummy data
            from app import Customer, Loan, CustomerInteraction
            if Customer.query.count() == 0:
                print("📝 No customers found, running initialization...")
                # Import and run the database initialization
                try:
                    import subprocess
                    result = subprocess.run(['python', 'init_comprehensive_db.py'], 
                                          capture_output=True, text=True, cwd='.')
                    if result.returncode == 0:
                        print("✅ Database initialized with dummy data!")
                    else:
                        print(f"⚠️ Database initialization warning: {result.stderr}")
                except Exception as e:
                    print(f"⚠️ Could not run database initialization: {e}")
                    print("You can manually run 'python init_comprehensive_db.py' later")
            else:
                print(f"📊 Found {Customer.query.count()} customers in database")
                
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
    port = int(os.environ.get('PORT', 5000))  # Use PORT env var if available
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🌐 Starting server on {host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    # Run the Flask application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True  # Enable threading for better performance
    ) 