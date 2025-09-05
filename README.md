# CRM Auto Backend API

A comprehensive Customer Relationship Management (CRM) backend API built with Flask, designed for loan collection and customer interaction management.

## 🚀 Quick Start on Replit

This project is **100% Replit-optimized**! Simply:

### **Method 1: GitHub Import (Recommended)**
1. Create GitHub repository with this code
2. In Replit: "Create Repl" → "Import from GitHub"
3. Paste your GitHub URL
4. Click "Run" - everything auto-configures!

### **Method 2: Direct Upload**
1. Upload all files to a new Replit Python project
2. Click "Run" - the application will automatically:
   - Install dependencies from `requirements.txt`
   - Create database tables
   - Populate with sample data
   - Start the API server

### **Auto-Features on Replit:**
- ✅ **Zero Configuration** - Works immediately
- ✅ **Auto-URL Detection** - Shows your live API URL
- ✅ **Health Checks** - Built-in monitoring endpoints
- ✅ **Sample Data** - 5 customers, loans, and interactions ready
- ✅ **CORS Enabled** - Ready for frontend integration

## 📋 API Endpoints

### Customer Management
- `GET /api/customers` - List all customers
- `GET /api/customers/{id}` - Get customer details
- `POST /api/customers` - Create new customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Loan Management
- `GET /api/loans` - List all loans
- `GET /api/loans/{id}` - Get loan details
- `POST /api/loans` - Create new loan
- `PUT /api/loans/{id}` - Update loan
- `DELETE /api/loans/{id}` - Delete loan

### Customer Interactions
- `GET /api/customers/{id}/interactions` - Get customer interactions
- `POST /api/customers/{id}/interactions` - Create new interaction

### CRM Specific Endpoints
- `GET /api/fetch_user_profile_pre_call/?caller_number={number}` - Get comprehensive customer profile
- `POST /api/post_call_outcomes/` - Update customer and loan records after call

## 📁 Project Structure

```
backend/
├── main.py                    # Main entry point for Replit
├── app.py                     # Flask application and API routes
├── requirements.txt           # Python dependencies
├── init_comprehensive_db.py   # Database initialization script
├── API_EXAMPLES.md           # Detailed API usage examples
├── .replit                   # Replit configuration
└── instance/
    └── crm.db               # SQLite database (auto-created)
```

## 🗄️ Database Schema

The system includes three main models:

1. **Customer** - Customer information (personal, contact, financial details)
2. **Loan** - Loan details (amounts, dates, status, payment info)
3. **CustomerInteraction** - Call logs and interaction history

## 🔧 Configuration

The app automatically configures itself for Replit deployment:
- Database: SQLite (file-based, perfect for Replit)
- CORS: Enabled for all origins
- Host: `0.0.0.0` (allows external connections)
- Port: Uses Replit's PORT environment variable

## 📊 Sample Data

The system comes with 5 sample customers, each with:
- Complete customer profile
- One loan with realistic payment scenarios
- Multiple interaction records showing various call outcomes

## 🌐 Frontend Integration

This backend is designed to work with the React frontend. Update the frontend's API base URL to your Replit app URL:

```javascript
const API_BASE_URL = 'https://your-replit-app-name.your-username.repl.co';
```

## 📖 API Documentation

See `API_EXAMPLES.md` for detailed curl examples and request/response formats for all endpoints.

## 🔍 Health Check

### **Quick Verification:**
```bash
# Basic health check
curl https://your-replit-app-name.your-username.repl.co/health

# Detailed API status
curl https://your-replit-app-name.your-username.repl.co/api/health

# Test customer data
curl https://your-replit-app-name.your-username.repl.co/api/customers
```

### **Built-in Test Suite:**
Run this in your Replit shell to verify everything works:
```bash
python test_replit.py
```

This will test all endpoints and confirm your deployment is working perfectly!

## 🎯 Features

- ✅ Complete CRUD operations for customers and loans
- ✅ Customer interaction tracking
- ✅ Pre-call customer profile retrieval
- ✅ Post-call outcome processing
- ✅ Automatic database initialization
- ✅ CORS enabled for frontend integration
- ✅ Production-ready configuration 