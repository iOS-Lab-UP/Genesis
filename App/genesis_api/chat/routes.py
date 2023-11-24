from genesis_api import socketio
from genesis_api.chat.utils import *
from flask_socketio import join_room, leave_room, emit
from flask import request


@socketio.on('connect')
def handle_connect(msg):
    print('Client connected:', request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)


@socketio.on('send_message')
def handle_send_message(data):
    print('Received message:', data)
    emit('new_message', data, broadcast=True)


@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('join_room', {
         'message': f'{username} has joined the room {room}'}, room=room)


@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('leave_room', {
         'message': f'{username} has left the room {room}'}, room=room)
