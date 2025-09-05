# CRM Auto Backend API

A comprehensive Customer Relationship Management (CRM) backend API built with Flask, designed for loan collection and customer interaction management.

## 🚀 Quick Start on Replit

This project is ready to deploy on Replit! Simply:

1. Upload all files to a new Replit Python project
2. Click "Run" - the application will automatically:
   - Install dependencies from `requirements.txt`
   - Create database tables
   - Populate with sample data
   - Start the API server

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

Once deployed, verify the API is working:
```bash
curl https://your-replit-app-name.your-username.repl.co/api/customers
```

## 🎯 Features

- ✅ Complete CRUD operations for customers and loans
- ✅ Customer interaction tracking
- ✅ Pre-call customer profile retrieval
- ✅ Post-call outcome processing
- ✅ Automatic database initialization
- ✅ CORS enabled for frontend integration
- ✅ Production-ready configuration 