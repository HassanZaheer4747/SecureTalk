import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from flask import current_app

def get_encryption_key():
    """Get the encryption key from environment or app config"""
    key = current_app.config.get('ENCRYPTION_KEY')
    if not key:
        # Use a default key for development (this should be changed in production)
        key = os.environ.get('ENCRYPTION_KEY', 'default_dev_key_change_in_production')
    
    # Ensure the key is 32 bytes (256 bits) for AES-256
    return hashlib.sha256(key.encode()).digest()

def encrypt_message(message):
    """Encrypt a message using AES-256-CBC"""
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    
    # Convert the message to bytes
    message_bytes = message.encode('utf-8')
    
    # Add padding
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message_bytes) + padder.finalize()
    
    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)  # 16 bytes for AES
    
    # Create an encryptor
    cipher = Cipher(
        algorithms.AES(get_encryption_key()),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    
    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combine IV and encrypted data and encode as base64
    encrypted_message = base64.b64encode(iv + encrypted_data).decode('utf-8')
    
    return encrypted_message

def decrypt_message(encrypted_message):
    """Decrypt a message that was encrypted using AES-256-CBC"""
    # Decode the base64 encoded message
    encrypted_data = base64.b64decode(encrypted_message.encode('utf-8'))
    
    # Extract the IV (first 16 bytes)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    
    # Create a decryptor
    cipher = Cipher(
        algorithms.AES(get_encryption_key()),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    # Convert bytes back to string
    return data.decode('utf-8')

def generate_hash(message):
    """Generate a SHA-256 hash of the message for integrity verification"""
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    
    # Create a SHA-256 hash of the message
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

def verify_hash(message, hash_value):
    """Verify the integrity of a message using its hash"""
    # Generate a new hash of the message
    new_hash = generate_hash(message)
    
    # Compare the new hash with the provided hash
    return new_hash == hash_value