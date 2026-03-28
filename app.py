from app import create_app, socketio
from config import config
import os

# Get configuration from environment or use development by default
config_name = os.environ.get('FLASK_ENV', 'development')

# Create app with the specified configuration
app = create_app(config_name)

if __name__ == '__main__':
    socketio.run(app, debug=config[config_name].DEBUG, host='0.0.0.0', port=5000)