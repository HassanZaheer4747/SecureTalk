from datetime import datetime
from app import db
from app.utils.crypto import encrypt_message, decrypt_message, generate_hash, verify_hash

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    encrypted_content = db.Column(db.Text, nullable=False)
    content_hash = db.Column(db.String(64), nullable=False)  # SHA-256 hash
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    @property
    def content(self):
        # Decrypt the message content when accessed
        decrypted_content = decrypt_message(self.encrypted_content)
        # Verify message integrity
        if not verify_hash(decrypted_content, self.content_hash):
            raise ValueError("Message integrity check failed. The message may have been tampered with.")
        return decrypted_content
    
    @content.setter
    def content(self, content):
        # Encrypt the message content before storing
        self.encrypted_content = encrypt_message(content)
        # Generate hash for integrity verification
        self.content_hash = generate_hash(content)
    
    def mark_as_read(self):
        self.is_read = True
        db.session.commit()
    
    def __repr__(self):
        return f"Message(sender_id={self.sender_id}, receiver_id={self.receiver_id}, timestamp={self.timestamp})"