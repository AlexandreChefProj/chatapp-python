from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from datetime import datetime
from app import socketio
from app.database import save_message

# --- Events ---
@socketio.on('connect')
def handle_connect():
    """Handle a new connection."""
    if current_user.is_authenticated:
        emit('connected', {'username': current_user.username})
        print(f"{current_user.username} connected.")
    else:
        emit('error', {'message': 'Authentication required'})
        return False  # Disconnect unauthenticated users

@socketio.on('disconnect')
def handle_disconnect():
    """Handle a disconnection."""
    if current_user.is_authenticated:
        print(f"{current_user.username} disconnected.")

@socketio.on('send_message')
def handle_send_message(data):
    """
    Handle receiving a new chat message from a client.
    Save the message to the database and broadcast it to all clients.
    """
    if not current_user.is_authenticated:
        emit('error', {'message': 'Authentication required'})
        return

    message = data.get('message', '').strip()
    if not message:
        emit('error', {'message': 'Message cannot be empty'})
        return

    # Save the message in the database
    save_message(current_user.username, message)

    # Broadcast the message to all connected clients
    emit('new_message', {
        'username': current_user.username,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }, broadcast=True)

@socketio.on('join_chat')
def handle_join_chat(data):
    """
    Handle a user joining a chat room (optional feature for rooms).
    """
    if not current_user.is_authenticated:
        emit('error', {'message': 'Authentication required'})
        return

    room = data.get('room', 'default')
    join_room(room)
    emit('joined_room', {'room': room}, to=room)
    print(f"{current_user.username} joined room {room}.")

@socketio.on('leave_chat')
def handle_leave_chat(data):
    """
    Handle a user leaving a chat room (optional feature for rooms).
    """
    if not current_user.is_authenticated:
        emit('error', {'message': 'Authentication required'})
        return

    room = data.get('room', 'default')
    leave_room(room)
    emit('left_room', {'room': room}, to=room)
    print(f"{current_user.username} left room {room}.")
