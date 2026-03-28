# SecureTalk

SecureTalk is a secure messaging application built with Flask that prioritizes privacy and security. It features end-to-end encryption, secure authentication, and message integrity verification.

## Features

- **End-to-End Encryption**: All messages are encrypted using AES-256-CBC
- **Secure Authentication**: Password hashing with bcrypt and rate limiting for login attempts
- **Message Integrity**: SHA-256 hash verification ensures messages haven't been tampered with
- **Session Security**: Automatic session timeout after 30 minutes of inactivity
- **Real-time Messaging**: Instant message delivery using WebSockets
- **User Status Tracking**: See when users are online or offline
- **Responsive Design**: Works on desktop and mobile devices

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix/MacOS
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables in a `.env` file:
   ```
   SECRET_KEY=your_secret_key
   ENCRYPTION_KEY=your_32_byte_encryption_key
   DATABASE_URI=mysql+pymysql://username:password@localhost/securetalk
   ```
5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
6. Run the application:
   ```
   flask run
   ```

## Security Considerations

- The encryption key should be kept secure and not committed to version control
- In production, use HTTPS to protect data in transit
- Regularly update dependencies to patch security vulnerabilities
- Consider implementing additional security measures like two-factor authentication

## Project Structure

```
SecureTalk/
├── app/
│   ├── models/
│   │   ├── user.py
│   │   └── message.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── chat.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   ├── auth/
│   │   ├── chat/
│   │   └── main/
│   └── utils/
│       ├── crypto.py
│       └── forms.py
├── migrations/
├── instance/
├── app.py
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.