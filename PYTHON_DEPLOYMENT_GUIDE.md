# 🐍 Python Flask Deployment Guide for Render

## Overview

Your Signal Integrity Assessment app has been converted to Python using:
- **Backend**: Flask (Python web framework)
- **Frontend**: React + Vite (unchanged)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Server**: Gunicorn (production WSGI server)

## File Structure

```
signal-integrity-assessment/
├── app.py                    # Flask application (main backend)
├── requirements.txt          # Python dependencies
├── build.py                  # Build script for React frontend
├── package.json             # Node dependencies (for frontend only)
├── render.yaml              # Render configuration
├── Procfile                 # Process configuration
├── runtime.txt              # Python version specification
├── .gitignore               # Git ignore patterns
├── client/                  # React frontend (unchanged)
│   ├── src/
│   ├── index.html
│   └── package.json
└── dist/                    # Built frontend (created during build)
```

## Quick Start - 5 Minutes

### Step 1: Push to GitHub

```bash
# Initialize Git repository
git init

# Add all files
git add .

# Commit
git commit -m "Python Flask version for Render"

# Create GitHub repo at https://github.com/new
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy to Render Using Blueprint

**This is the easiest method!**

1. Go to https://dashboard.render.com
2. Click **"New +"** → **Blueprint**
3. Connect your GitHub repository
4. Click **"Apply"**

That's it! Render will:
- Create PostgreSQL database
- Create web service
- Install Python dependencies
- Build React frontend
- Deploy your app

⏱️ First deployment takes ~5-10 minutes.

### Step 3: Access Your App

Once deployed, your app will be available at:
```
https://signal-integrity-assessment.onrender.com
```

---

## Alternative: Manual Deployment

### Step 1: Create PostgreSQL Database

1. Go to https://dashboard.render.com
2. Click **"New +"** → **PostgreSQL**
3. Settings:
   - Name: `signal-integrity-db`
   - Database: `signal_integrity`
   - User: `signal_user`
   - Plan: **Free** (or Starter for production)
4. Click **"Create Database"**
5. **Copy the Internal Database URL** (you'll need this)

### Step 2: Create Web Service

1. Click **"New +"** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `signal-integrity-assessment`
   - **Runtime**: **Python 3**
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python3 build.py
     ```
   - **Start Command**: 
     ```bash
     gunicorn app:app
     ```
   - **Plan**: Free (or Starter for always-on)

4. Add Environment Variables:
   - `DATABASE_URL`: (paste from Step 1)
   - `SECRET_KEY`: (generate random string)
   - `FLASK_ENV`: `production`

5. Click **"Create Web Service"**

---

## How It Works

### Build Process

When you deploy, Render runs:

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run build script (build.py)
python3 build.py
  ├── Install npm dependencies
  ├── Build React app with Vite
  └── Copy to dist/ folder

# 3. Start Flask app with Gunicorn
gunicorn app:app
```

### Application Architecture

```
┌─────────────────────────────────────┐
│         Gunicorn Server             │
│              (Port 10000)            │
└──────────────┬──────────────────────┘
               │
        ┌──────▼──────┐
        │   Flask App  │
        │   (app.py)   │
        └──────┬───────┘
               │
        ┏━━━━━━┻━━━━━━┓
        ┃              ┃
   ┌────▼────┐   ┌────▼─────┐
   │   API   │   │  Static  │
   │ Routes  │   │  Files   │
   │         │   │ (React)  │
   └────┬────┘   └──────────┘
        │
   ┌────▼────────┐
   │  PostgreSQL │
   │  Database   │
   └─────────────┘
```

### API Endpoints

Your Flask backend provides:

```python
GET  /api/messages         # Get all messages
POST /api/messages         # Create new message
GET  /api/health          # Health check

