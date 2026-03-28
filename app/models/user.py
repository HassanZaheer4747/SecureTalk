from datetime import datetime
from flask_login import UserMixin
from app import db, bcrypt, login_manager

# Define user roles
class UserRole:
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=UserRole.USER)
    last_login = db.Column(db.DateTime, default=None)
    is_online = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)
    
    # Authentication methods
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    # Role-based authorization methods
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    def is_moderator(self):
        return self.role == UserRole.MODERATOR
    
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        self.is_online = True
        db.session.commit()
    
    def update_online_status(self, status):
        self.is_online = status
        db.session.commit()
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))