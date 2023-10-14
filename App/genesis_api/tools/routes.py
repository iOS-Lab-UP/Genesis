from flask import Blueprint, jsonify, session
from uptime import uptime
from genesis_api.tools.utils import *
from genesis_api.config import Config
import psutil
import datetime


tools = Blueprint('tools', __name__)


@tools.route('/', methods=['GET', 'POST'])
def health():
    '''
    Check if the server is up
    status: OK, SLOW, CRITICAL
    memory_usage: percentage of memory usage
    cpu_usage: percentage of cpu usage
    port: port where the server is running
    message: Server is up and running
    '''
    cpu = psutil.cpu_percent()
    return jsonify({
        "status": f"{server_status()}",
        "memory_usage": f"{getattr(psutil.virtual_memory(), 'percent')}%",
        "cpu_usage": f"{cpu}%",
        "port": 5555,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": f"{uptime() / 60 / 60 / 24:.2f} days",
        "message": "Server is up and running",
    })


@tools.route('/set/')
def set_key():
    Config.REDIS_CLIENT.set('key', 'value')
    return "Key set in session"


@tools.route('/get/')
def get():
    value = Config.REDIS_CLIENT.get('key')
    return f"Key value from session: {value}"