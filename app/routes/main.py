from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models.user import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('chat.dashboard'))
    return render_template('main/index.html', title='Welcome to SecureTalk')

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Get all users for the contacts list
    users = User.query.filter(User.id != current_user.id).all()
    
    return render_template('main/profile.html', 
                           title='Profile', 
                           users=users)

@main_bp.route('/users')
@login_required
def users():
    # Get all users except the current user
    users = User.query.filter(User.id != current_user.id).all()
    
    return render_template('main/users.html', 
                           title='Users', 
                           users=users)