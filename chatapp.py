from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from Crypto.Cipher import AES
import base64
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!123"
socketio = SocketIO(app, cors_allowed_origins="*")

# AES encryption/decryption setup
key = os.urandom(16)  # Random 16-byte AES key

def encrypt_message(message):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

def decrypt_message(encrypted_message):
    try:
        decoded_message = base64.b64decode(encrypted_message)
        nonce = decoded_message[:16]
        tag = decoded_message[16:32]
        ciphertext = decoded_message[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    except Exception as e:
        print("Decryption error:", e)
        return None

# Handling user connected event
@socketio.on('user_connected')
def handle_user_connected(data):
    print("User connected: " + data)
    emit('message', {"username": "System", "message": data}, broadcast=True)  # Broadcast to all users

# Handling message event
@socketio.on('send_message')
def handle_send_message(data):
    username = data['username']
    message = data['message']
    
    # Encrypt the message
    encrypted_message = encrypt_message(message)
    
    print(f"Received message from {username}: {message} (Encrypted: {encrypted_message})")
    
    # Send the encrypted message to other clients
    emit('message', {'username': username, 'message': encrypted_message}, broadcast=True)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host="192.168.1.3", port=5000, debug=True)
