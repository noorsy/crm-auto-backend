# CRM Auto Backend API

## Overview

This is a comprehensive Customer Relationship Management (CRM) backend API built with Flask, specifically designed for loan collection and customer interaction management in call centers. The system manages customer profiles, loan details, payment tracking, and customer interactions with features optimized for auto-deployment on Replit. The application provides pre-call customer data retrieval and post-call outcome tracking to support call center operations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask**: Core web framework with RESTful API design
- **Flask-SQLAlchemy**: ORM for database operations with support for multiple database types
- **Flask-CORS**: Cross-origin resource sharing for frontend integration
- **Flask-JWT-Extended**: Authentication and authorization system
- **Flask-Migrate**: Database migration management

### Database Architecture
- **Multi-database Support**: SQLite for development, PostgreSQL for production
- **Automatic Environment Detection**: Detects Replit, Heroku, Vercel environments
- **Three Core Tables**:
  - `customer`: Personal information, contact details, financial data, call eligibility
  - `loan`: Product details, payment status, due dates, collection status
  - `customer_interaction`: Call logs, agent notes, disposition tracking

### API Design
- **RESTful Endpoints**: Standard CRUD operations for customers, loans, interactions
- **CRM-Specific Endpoints**: 
  - Pre-call customer profile retrieval by phone number
  - Post-call outcome recording
  - Comprehensive customer data aggregation
- **Error Handling**: Structured error responses with appropriate HTTP status codes
- **Request Logging**: Built-in request/response logging for debugging

### Database Management System
- **CLI Tool**: Custom database manager with commands for initialization, seeding, status checks
- **Auto-Migration**: Automatic table creation and schema updates
- **Sample Data**: Pre-populated customer, loan, and interaction data for testing

### Deployment Architecture
- **Replit-Optimized**: Zero-configuration deployment with automatic setup
- **GitHub Integration**: Version control with manual and webhook-based sync options
- **Environment Auto-Detection**: Automatic configuration for different hosting platforms
- **Health Monitoring**: Built-in health check endpoints for system status

## External Dependencies

### Core Python Packages
- **flask==3.1.2**: Web framework
- **flask-sqlalchemy==3.1.1**: Database ORM
- **psycopg2-binary==2.9.7**: PostgreSQL adapter for production use
- **gunicorn==21.2.0**: WSGI HTTP Server for production deployment
- **python-dotenv==1.1.1**: Environment variable management

### Authentication & Security
- **flask-jwt-extended==4.6.0**: JWT token management
- **bcrypt==4.2.1**: Password hashing
- **email-validator==2.2.0**: Email validation utilities

### Data Serialization
- **marshmallow==3.22.0**: Object serialization/deserialization
- **flask-marshmallow==1.2.1**: Flask integration for Marshmallow
- **marshmallow-sqlalchemy==1.1.0**: SQLAlchemy integration

### Hosting Platforms
- **Primary**: Replit (auto-deployment, zero configuration)
- **Production Ready**: Heroku, Vercel support via environment detection
- **Database Services**: PostgreSQL for production, SQLite for development

### Development Tools
- **click==8.1.7**: CLI framework for database management commands
- **requests==2.31.0**: HTTP library for external API calls and testing
- **flask-migrate==4.0.5**: Database schema migration management