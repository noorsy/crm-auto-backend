"""
Database Configuration for CRM Auto Backend
Supports multiple database types for different environments
"""

import os
from urllib.parse import urlparse

class DatabaseConfig:
    """Database configuration class with support for multiple database types"""
    
    @staticmethod
    def get_database_uri():
        """
        Get database URI based on environment variables
        Priority: DATABASE_URL > Environment detection > SQLite default
        """
        
        # Check for explicit DATABASE_URL (highest priority)
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            # Handle different database URL formats
            if database_url.startswith('postgres://'):
                # Fix for newer SQLAlchemy versions
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            return database_url
        
        # Auto-detect environment and choose appropriate database
        if os.getenv('REPLIT_DB_URL'):
            # Replit environment - use Replit Database
            return DatabaseConfig._get_replit_db_uri()
        elif os.getenv('HEROKU_APP_NAME'):
            # Heroku environment - use PostgreSQL
            return DatabaseConfig._get_heroku_db_uri()
        elif os.getenv('VERCEL_ENV'):
            # Vercel environment - use PostgreSQL
            return DatabaseConfig._get_vercel_db_uri()
        else:
            # Local development - use SQLite
            return 'sqlite:///crm.db'
    
    @staticmethod
    def _get_replit_db_uri():
        """Configure database for Replit environment"""
        replit_db_url = os.getenv('REPLIT_DB_URL')
        if replit_db_url:
            return replit_db_url
        
        # Fallback to SQLite for Replit
        return 'sqlite:///crm.db'
    
    @staticmethod
    def _get_heroku_db_uri():
        """Configure database for Heroku environment"""
        # Heroku provides DATABASE_URL automatically for PostgreSQL
        return os.getenv('DATABASE_URL', 'sqlite:///crm.db')
    
    @staticmethod
    def _get_vercel_db_uri():
        """Configure database for Vercel environment"""
        # Vercel with PostgreSQL (e.g., Neon, Supabase)
        postgres_url = os.getenv('POSTGRES_URL')
        if postgres_url:
            return postgres_url
        return 'sqlite:///crm.db'
    
    @staticmethod
    def get_database_config():
        """Get complete database configuration"""
        database_uri = DatabaseConfig.get_database_uri()
        
        config = {
            'SQLALCHEMY_DATABASE_URI': database_uri,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        }
        
        # Add database-specific configurations
        if 'postgresql' in database_uri or 'postgres' in database_uri:
            config.update({
                'SQLALCHEMY_ENGINE_OPTIONS': {
                    'pool_pre_ping': True,
                    'pool_recycle': 300,
                    'connect_args': {
                        'connect_timeout': 10,
                        'application_name': 'crm_auto_backend'
                    }
                }
            })
        elif 'sqlite' in database_uri:
            config.update({
                'SQLALCHEMY_ENGINE_OPTIONS': {
                    'connect_args': {'timeout': 20}
                }
            })
        
        return config
    
    @staticmethod
    def get_database_info():
        """Get information about the current database configuration"""
        database_uri = DatabaseConfig.get_database_uri()
        
        if 'sqlite' in database_uri:
            return {
                'type': 'SQLite',
                'description': 'File-based database (good for development)',
                'features': ['Simple setup', 'No external dependencies', 'Limited concurrency'],
                'suitable_for': 'Development, testing, low-traffic apps'
            }
        elif 'postgresql' in database_uri or 'postgres' in database_uri:
            return {
                'type': 'PostgreSQL',
                'description': 'Production-grade relational database',
                'features': ['High concurrency', 'ACID compliance', 'Advanced features'],
                'suitable_for': 'Production, high-traffic applications'
            }
        else:
            return {
                'type': 'Unknown',
                'description': 'Custom database configuration',
                'features': ['Custom setup'],
                'suitable_for': 'Custom requirements'
            }

# Environment-specific database configurations
DATABASE_CONFIGS = {
    'development': {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///crm_dev.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': True,  # Enable for debugging
    },
    'testing': {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # In-memory for tests
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    },
    'production': {
        'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL', 'sqlite:///crm.db'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,
            'pool_recycle': 300,
        }
    }
}

def get_config_by_name(config_name):
    """Get database configuration by environment name"""
    return DATABASE_CONFIGS.get(config_name, DATABASE_CONFIGS['development']) 