GET  /*                    # Serve React app (all other routes)
```

---

## Environment Variables

### Required

```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
```
- Automatically provided by Render when using Blueprint
- Or copy from your PostgreSQL database

### Optional

```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
PORT=10000  # Render sets this automatically
```

**Generate SECRET_KEY**:
```python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Local Development

### Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Node dependencies (for frontend)
npm install

# 4. Set environment variables
export DATABASE_URL="postgresql://localhost/signal_integrity"
export FLASK_ENV="development"

# 5. Run Flask development server
python app.py

# Or run with auto-reload
flask run --debug
```

### Development Workflow

```bash
# Terminal 1: Run Flask backend
python app.py

# Terminal 2: Run React frontend with hot reload
cd client
npm run dev

# React will proxy API requests to Flask at http://localhost:5000
```

### Building Frontend Only

```bash
# Build React app
cd client
npm run build

# Output will be in client/dist/
```

---

## Database Management

### Auto-Migration

Flask-SQLAlchemy automatically creates tables on first run:

```python
# This happens in app.py
with app.app_context():
    db.create_all()  # Creates all tables
```

### Manual Database Operations

```python
# Connect to your database
from app import app, db, Message

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Query messages
    messages = Message.query.all()
    
    # Create new message
    msg = Message(content="New message")
    db.session.add(msg)
    db.session.commit()
    
    # Delete all messages
    Message.query.delete()
    db.session.commit()
```

### Accessing Database via Render Shell

1. Go to your Web Service in Render
2. Click **"Shell"** tab
3. Run Python shell:

```bash
python3
```

```python
from app import app, db, Message

with app.app_context():
    # Your database operations here
    messages = Message.query.all()
    for msg in messages:
        print(msg.content)
```

---

## Troubleshooting

### Build Fails - npm not found

**Problem**: Build script can't find npm

**Solution**: Render needs Node.js installed. Update `render.yaml`:

```yaml
services:
  - type: web
    buildCommand: |
      curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
      export NVM_DIR="$HOME/.nvm"
      [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
      nvm install 18
      nvm use 18
      pip install -r requirements.txt
      python3 build.py
```

**Or simpler**: Use the Blueprint method - it handles this automatically!

### Database Connection Error

**Problem**: Can't connect to database

**Check**:
1. `DATABASE_URL` environment variable is set
2. Using Internal Database URL (not External)
3. URL starts with `postgresql://` (not `postgres://`)

**Fix**: The `app.py` automatically fixes postgres:// URLs:
```python
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
```

### App Won't Start

**Problem**: Gunicorn can't start app

**Check**:
1. `app.py` exists in root directory
2. Start command is: `gunicorn app:app`
3. Check logs in Render Dashboard

**Debug**:
```bash
# In Render Shell
python3 app.py  # Try running directly
```

### React App Not Loading

**Problem**: Get 404 or blank page

**Check**:
1. `dist/` folder exists after build
2. `dist/index.html` exists
3. Build script ran successfully

**Fix**: Rebuild manually:
```bash
# In Render Shell
python3 build.py
```

---

## Production Best Practices

### 1. Use Production Database

```yaml
databases:
  - name: signal-integrity-db
    plan: starter  # $7/month - includes backups
```

### 2. Always-On Service

```yaml
services:
  - type: web
    plan: starter  # $7/month - no spin-down
```

### 3. Increase Workers

For better performance:

```yaml
startCommand: gunicorn app:app --workers 4 --timeout 120
```

### 4. Enable Logging

```python
# Add to app.py
import logging

if not app.debug:
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Signal Integrity Assessment startup')
```

### 5. Set SECRET_KEY

Never use the default! Generate a secure one:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Add to Render environment variables.

---

## Monitoring

### Health Check

Your app includes a health check endpoint:

```bash
curl https://your-app.onrender.com/api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-27T12:00:00",
  "database": "connected"
}
```

### View Logs

```bash
# In Render Dashboard
Service → Logs tab

# Or use Render CLI
render logs -s signal-integrity-assessment
```

### Error Tracking

Add Sentry for error tracking:

```bash
pip install sentry-sdk[flask]
```

```python
# Add to app.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
)
```

---

## Scaling

### Vertical Scaling (More Resources)

```yaml
services:
  - type: web
    plan: standard  # 1 CPU, 2 GB RAM - $25/month
```

### Horizontal Scaling (Multiple Instances)

```yaml
services:
  - type: web
    plan: standard
    numInstances: 3  # Run 3 instances
```

Render automatically load balances between instances.

**Note**: Ensure your app is stateless (no in-memory sessions).

---

## Migration from Node.js Version

### What Changed

| Component | Node.js Version | Python Version |
|-----------|-----------------|----------------|
| Backend Framework | Express.js | Flask |
| ORM | Drizzle | SQLAlchemy |
| Runtime | Node.js 18+ | Python 3.11+ |
| Process Manager | tsx | Gunicorn |
| Build Tool | esbuild | Python + npm |
| Frontend | React + Vite | React + Vite (same) |

### What Stayed The Same

- ✅ React frontend (unchanged)
- ✅ PostgreSQL database
- ✅ API endpoints (same URLs)
- ✅ Deployment process
- ✅ Environment variables

### API Compatibility

Both versions have identical APIs:

```typescript
// Frontend code works with both backends
fetch('/api/messages')
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## Cost Breakdown

### Free Tier
```
Web Service:    $0   (spins down after 15 min)
PostgreSQL:     $0   (1 GB storage)
────────────────────
TOTAL:          $0/month
```
✅ Good for: Testing, demos, development

### Production (Starter)
```
Web Service:    $7   (always-on)
PostgreSQL:     $7   (backups, 10 GB)
────────────────────
TOTAL:          $14/month
```
✅ Good for: Production apps, side projects

### High Traffic (Standard)
```
Web Service:    $25  (better performance)
PostgreSQL:     $20  (50 GB, high performance)
────────────────────
TOTAL:          $45/month
```
✅ Good for: Growing apps, high traffic

---

## Files Explained

### Core Files

**app.py** - Main Flask application
- Handles API requests
- Serves React static files
- Manages database connections
- Includes health check endpoint

**requirements.txt** - Python dependencies
```
Flask==3.0.0            # Web framework
Flask-CORS==4.0.0       # CORS support
Flask-SQLAlchemy==3.1.1 # Database ORM
psycopg2-binary==2.9.9  # PostgreSQL driver
gunicorn==21.2.0        # Production server
```

**build.py** - Build automation script
- Installs Python dependencies
- Installs npm dependencies  
- Builds React frontend
- Copies to dist/ folder

**render.yaml** - Infrastructure as code
- Defines web service
- Defines database
- Configures environment variables
- Enables auto-deployment

**Procfile** - Process definition (backup)
```
web: gunicorn app:app
```

**runtime.txt** - Python version
```
python-3.11.0
```

---

## Testing Your Deployment

### 1. Check Homepage
```
https://your-app.onrender.com
```
Should show React app

### 2. Check API
```bash
curl https://your-app.onrender.com/api/messages
```
Should return JSON array

### 3. Check Health
```bash
curl https://your-app.onrender.com/api/health
```
Should return healthy status

### 4. Test Database
Try creating a message through your app

### 5. Check Logs
Look for errors in Render Dashboard → Logs

---

## Next Steps

1. ✅ Deploy to Render using Blueprint
2. ⏰ Wait for first deployment (~5-10 min)
3. 🧪 Test your application
4. 💰 Upgrade to Starter plan ($14/month)
5. 🌐 Add custom domain (optional)
6. 📊 Set up monitoring
7. 🔒 Generate secure SECRET_KEY
8. 💾 Enable database backups (Starter+)

---

## Getting Help

- **Flask Docs**: https://flask.palletsprojects.com
- **Render Docs**: https://render.com/docs/deploy-flask
- **Python Docs**: https://docs.python.org/3/
- **Community**: https://community.render.com

---

## Summary

✅ **Easy Deployment**: Use Blueprint for one-click deployment

✅ **Same Frontend**: React app unchanged, works identically

✅ **Python Backend**: Flask replaces Express.js, same API

✅ **PostgreSQL**: Database setup identical to Node version

✅ **Cost Effective**: $14/month for production

✅ **No Code Changes**: Frontend doesn't need modification

---

**Ready to deploy? Use the Blueprint method for the fastest deployment!** 🚀

Your app will be live in ~10 minutes! 🎉
