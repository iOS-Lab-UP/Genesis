from genesis_api import socketio
from genesis_api.chat.utils import *
from flask_socketio import join_room, leave_room


@socketio.on('connect')
def on_connect():
    print('User connected')


@socketio.on('disconnect')
def on_disconnect():
    print('User disconnected')


@socketio.on('chat_message')
def handle_chat_message(message):
    # Broadcast message to all connected clients
    socketio.emit('new_message', message)


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
