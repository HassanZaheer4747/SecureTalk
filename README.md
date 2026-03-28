# 🔐 SecureTalk

A modern, secure messaging application built with Flask that prioritizes **privacy, security, and real-time communication**. 

## ✨ Key Features

- **🔒 End-to-End Encryption** - All messages encrypted with AES-256-CBC
- **🛡️ Secure Authentication** - Bcrypt password hashing with rate limiting
- **⚡ Real-Time Messaging** - Instant message delivery using WebSockets
- **✅ Message Integrity** - SHA-256 hash verification prevents tampering
- **👥 User Status Tracking** - See online/offline status in real-time
- **⏱️ Session Security** - Auto-logout after 30 minutes of inactivity
- **📱 Responsive Design** - Works seamlessly on desktop and mobile

## 🎯 Use Cases

- Secure team communication
- Privacy-focused messaging platform
- Educational project demonstrating encryption & security best practices
- Foundation for building enterprise messaging solutions

## 🚀 Tech Stack

- **Backend**: Flask, Flask-SocketIO, SQLAlchemy
- **Security**: AES-256-CBC encryption, Bcrypt, Flask-Limiter
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (configurable for MySQL)
- **Real-time**: WebSockets with Flask-SocketIO

## 📋 Requirements

- Python 3.8+
- Virtual environment (venv/virtualenv)
- All dependencies in `requirements.txt`

## 🔧 Quick Start

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r [requirements.txt](http://_vscodecontentref_/0)
python [run.py](http://_vscodecontentref_/1)

📚 Project Structure
SecureTalk/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints & blueprints
│   ├── static/          # CSS & JavaScript
│   ├── templates/       # HTML templates
│   └── utils/           # Crypto & form utilities
├── [config.py](http://_vscodecontentref_/2)            # Configuration management
├── [run.py](http://_vscodecontentref_/3)              # Application entry point
└── [requirements.txt](http://_vscodecontentref_/4)    # Dependencies

⚙️ Configuration

   SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_32_byte_key
DATABASE_URI=sqlite:///instance/securetalk.db
FLASK_ENV=development
