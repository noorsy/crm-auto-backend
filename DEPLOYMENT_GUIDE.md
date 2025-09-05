# 🚀 GitHub + Replit Deployment Guide

This guide shows you how to deploy your CRM Auto Backend using GitHub with automatic syncing to Replit.

## 📋 Overview

**Benefits of GitHub + Replit Integration:**
- ✅ Version control with Git
- ✅ Automatic deployment on code changes
- ✅ Easy collaboration and backup
- ✅ Professional development workflow
- ✅ Free hosting on Replit with GitHub sync

## 🎯 Step 1: Create GitHub Repository

### Option A: Using GitHub Website (Recommended)

1. **Go to GitHub.com**
   - Sign in to your GitHub account
   - Click the "+" icon → "New repository"

2. **Repository Settings**
   - Repository name: `crm-auto-backend`
   - Description: `CRM Auto Backend API - Customer and loan management system for call centers`
   - Set to **Public** (required for free Replit integration)
   - ❌ Don't initialize with README (we already have one)
   - Click "Create repository"

3. **Copy the Repository URL**
   - You'll get something like: `https://github.com/yourusername/crm-auto-backend.git`

### Option B: Using GitHub CLI (if you have it)

```bash
# Install GitHub CLI first (if not installed)
brew install gh  # macOS
# or
sudo apt install gh  # Ubuntu

# Create repository
gh repo create crm-auto-backend --public --description "CRM Auto Backend API"
```

## 🔗 Step 2: Connect Local Repository to GitHub

Run these commands in your backend directory:

```bash
# Add GitHub as remote origin
git remote add origin https://github.com/YOURUSERNAME/crm-auto-backend.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOURUSERNAME` with your actual GitHub username!**

## 🌐 Step 3: Deploy to Replit with GitHub Integration

### 3.1 Create Replit Project from GitHub

1. **Go to Replit.com**
   - Sign in to your Replit account
   - Click "Create Repl"

2. **Import from GitHub**
   - Click "Import from GitHub" tab
   - Paste your repository URL: `https://github.com/YOURUSERNAME/crm-auto-backend`
   - Click "Import from GitHub"

3. **Configure Project**
   - Language will auto-detect as Python
   - Project name will auto-populate
   - Click "Import Repl"

### 3.2 Enable Auto-Sync

1. **In your Replit project:**
   - Look for the "Version Control" panel (Git icon in sidebar)
   - Click "Connect to GitHub" if not already connected
   - Enable "Auto-sync" or "Auto-pull"

2. **Set up Auto-Deploy:**
   - Go to your Replit project settings
   - Enable "Always On" (optional, for 24/7 uptime)
   - The project will auto-restart when GitHub changes are detected

## ▶️ Step 4: Run and Test

1. **Click "Run" in Replit**
   - Dependencies will install automatically
   - Database will be created and populated
   - API server will start

2. **Get Your API URL**
   ```
   https://your-repl-name.your-username.repl.co
   ```

3. **Test the API**
   ```bash
   # Test customers endpoint
   curl https://your-repl-name.your-username.repl.co/api/customers
   
   # Test pre-call endpoint
   curl "https://your-repl-name.your-username.repl.co/api/fetch_user_profile_pre_call/?caller_number=5551234567"
   ```

## 🔄 Step 5: Automatic Updates Workflow

Now you have automatic deployment! Here's how it works:

### Making Updates Locally

```bash
# Make your code changes
# Then commit and push to GitHub

git add .
git commit -m "Add new feature: XYZ"
git push origin main
```

### Automatic Replit Deployment

1. **Replit detects the GitHub push**
2. **Automatically pulls the latest code**
3. **Restarts the application**
4. **Your changes are live!** ✨

## 🛠️ Development Workflow Examples

### Adding a New Feature

```bash
# 1. Make changes to your code locally
# 2. Test locally if needed
# 3. Commit and push

git add .
git commit -m "feat: Add customer search by phone number"
git push origin main

# 4. Replit automatically deploys the changes!
```

### Bug Fixes

```bash
git add .
git commit -m "fix: Resolve date formatting issue in interactions"
git push origin main
```

### Database Schema Updates

```bash
# Update your models in app.py
# Update init_comprehensive_db.py if needed

git add .
git commit -m "schema: Add new customer field for preferred contact time"
git push origin main
```

## 📱 Step 6: Connect Frontend

Once your backend is deployed, update your frontend's API URL:

**In your frontend `src/context/ApiContext.js`:**

```javascript
// Replace this line:
const API_BASE_URL = 'http://localhost:5000/api';

// With your Replit URL:
const API_BASE_URL = 'https://your-repl-name.your-username.repl.co/api';
```

## 🎛️ Environment Variables (Optional)

For production secrets, use Replit's environment variables:

1. **In Replit, go to "Secrets" tab**
2. **Add environment variables:**
   - `SECRET_KEY`: Your Flask secret key
   - `JWT_SECRET_KEY`: Your JWT secret
   - `DATABASE_URL`: Custom database URL (optional)

3. **These will override the defaults in your code**

## 📊 Monitoring Your Deployment

### Check Deployment Status

1. **Replit Console**: View real-time logs
2. **GitHub Actions**: See commit history and auto-deployments
3. **API Health Check**: Monitor uptime

### Common Commands

```bash
# Check git status
git status

# View commit history
git log --oneline

# Force update Replit (if auto-sync fails)
# Go to Replit → Version Control → Pull from GitHub
```

## 🔧 Troubleshooting

### Issue: Replit not updating automatically

**Solution:**
1. Go to Replit → Version Control panel
2. Click "Pull from GitHub" manually
3. Check if auto-sync is enabled in settings

### Issue: Import errors in Replit

**Solution:**
1. Check that `requirements.txt` is properly formatted
2. Click "Shell" in Replit and run: `pip install -r requirements.txt`
3. Restart the Repl

### Issue: Database not initializing

**Solution:**
1. Check Replit console for error messages
2. Delete the `instance/` folder in Replit
3. Restart the application

## 🎉 You're All Set!

Your CRM Auto Backend is now:
- ✅ Version controlled with Git
- ✅ Hosted on GitHub
- ✅ Auto-deployed to Replit
- ✅ Ready for continuous development

**Next Steps:**
1. Deploy your frontend using the same GitHub + hosting approach
2. Update frontend API URLs to point to your Replit backend
3. Start developing new features with automatic deployment!

## 📚 Quick Reference

| Action | Command |
|--------|---------|
| Add changes | `git add .` |
| Commit | `git commit -m "message"` |
| Deploy | `git push origin main` |
| Check status | `git status` |
| View logs | Check Replit console |

**Your API Base URL:** `https://your-repl-name.your-username.repl.co/api`

Happy coding! 🚀 