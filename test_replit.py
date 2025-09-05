#!/usr/bin/env python3
"""
Quick test script to verify CRM Auto Backend works on Replit
Run this to ensure everything is functioning correctly
"""

import os
import sys
import requests
import time

def test_replit_deployment():
    """Test the deployment on Replit"""
    
    print("🧪 Testing CRM Auto Backend on Replit")
    print("=" * 50)
    
    # Determine base URL
    if os.getenv('REPL_SLUG') and os.getenv('REPL_OWNER'):
        base_url = f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co"
    else:
        base_url = "http://localhost:5000"
    
    print(f"🌐 Testing URL: {base_url}")
    print()
    
    tests = [
        {
            'name': 'Root Endpoint',
            'url': f'{base_url}/',
            'method': 'GET',
            'expected_keys': ['message', 'description', 'version']
        },
        {
            'name': 'Health Check',
            'url': f'{base_url}/health',
            'method': 'GET',
            'expected_keys': ['status', 'message', 'database']
        },
        {
            'name': 'API Health Check',
            'url': f'{base_url}/api/health',
            'method': 'GET',
            'expected_keys': ['status', 'database', 'endpoints']
        },
        {
            'name': 'Customers API',
            'url': f'{base_url}/api/customers',
            'method': 'GET',
            'expected_type': list
        },
        {
            'name': 'Loans API',
            'url': f'{base_url}/api/loans',
            'method': 'GET',
            'expected_type': list
        },
        {
            'name': 'Pre-Call Profile',
            'url': f'{base_url}/api/fetch_user_profile_pre_call/?caller_number=5551234567',
            'method': 'GET',
            'expected_keys': ['caller_details', 'status', 'success']
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        print(f"🔍 Testing {test['name']}...")
        
        try:
            response = requests.get(test['url'], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check expected keys
                if 'expected_keys' in test:
                    missing_keys = [key for key in test['expected_keys'] if key not in data]
                    if missing_keys:
                        print(f"❌ Missing keys: {missing_keys}")
                        failed += 1
                        continue
                
                # Check expected type
                if 'expected_type' in test:
                    if not isinstance(data, test['expected_type']):
                        print(f"❌ Expected {test['expected_type']}, got {type(data)}")
                        failed += 1
                        continue
                
                print(f"✅ {test['name']} - OK")
                passed += 1
                
            else:
                print(f"❌ {test['name']} - HTTP {response.status_code}")
                failed += 1
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {test['name']} - Connection failed (server may not be running)")
            failed += 1
        except requests.exceptions.Timeout:
            print(f"❌ {test['name']} - Request timeout")
            failed += 1
        except Exception as e:
            print(f"❌ {test['name']} - Error: {e}")
            failed += 1
    
    print()
    print("📊 Test Results")
    print("-" * 20)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print()
        print("🎉 All tests passed! Your Replit deployment is working perfectly!")
        print(f"🌍 Your API is live at: {base_url}")
        print()
        print("📋 Quick API Examples:")
        print(f"   curl {base_url}/health")
        print(f"   curl {base_url}/api/customers")
        print(f"   curl \"{base_url}/api/fetch_user_profile_pre_call/?caller_number=5551234567\"")
    else:
        print()
        print("⚠️ Some tests failed. Check the server logs for more details.")
        
    return failed == 0

def test_database():
    """Test database functionality"""
    print("\n🗄️ Testing Database")
    print("-" * 20)
    
    try:
        from app import app, Customer, Loan, CustomerInteraction
        
        with app.app_context():
            customer_count = Customer.query.count()
            loan_count = Loan.query.count()
            interaction_count = CustomerInteraction.query.count()
            
            print(f"📊 Customers: {customer_count}")
            print(f"💰 Loans: {loan_count}")
            print(f"📞 Interactions: {interaction_count}")
            
            if customer_count >= 5:
                print("✅ Sample data is present")
                return True
            else:
                print("⚠️ Sample data missing - run 'python db_manager.py seed'")
                return False
                
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 CRM Auto Backend - Replit Verification")
    print("=" * 60)
    
    # Test database first
    db_ok = test_database()
    
    # Wait a moment for server to be ready
    print("\n⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Test API endpoints
    api_ok = test_replit_deployment()
    
    print("\n" + "=" * 60)
    if db_ok and api_ok:
        print("🎉 SUCCESS: Your CRM Auto Backend is ready for production!")
        print("📝 You can now:")
        print("   - Share your Replit URL with others")
        print("   - Connect your frontend to this backend")
        print("   - Start using the API for call center operations")
    else:
        print("❌ ISSUES DETECTED: Please check the logs above")
        print("💡 Try restarting the Repl or running 'python db_manager.py reset'")

if __name__ == '__main__':
    main() 