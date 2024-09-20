from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!123"  # Secret key
socketio = SocketIO(app, cors_allowed_origins="*")  # Allowing Cross-Origin

# Handle user connected event
@socketio.on('user_connected')
def handle_user_connected(data):
    print("User connected: " + data)
    emit('message', data, broadcast=True)  # Broadcast to all users

# Handle message event
@socketio.on('send_message')
def handle_send_message(data):
    print(f"Received message from {data['username']}: {data['message']}")
    full_message = f"{data['username']}: {data['message']}"
    emit('message', full_message, broadcast=True)  # Broadcast the message to all clients

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host="192.168.56.1", port=5000, debug=True)