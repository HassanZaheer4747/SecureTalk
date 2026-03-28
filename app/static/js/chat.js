// SecureTalk - Chat JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Connect to Socket.IO server
    const socket = io();
    
    // DOM Elements
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const messagesContainer = document.getElementById('messages');
    const usersList = document.getElementById('users-list');
    const typingIndicator = document.getElementById('typing-indicator');
    const chatHeader = document.getElementById('chat-header');
    const messageInputContainer = document.getElementById('message-input-container');
    const noChatSelected = document.getElementById('no-chat-selected');
    
    // Get current user ID from data attribute
    const currentUserId = document.getElementById('current-user-id')?.value;
    let recipientId = null;
    let typingTimeout;
    
    // Connect event
    socket.on('connect', function() {
        console.log('Connected to server');
    });
    
    // Disconnect event
    socket.on('disconnect', function() {
        console.log('Disconnected from server');
    });
    
    // User status change event
    socket.on('user_status_change', function(data) {
        const userElement = document.getElementById(`user-${data.user_id}`);
        if (userElement) {
            const statusIndicator = userElement.querySelector('.status-indicator');
            const statusText = userElement.querySelector('.status-text');
            
            if (data.status === 'online') {
                statusIndicator.classList.remove('offline');
                statusIndicator.classList.add('online');
                if (statusText) statusText.textContent = 'Online';
            } else {
                statusIndicator.classList.remove('online');
                statusIndicator.classList.add('offline');
                if (statusText) statusText.textContent = 'Offline';
            }
        }
    });
    
    // Receive message event
    socket.on('new_message', function(data) {
        // Add message to chat
        addMessageToChat(data.sender_id, data.content, data.timestamp, false);
        
        // Play notification sound
        playNotificationSound();
        
        // Send read receipt if chat is open with this sender
        if (recipientId && recipientId == data.sender_id) {
            socket.emit('mark_read', {message_id: data.id});
        }
        
        // Update unread count in sidebar
        updateUnreadCount(data.sender_id);
    });
    
    // Message sent confirmation
    socket.on('message_sent', function(data) {
        // Update message status to sent
        const messageElement = document.getElementById(`message-${data.temp_id}`);
        if (messageElement) {
            const statusElement = messageElement.querySelector('.message-status');
            if (statusElement) {
                statusElement.innerHTML = '<i class="fas fa-check"></i>';
                statusElement.setAttribute('title', 'Sent');
            }
            // Update the message ID
            messageElement.id = `message-${data.id}`;
        }
    });
    
    // Message read confirmation
    socket.on('message_read', function(data) {
        // Update message status to read
        const messageElement = document.getElementById(`message-${data.message_id}`);
        if (messageElement) {
            const statusElement = messageElement.querySelector('.message-status');
            if (statusElement) {
                statusElement.innerHTML = '<i class="fas fa-check-double"></i>';
                statusElement.setAttribute('title', 'Read');
            }
        }
    });
    
    // User typing event
    socket.on('user_typing', function(data) {
        if (data.user_id == recipientId) {
            typingIndicator.textContent = 'Typing...';
            typingIndicator.style.display = 'block';
            
            // Hide typing indicator after 3 seconds
            clearTimeout(typingTimeout);
            typingTimeout = setTimeout(function() {
                typingIndicator.style.display = 'none';
            }, 3000);
        }
    });
    
    // Send message form submission
    if (messageForm) {
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const message = messageInput.value.trim();
            if (message && recipientId) {
                // Generate temporary ID for the message
                const tempId = 'temp-' + Date.now();
                
                // Add message to chat with pending status
                addMessageToChat(currentUserId, message, new Date().toISOString(), true, tempId);
                
                // Send message to server
                socket.emit('send_message', {
                    receiver_id: recipientId,
                    content: message,
                    temp_id: tempId
                });
                
                // Clear input
                messageInput.value = '';
                
                // Scroll to bottom
                scrollToBottom();
            }
        });
    }
    
    // Input typing event
    if (messageInput) {
        messageInput.addEventListener('input', function() {
            if (recipientId) {
                socket.emit('typing', {recipient_id: recipientId});
            }
        });
    }
    
    // User list click event
    if (usersList) {
        usersList.addEventListener('click', function(e) {
            const userItem = e.target.closest('.user-item');
            if (userItem) {
                const userId = userItem.getAttribute('data-user-id');
                if (userId) {
                    // Update active user
                    document.querySelectorAll('.user-item').forEach(item => {
                        item.classList.remove('active');
                    });
                    userItem.classList.add('active');
                    
                    // Update recipient ID
                    recipientId = userId;
                    document.getElementById('recipient-id').value = userId;
                    
                    // Show chat interface
                    chatHeader.style.display = 'flex';
                    messageInputContainer.style.display = 'block';
                    noChatSelected.style.display = 'none';
                    
                    // Update chat header
                    const username = userItem.querySelector('.user-name').textContent;
                    const userAvatar = userItem.querySelector('.user-avatar').textContent;
                    const isOnline = userItem.querySelector('.status-indicator').classList.contains('online');
                    
                    document.getElementById('chat-header-username').textContent = username;
                    document.getElementById('chat-header-avatar').textContent = userAvatar;
                    document.getElementById('chat-header-status').className = `status-indicator ${isOnline ? 'online' : 'offline'}`;
                    document.getElementById('chat-header-status-text').textContent = isOnline ? 'Online' : 'Offline';
                    
                    // Load chat history
                    loadChatHistory(userId);
                    
                    // Reset unread count
                    const unreadElement = userItem.querySelector('.unread-count');
                    if (unreadElement) {
                        unreadElement.textContent = '';
                        unreadElement.style.display = 'none';
                    }
                }
            }
        });
    }
    
    // Add message to chat
    function addMessageToChat(senderId, message, timestamp, isSent, tempId = null) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        
        if (senderId == currentUserId) {
            messageElement.classList.add('message-sent');
            
            // Add message status indicator for sent messages
            const statusHtml = '<span class="message-status" title="Sending"><i class="fas fa-clock"></i></span>';
            
            messageElement.innerHTML = `
                <div class="message-content">
                    <div class="message-text">${escapeHtml(message)}</div>
                    <div class="message-meta">
                        <span class="message-time">${formatTimestamp(timestamp)}</span>
                        ${statusHtml}
                    </div>
                </div>
            `;
        } else {
            messageElement.classList.add('message-received');
            
            messageElement.innerHTML = `
                <div class="message-content">
                    <div class="message-text">${escapeHtml(message)}</div>
                    <div class="message-meta">
                        <span class="message-time">${formatTimestamp(timestamp)}</span>
                    </div>
                </div>
            `;
        }
        
        if (tempId) {
            messageElement.id = `message-${tempId}`;
        }
        
        messagesContainer.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Load chat history
    function loadChatHistory(userId) {
        fetch(`/chat/history/${userId}`)
            .then(response => response.json())
            .then(data => {
                // Clear existing messages
                messagesContainer.innerHTML = '';
                
                // Add messages to chat
                data.messages.forEach(msg => {
                    addMessageToChat(msg.sender_id, msg.content, msg.timestamp, msg.sender_id == currentUserId);
                });
                
                scrollToBottom();
            })
            .catch(error => {
                console.error('Error loading chat history:', error);
            });
    }
    
    // Update unread count
    function updateUnreadCount(senderId) {
        const userElement = document.getElementById(`user-${senderId}`);
        if (userElement) {
            const unreadElement = userElement.querySelector('.unread-count');
            if (unreadElement) {
                const currentCount = parseInt(unreadElement.textContent) || 0;
                const newCount = currentCount + 1;
                unreadElement.textContent = newCount;
                unreadElement.style.display = 'block';
            }
        }
    }
    
    // Play notification sound
    function playNotificationSound() {
        // You can add sound notification here
        console.log('Notification sound played');
    }
    
    // Scroll to bottom of messages
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Format timestamp
    function formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }
    
    // Escape HTML to prevent XSS
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});