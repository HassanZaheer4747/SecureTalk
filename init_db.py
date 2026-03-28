#!/usr/bin/env python
# Database initialization script for SecureTalk

import os
import sys
from flask import Flask
from flask_migrate import Migrate, upgrade
from app import db
from app.models.user import User
from app.models.message import Message
from config import config

def init_db():
    """Initialize the database with tables and initial data."""
    # Create a minimal Flask application
    app = Flask(__name__)
    app.config.from_object(config['development'])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.password = 'Admin123!'
            db.session.add(admin)
            
            # Create test user
            test_user = User(username='testuser', email='test@example.com', role='user')
            test_user.password = 'Test123!'
            db.session.add(test_user)
            
            db.session.commit()
            print('Created admin and test users')
        else:
            print('Admin user already exists')
        
        print('Database initialized successfully')

def run_migrations():
    """Run database migrations."""
    # Create a minimal Flask application
    app = Flask(__name__)
    app.config.from_object(config['development'])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        # Run migrations
        upgrade()
        print('Migrations applied successfully')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'migrate':
        run_migrations()
    else:
        init_db()