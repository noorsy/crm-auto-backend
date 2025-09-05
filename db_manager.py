#!/usr/bin/env python3
"""
Database Management Utility for CRM Auto Backend
Handles database operations, migrations, and maintenance
"""

import os
import sys
import click
from datetime import datetime
from app import app, db, Customer, Loan, CustomerInteraction
from database_config import DatabaseConfig

@click.group()
def cli():
    """CRM Auto Database Management CLI"""
    pass

@cli.command()
def init():
    """Initialize the database with tables"""
    with app.app_context():
        try:
            db.create_all()
            click.echo("✅ Database tables created successfully!")
            
            # Show database info
            db_info = DatabaseConfig.get_database_info()
            click.echo(f"📊 Database Type: {db_info['type']}")
            click.echo(f"📝 Description: {db_info['description']}")
            
        except Exception as e:
            click.echo(f"❌ Error creating tables: {e}")
            sys.exit(1)

@cli.command()
def seed():
    """Populate database with sample data"""
    with app.app_context():
        try:
            # Check if data already exists
            if Customer.query.count() > 0:
                if not click.confirm(f"Database has {Customer.query.count()} customers. Overwrite?"):
                    click.echo("❌ Seed operation cancelled")
                    return
                
                # Clear existing data
                CustomerInteraction.query.delete()
                Loan.query.delete()
                Customer.query.delete()
                db.session.commit()
                click.echo("🗑️ Existing data cleared")
            
            # Run the comprehensive database initialization
            import subprocess
            result = subprocess.run(['python', 'init_comprehensive_db.py'], 
                                  capture_output=True, text=True, cwd='.')
            
            if result.returncode == 0:
                click.echo("✅ Database seeded with sample data!")
                click.echo(f"📊 Created {Customer.query.count()} customers")
                click.echo(f"💰 Created {Loan.query.count()} loans")
                click.echo(f"📞 Created {CustomerInteraction.query.count()} interactions")
            else:
                click.echo(f"❌ Seed failed: {result.stderr}")
                
        except Exception as e:
            click.echo(f"❌ Error seeding database: {e}")

@cli.command()
def status():
    """Show database status and statistics"""
    with app.app_context():
        try:
            db_info = DatabaseConfig.get_database_info()
            
            click.echo("🗄️ Database Status")
            click.echo("=" * 50)
            click.echo(f"Type: {db_info['type']}")
            click.echo(f"Description: {db_info['description']}")
            click.echo(f"URI: {DatabaseConfig.get_database_uri()}")
            click.echo(f"Suitable for: {db_info['suitable_for']}")
            click.echo()
            
            click.echo("📊 Data Statistics")
            click.echo("-" * 20)
            click.echo(f"Customers: {Customer.query.count()}")
            click.echo(f"Loans: {Loan.query.count()}")
            click.echo(f"Interactions: {CustomerInteraction.query.count()}")
            click.echo()
            
            # Show recent activity
            recent_customers = Customer.query.order_by(Customer.created_at.desc()).limit(3).all()
            if recent_customers:
                click.echo("🕒 Recent Customers")
                click.echo("-" * 20)
                for customer in recent_customers:
                    created = customer.created_at.strftime("%Y-%m-%d %H:%M") if customer.created_at else "Unknown"
                    click.echo(f"• {customer.first_name} {customer.last_name} ({created})")
            
        except Exception as e:
            click.echo(f"❌ Error getting database status: {e}")

@cli.command()
def backup():
    """Create a backup of the database (SQLite only)"""
    with app.app_context():
        try:
            db_uri = DatabaseConfig.get_database_uri()
            
            if 'sqlite' not in db_uri:
                click.echo("❌ Backup only supports SQLite databases")
                return
            
            # Extract database file path
            db_path = db_uri.replace('sqlite:///', '')
            if not os.path.exists(db_path):
                click.echo(f"❌ Database file not found: {db_path}")
                return
            
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_crm_{timestamp}.db"
            
            import shutil
            shutil.copy2(db_path, backup_path)
            
            click.echo(f"✅ Database backed up to: {backup_path}")
            click.echo(f"📁 Backup size: {os.path.getsize(backup_path)} bytes")
            
        except Exception as e:
            click.echo(f"❌ Error creating backup: {e}")

