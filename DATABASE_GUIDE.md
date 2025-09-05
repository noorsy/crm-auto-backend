# 🗄️ Database Management Guide

Comprehensive guide for managing the CRM Auto Backend database across different environments.

## 📋 Current Database Setup

### **Database Type**: SQLite (Development) + PostgreSQL (Production Ready)

Our application is designed to work with multiple database types:

| Environment | Database | Configuration |
|-------------|----------|---------------|
| **Local Development** | SQLite | `sqlite:///crm.db` (file-based) |
| **Replit Deployment** | SQLite | Auto-created, self-contained |
| **Production** | PostgreSQL | Via `DATABASE_URL` environment variable |

## 🏗️ Database Schema

### **Core Tables:**

1. **`customer`** - Customer information
   - Personal details (name, DOB, SSN, address)
   - Contact information (email, phone)
   - Financial info (credit score, income)
   - Call eligibility status

2. **`loan`** - Loan management
   - Product details and amounts
   - Payment status and history
   - Due dates and installments
   - Collection status

3. **`customer_interaction`** - Call center interactions
   - Call logs and outcomes
   - Agent notes and disposition
   - Timestamps and follow-up dates

## 🛠️ Database Management Commands

We've created a powerful CLI tool for database management:

### **Basic Commands:**

```bash
# Initialize database tables
python db_manager.py init

# Check database status
python db_manager.py status

# Populate with sample data
python db_manager.py seed

# Get comprehensive database info
python db_manager.py info
```

### **Maintenance Commands:**

```bash
# Create backup (SQLite only)
python db_manager.py backup

# Reset database (careful!)
python db_manager.py reset

# Run custom queries
python db_manager.py query "SELECT COUNT(*) FROM customer"
```

## 🔄 Environment-Specific Configurations

### **1. Local Development (SQLite)**

**Pros:**
- ✅ No setup required
- ✅ File-based, easy to backup
- ✅ Perfect for development and testing
- ✅ No external dependencies

**Cons:**
- ❌ Limited concurrent users
- ❌ No advanced features

**Configuration:**
```python
# Automatic - no setup needed
DATABASE_URL = "sqlite:///crm.db"
```

### **2. Replit Deployment (SQLite)**

**Current Setup:**
- Database auto-created on first run
- Sample data automatically populated
- Self-contained and ready to use

**Benefits:**
- ✅ Zero configuration
- ✅ Immediate deployment
- ✅ Perfect for demos and prototypes

**Limitations:**
- ⚠️ Data may reset on container restarts
- ⚠️ Single user at a time
- ⚠️ No backup/restore built-in

### **3. Production (PostgreSQL) - Ready to Upgrade**

**When to Upgrade:**
- Multiple concurrent users
- Need for data persistence
- Production workloads
- Advanced database features

**Setup Options:**

#### **Option A: Neon (Recommended - Free Tier)**
```bash
# 1. Sign up at neon.tech
# 2. Create a database
# 3. Get connection string
# 4. Set environment variable in Replit:
DATABASE_URL=postgresql://user:password@host:5432/database
```

#### **Option B: Supabase**
```bash
# 1. Sign up at supabase.com
# 2. Create project
# 3. Get PostgreSQL connection string
# 4. Set in Replit Secrets:
DATABASE_URL=postgresql://postgres:password@host:5432/postgres
```

#### **Option C: Railway**
```bash
# 1. Sign up at railway.app
# 2. Add PostgreSQL service
# 3. Use provided DATABASE_URL
```

## 🚀 Deployment Scenarios

### **Scenario 1: Quick Demo/Prototype (Current)**
```
✅ Use SQLite on Replit
✅ Auto-initialization
✅ Sample data included
✅ Zero configuration
```

### **Scenario 2: Production Deployment**
```bash
# 1. Set up PostgreSQL database (Neon/Supabase)
# 2. Configure environment variable
DATABASE_URL=postgresql://...

# 3. Deploy to Replit
# 4. Database auto-migrates to PostgreSQL
# 5. Run seed command if needed
```

### **Scenario 3: Development to Production**
```bash
# Local development (SQLite)
python db_manager.py status
python db_manager.py backup  # Save current data

# Production setup
export DATABASE_URL="postgresql://..."
python db_manager.py init
python db_manager.py seed  # or import real data
```

## 📊 Database Monitoring

### **Check Database Health:**
```bash
# Quick status
python db_manager.py status

# Detailed information
python db_manager.py info

# Check recent activity
python db_manager.py query "SELECT * FROM customer ORDER BY created_at DESC LIMIT 5"
```

### **Monitor via API:**
```bash
# Test database connectivity
curl https://your-app.repl.co/api/customers

# Check specific customer
curl "https://your-app.repl.co/api/fetch_user_profile_pre_call/?caller_number=5551234567"
```

## 🔧 Troubleshooting

### **Issue: Database not initializing**

**Solution:**
```bash
# Check status
python db_manager.py status

# Reinitialize if needed
python db_manager.py reset
python db_manager.py seed
```

### **Issue: Connection errors in production**

**Solution:**
```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Test connection
python db_manager.py info

# Verify PostgreSQL accessibility
```

### **Issue: Data loss on Replit**

**Solution:**
```bash
# Create regular backups
python db_manager.py backup

# Or upgrade to PostgreSQL for persistence
```

## 🔄 Migration Strategies

### **SQLite to PostgreSQL Migration:**

```bash
# 1. Backup current SQLite data
python db_manager.py backup

# 2. Export data (create a script)
python -c "
from app import *
import json
with app.app_context():
    customers = [{'id': c.id, 'name': c.first_name + ' ' + c.last_name} for c in Customer.query.all()]
    with open('export.json', 'w') as f:
        json.dump(customers, f)
"

# 3. Set PostgreSQL URL
export DATABASE_URL="postgresql://..."

# 4. Initialize new database
python db_manager.py init

# 5. Import data (create import script)
```

## 📈 Performance Considerations

### **SQLite Limitations:**
- Max ~1000 concurrent reads
- Single writer at a time
- File locking issues possible
- No built-in replication

### **PostgreSQL Benefits:**
- Unlimited concurrent connections
- ACID compliance
- Advanced indexing
- Built-in backup/restore
- Horizontal scaling options

## 🔐 Security Best Practices

### **Environment Variables:**
```bash
# Production secrets (set in Replit Secrets)
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://...
```

### **Database Security:**
- Use environment variables for credentials
- Enable SSL for PostgreSQL connections
- Regular backups
- Access logging (PostgreSQL)

## 📚 Quick Reference

| Task | Command |
|------|---------|
| Check status | `python db_manager.py status` |
| Initialize | `python db_manager.py init` |
| Add sample data | `python db_manager.py seed` |
| Backup | `python db_manager.py backup` |
| Reset | `python db_manager.py reset` |
| Custom query | `python db_manager.py query "SELECT ..."` |

## 🎯 Recommendations

### **For Development:**
- ✅ Keep using SQLite
- ✅ Use db_manager.py for operations
- ✅ Regular backups

### **For Production:**
- 🔄 Upgrade to PostgreSQL (Neon/Supabase)
- 🔄 Set up monitoring
- 🔄 Implement backup strategy
- 🔄 Use connection pooling

### **For Scaling:**
- 📈 Consider read replicas
- 📈 Implement caching (Redis)
- 📈 Database indexing optimization
- 📈 Connection pooling

Your database is now ready for any deployment scenario! 🚀 