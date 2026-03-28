from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, current_user, logout_user, login_required
from hmac import compare_digest
from datetime import datetime, timedelta
from app import db, limiter
from app.models.user import User
from app.utils.forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Rate limiting for login attempts to prevent brute force attacks
@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.verify_password(form.password.data):
            # Successful login
            login_user(user, remember=form.remember.data)
            user.update_last_login()
            
            # Set session timeout (30 minutes of inactivity)
            session.permanent = True
            session.modified = True
            
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.index'))
        else:
            # Failed login attempt
            flash('Login unsuccessful. Please check email and password', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        
        if existing_user:
            flash('Username already taken. Please choose a different one.', 'danger')
        elif existing_email:
            flash('Email already registered. Please use a different email or login.', 'danger')
        else:
            # Create new user with securely hashed password
            user = User(username=form.username.data, email=form.email.data)
            user.password = form.password.data  # This will hash the password
            
            db.session.add(user)
            db.session.commit()
            
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    current_user.update_online_status(False)
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

# Session management - check for session timeout
@auth_bp.before_app_request
def before_request():
    session.permanent = True
    session.modified = True
    current_app.permanent_session_lifetime = timedelta(minutes=30)
    
    # Update user's online status
    if current_user.is_authenticated:
        current_user.update_online_status(True)