# Signal Integrity Assessment - Python/Flask Version

A structured executive assessment tool to reveal the reliability of leadership awareness across critical business operations.

## 🚀 Quick Deploy to Render

### Method 1: Blueprint (Easiest - 1 Click!)

1. Push this code to GitHub
2. Go to https://dashboard.render.com
3. Click **New +** → **Blueprint**
4. Connect your repository
5. Click **Apply**

Done! Your app will be live in ~10 minutes at `https://your-app.onrender.com`

### Method 2: Manual Setup (5 Minutes)

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# 2. Create PostgreSQL database on Render
# Dashboard → New + → PostgreSQL → Create

# 3. Create Web Service on Render
# Dashboard → New + → Web Service
# Build Command: pip install -r requirements.txt && python3 build.py
# Start Command: gunicorn app:app
# Add DATABASE_URL environment variable

# 4. Deploy!
```

## 🏗️ Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM  
- **PostgreSQL** - Database
- **Gunicorn** - Production WSGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library

## 📁 Project Structure

```
.
├── app.py              # Flask application (main backend)
├── requirements.txt    # Python dependencies
├── build.py           # Build script (React + Python)
├── package.json       # Node dependencies (frontend only)
├── render.yaml        # Render deployment config
├── Procfile           # Process definition
├── runtime.txt        # Python version
├── client/            # React frontend
│   ├── src/
│   │   ├── App.tsx    # Main React component
│   │   └── ...
│   ├── index.html
│   └── package.json
└── dist/             # Built frontend (created by build.py)
```

## 💻 Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn
- PostgreSQL (optional for local dev)

### Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Node dependencies
npm install

# 4. Set environment variables
export DATABASE_URL="postgresql://localhost/signal_integrity"
export FLASK_ENV="development"
export SECRET_KEY="dev-secret-key"

# 5. Run development server
python app.py
```

The app will be available at `http://localhost:5000`

### Development with Hot Reload

```bash
# Terminal 1: Flask backend
python app.py

# Terminal 2: React frontend (hot reload)
cd client
npm run dev
```

React will run on `http://localhost:5173` and proxy API requests to Flask.

## 🔨 Build

### Build Frontend Only
```bash
cd client
npm run build
```

### Full Build (Python + React)
```bash
python3 build.py
```

This will:
1. Install Python dependencies
2. Install npm dependencies
3. Build React app with Vite
4. Copy build to `dist/` folder

## 🌐 API Endpoints

```
GET  /api/messages         # Get all messages
POST /api/messages         # Create new message
  Body: { "content": "string" }

GET  /api/health          # Health check endpoint
GET  /*                   # Serve React app (catch-all)
```

## 🔧 Environment Variables

### Required
```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Optional
```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=production  # or development
PORT=5000            # Render sets this automatically
```

Generate SECRET_KEY:
```python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## 🗄️ Database

### Auto-Migration
Tables are automatically created on first run:
```python
with app.app_context():
    db.create_all()
```

### Database Models

**Message Model:**
```python
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Manual Database Operations

```python
from app import app, db, Message

with app.app_context():
    # Create tables
    db.create_all()
    
    # Query messages
    messages = Message.query.all()
    
    # Create message
    msg = Message(content="Hello")
    db.session.add(msg)
    db.session.commit()
```

## 🚀 Deployment

### Render (Recommended)

**Using Blueprint (Easiest):**
1. Add `render.yaml` to your repo (already included)
2. Push to GitHub
3. Render Dashboard → New + → Blueprint
4. Connect repo → Apply

**Manual Setup:**
See [PYTHON_DEPLOYMENT_GUIDE.md](PYTHON_DEPLOYMENT_GUIDE.md)

### Other Platforms

**Heroku:**
```bash
heroku create your-app-name
git push heroku main
```

**Railway:**
```bash
railway init
railway up
```

**DigitalOcean App Platform:**
Use the included `render.yaml` - it's compatible!

## 🧪 Testing

```bash
# Test Flask backend
curl http://localhost:5000/api/health

# Test API endpoints
curl http://localhost:5000/api/messages

# Create message
curl -X POST http://localhost:5000/api/messages \
  -H "Content-Type: application/json" \
  -d '{"content":"Test message"}'
```

## 📦 Dependencies

### Python (requirements.txt)
- Flask 3.0.0 - Web framework
- Flask-CORS 4.0.0 - CORS support
- Flask-SQLAlchemy 3.1.1 - ORM
- psycopg2-binary 2.9.9 - PostgreSQL adapter
- gunicorn 21.2.0 - Production server

### Node (package.json)
- React 18.3.1 - UI framework
- Vite 7.3.0 - Build tool
- Tailwind CSS 3.4.17 - Styling
- TypeScript 5.6.3 - Type safety

## 🐛 Troubleshooting

### Build fails
- Check Python version: `python3 --version` (need 3.11+)
- Check Node version: `node --version` (need 18+)
- Clear build cache: `rm -rf dist/ client/dist/`

### Database connection error
- Check DATABASE_URL format
- Ensure PostgreSQL is running (local dev)
- Use Internal URL on Render (not External)

### App won't start
- Check logs: Render Dashboard → Logs
- Try running locally: `python app.py`
- Check gunicorn: `gunicorn --version`

### React app not loading
- Build frontend: `python3 build.py`
- Check dist folder exists: `ls -la dist/`
- Check Flask is serving static files

## 📊 Performance

### Production Settings

**Gunicorn Workers:**
```bash
gunicorn app:app --workers 4 --timeout 120
```

**Database Connection Pooling:**
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
}
```

## 🔒 Security

- ✅ CORS configured with Flask-CORS
- ✅ Secret key for session management
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ HTTPS enforced on Render
- ⚠️ Change SECRET_KEY in production!

## 💰 Cost Estimate

### Render Pricing
- **Free Tier**: $0 (spins down after 15 min)
- **Starter**: $14/month (always-on web + database)
- **Standard**: $45/month (better performance)

Recommended for production: **Starter ($14/month)**

## 📚 Documentation

- [Python Deployment Guide](PYTHON_DEPLOYMENT_GUIDE.md) - Complete deployment walkthrough
- [Flask Documentation](https://flask.palletsprojects.com)
- [Render Documentation](https://render.com/docs)
- [React Documentation](https://react.dev)

## 🤝 Contributing

This is a migration from Node.js/Express to Python/Flask. The frontend React app remains unchanged.

### Original Node.js Version
If you need the Node.js version, see the git history or contact the maintainers.

## 📝 License

MIT

## 🙋 Support

- **Issues**: Create a GitHub issue
- **Render Support**: support@render.com
- **Community**: https://community.render.com

---

## Quick Commands Cheat Sheet

```bash
# Development
python app.py                    # Run Flask dev server
cd client && npm run dev        # Run React dev server

# Build
python3 build.py                # Full build
cd client && npm run build      # Frontend only

# Production
gunicorn app:app                # Start production server

# Database
python3                         # Python shell
>>> from app import app, db, Message
>>> with app.app_context(): db.create_all()

# Deploy
git push origin main            # Auto-deploys on Render

# View logs
# Render Dashboard → Your Service → Logs
```

---

**Ready to deploy?** See [PYTHON_DEPLOYMENT_GUIDE.md](PYTHON_DEPLOYMENT_GUIDE.md) for detailed instructions! 🚀
