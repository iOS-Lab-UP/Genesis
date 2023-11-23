from genesis_api import socketio
from genesis_api.chat.utils import *
from flask_socketio import join_room, leave_room, emit


@socketio.on('connect')
def on_connect():
    print('User connected')


@socketio.on('disconnect')
def on_disconnect():
    print('User disconnected')


@socketio.on('chat_message')
def handle_chat_message(message):
    try:
        # Extract the sender's user ID from the message, assuming it's included
        user_id = message.get('user_id')

        # Optional: Print the message and sender ID to the server console
        print(f'Message from {user_id}: {message.get("text")}')

        # Emit the new message to all connected clients, including the sender
        # You can add the user_id to the message if it's not already included
        emit('new_message', message, broadcast=True)

        # Return True to acknowledge that the message was handled successfully
        return True
    except Exception as e:
        # If there's an error, print the error message to the server console
        print(f"Error handling chat_message: {e}")

        # Return False to acknowledge that there was an error handling the message
        return False


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.emit(
        'join_room', f'{username} has joined the room {room}', room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    socketio.emit(
        'leave_room', f'{username} has left the room {room}', room=room)
