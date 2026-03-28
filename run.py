#!/usr/bin/env python
# Run script for SecureTalk

import os
from app import create_app, socketio
from config import config

# Get configuration from environment or use development by default
config_name = os.environ.get('FLASK_ENV', 'development')

# Create app with the specified configuration
app = create_app(config_name)

if __name__ == '__main__':
    # Get port from environment or use 5000 by default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app with socketio
    socketio.run(app, host='0.0.0.0', port=port, debug=True)