@cli.command()
def reset():
    """Reset database (drop all tables and recreate)"""
    if not click.confirm("⚠️ This will delete ALL data. Are you sure?"):
        click.echo("❌ Reset operation cancelled")
        return
    
    with app.app_context():
        try:
            click.echo("🗑️ Dropping all tables...")
            db.drop_all()
            
            click.echo("🔨 Creating tables...")
            db.create_all()
            
            click.echo("✅ Database reset complete!")
            
            if click.confirm("🌱 Would you like to seed with sample data?"):
                # Run seed command
                ctx = click.get_current_context()
                ctx.invoke(seed)
                
        except Exception as e:
            click.echo(f"❌ Error resetting database: {e}")

@cli.command()
@click.argument('query')
def query(query):
    """Execute a custom SQL query (read-only for safety)"""
    with app.app_context():
        try:
            # Only allow SELECT queries for safety
            if not query.strip().upper().startswith('SELECT'):
                click.echo("❌ Only SELECT queries are allowed for safety")
                return
            
            result = db.session.execute(query)
            rows = result.fetchall()
            
            if not rows:
                click.echo("🔍 No results found")
                return
            
            # Display results
            click.echo(f"📊 Found {len(rows)} results:")
            click.echo("-" * 50)
            
            for i, row in enumerate(rows, 1):
                click.echo(f"{i}: {dict(row)}")
                if i >= 10:  # Limit output
                    click.echo(f"... and {len(rows) - 10} more rows")
                    break
                    
        except Exception as e:
            click.echo(f"❌ Query error: {e}")

@cli.command()
def migrate():
    """Run database migrations (if using Flask-Migrate)"""
    with app.app_context():
        try:
            # Check if migrations directory exists
            if not os.path.exists('migrations'):
                click.echo("📁 Initializing migrations...")
                from flask_migrate import init
                init()
                
            click.echo("🔄 Running migrations...")
            from flask_migrate import upgrade
            upgrade()
            
            click.echo("✅ Migrations completed!")
            
        except ImportError:
            click.echo("❌ Flask-Migrate not available. Using basic table creation.")
            ctx = click.get_current_context()
            ctx.invoke(init)
        except Exception as e:
            click.echo(f"❌ Migration error: {e}")

@cli.command()
def info():
    """Show comprehensive database information"""
    with app.app_context():
        try:
            click.echo("🏗️ CRM Auto Database Information")
            click.echo("=" * 60)
            
            # Database configuration
            db_info = DatabaseConfig.get_database_info()
            click.echo(f"Type: {db_info['type']}")
            click.echo(f"Description: {db_info['description']}")
            click.echo(f"Features: {', '.join(db_info['features'])}")
            click.echo(f"Best for: {db_info['suitable_for']}")
            click.echo()
            
            # Connection info
            click.echo("🔗 Connection Details")
            click.echo("-" * 30)
            db_uri = DatabaseConfig.get_database_uri()
            # Hide sensitive info in URI
            safe_uri = db_uri.split('://')[0] + '://***' if '://' in db_uri else db_uri
            click.echo(f"URI: {safe_uri}")
            click.echo()
            
            # Table information
            click.echo("📋 Table Structure")
            click.echo("-" * 30)
            
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            for table in tables:
                columns = inspector.get_columns(table)
                click.echo(f"• {table} ({len(columns)} columns)")
                
                # Count records
                try:
                    count = db.session.execute(f"SELECT COUNT(*) FROM {table}").scalar()
                    click.echo(f"  Records: {count}")
                except:
                    click.echo(f"  Records: Unable to count")
            
        except Exception as e:
            click.echo(f"❌ Error getting database info: {e}")

if __name__ == '__main__':
    cli() 