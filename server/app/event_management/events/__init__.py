from flask_socketio import emit

from ... import sio
from .event_management_namespace import EventManagementNamespace

sio.on_namespace(EventManagementNamespace('/event_management'))


@sio.on_error_default
def default_error_handler(e):
    emit('error', e.args)
    raise e
