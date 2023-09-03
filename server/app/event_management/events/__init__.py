from ... import sio
from .event_management_namespace import EventManagementNamespace


sio.on_namespace(EventManagementNamespace('/event_management'))
