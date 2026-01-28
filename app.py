"""
Signal Integrity Assessment - Flask Backend
Main application entry point
"""

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os
from datetime import datetime

# Database setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__, static_folder='dist', static_url_path='')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
# Fix for Render/Heroku postgres:// URLs
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize extensions
db.init_app(app)
CORS(app)

# Models
class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Create tables
with app.app_context():
    db.create_all()
    
    # Seed database if empty
    if Message.query.count() == 0:
        seed_messages = [
            Message(content="Hello from the backend!"),
            Message(content="This is a seed message.")
        ]
        db.session.add_all(seed_messages)
        db.session.commit()
        print("Database seeded with initial messages")

# API Routes
@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Get all messages"""
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return jsonify([msg.to_dict() for msg in messages])

@app.route('/api/messages', methods=['POST'])
def create_message():
    """Create a new message"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'message': 'Content is required'}), 400
        
        content = data['content']
        if not content or not content.strip():
            return jsonify({'message': 'Content cannot be empty'}), 400
        
        message = Message(content=content)
        db.session.add(message)
        db.session.commit()
        
        return jsonify(message.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating message: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500

# Health check endpoint
@app.route("/api/health", methods=["GET"])
def health_check():
    return "OK", 200


# Serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve React app for all non-API routes"""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Error handlers
@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    # If it's an API request, return JSON
    if request.path.startswith('/api/'):
        return jsonify({'message': 'Not found'}), 404
    # Otherwise serve the React app (for client-side routing)
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'message': 'Internal Server Error'}), 500

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
