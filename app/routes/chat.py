from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import current_user, login_required
from flask_socketio import emit, join_room, leave_room
from app import db, socketio
from app.models.user import User
from app.models.message import Message
from sqlalchemy import or_, and_

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

# Chat dashboard - main chat interface
@chat_bp.route('/dashboard')
@login_required
def dashboard():
    # Get all users except the current user
    users = User.query.filter(User.id != current_user.id).all()
    
    return render_template('chat/dashboard.html', 
                           title='Chat Dashboard', 
                           users=users)

# Get chat history with a specific user
@chat_bp.route('/history/<int:user_id>')
@login_required
def chat_history(user_id):
    # Verify the user exists
    user = User.query.get_or_404(user_id)
    
    # Get all messages between current user and the selected user
    messages = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == user_id),
            and_(Message.sender_id == user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.timestamp).all()
    
    # Mark unread messages as read
    unread_messages = Message.query.filter_by(
        sender_id=user_id, 
        receiver_id=current_user.id,
        is_read=False
    ).all()
    
    for msg in unread_messages:
        msg.mark_as_read()
    
    # Format messages for display
    message_list = []
    for msg in messages:
        try:
            message_list.append({
                'id': msg.id,
                'sender_id': msg.sender_id,
                'receiver_id': msg.receiver_id,
                'content': msg.content,  # This will decrypt the message
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_read': msg.is_read
            })
        except ValueError as e:
            # Handle integrity check failure
            message_list.append({
                'id': msg.id,
                'sender_id': msg.sender_id,
                'receiver_id': msg.receiver_id,
                'content': "[Message integrity check failed]",
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_read': msg.is_read,
                'error': str(e)
            })
    
    return jsonify({
        'messages': message_list,
        'user': {
            'id': user.id,
            'username': user.username,
            'is_online': user.is_online
        }
    })

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        # Join a personal room for private messages
        join_room(f'user_{current_user.id}')
        current_user.update_online_status(True)
        
        # Broadcast to all users that this user is online
        emit('user_status_change', {
            'user_id': current_user.id,
            'status': 'online'
        }, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        leave_room(f'user_{current_user.id}')
        current_user.update_online_status(False)
        
        # Broadcast to all users that this user is offline
        emit('user_status_change', {
            'user_id': current_user.id,
            'status': 'offline'
        }, broadcast=True)

@socketio.on('send_message')
def handle_send_message(data):
    if current_user.is_authenticated:
        receiver_id = data.get('receiver_id')
        content = data.get('content')
        
        if not receiver_id or not content:
            emit('error', {'message': 'Invalid message data'}, room=f'user_{current_user.id}')
            return
        
        # Create and save the message
        message = Message(
            sender_id=current_user.id,
            receiver_id=receiver_id
        )
        message.content = content  # This will encrypt the message and generate hash
        
        db.session.add(message)
        db.session.commit()
        
        # Send the message to the receiver's room
        emit('new_message', {
            'id': message.id,
            'sender_id': message.sender_id,
            'sender_username': current_user.username,
            'receiver_id': message.receiver_id,
            'content': content,  # Send the original content, not the encrypted version
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': False
        }, room=f'user_{receiver_id}')
        
        # Also send back to the sender for confirmation
        emit('message_sent', {
            'id': message.id,
            'receiver_id': message.receiver_id,
            'content': content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, room=f'user_{current_user.id}')

@socketio.on('mark_read')
def handle_mark_read(data):
    if current_user.is_authenticated:
        message_id = data.get('message_id')
        
        if not message_id:
            return
        
        message = Message.query.get(message_id)
        if message and message.receiver_id == current_user.id:
            message.mark_as_read()
            
            # Notify the sender that the message was read
            emit('message_read', {
                'message_id': message_id
            }, room=f'user_{message.sender_id}')

@socketio.on('typing')
def handle_typing(data):
    if current_user.is_authenticated:
        recipient_id = data.get('recipient_id')
        if recipient_id:
            emit('user_typing', {
                'user_id': current_user.id
            }, room=f'user_{recipient_id}')