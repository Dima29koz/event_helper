from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import current_user, decode_token
from socketio.exceptions import ConnectionRefusedError

from server.app.models import models
from server.common.enums import Role


def roles_required(roles: set[Role] = None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            event = models.Event.get_by_id(kwargs.get('event_id'))
            if not event:
                return jsonify(msg='Event id not found'), 404
            if current_user == event.creator or _has_role(roles, current_user, event):
                return fn(*args, **kwargs)
            return jsonify(msg='Not allowed'), 403

        return decorated_view

    return wrapper


def keys_required(user_token=False):
    def wrapper(fn):
        @wraps(fn)
        def decorated_event(*args, **kwargs):
            event_key = request.headers.get('Event-Key') or kwargs.get('event_key')
            event = models.Event.get_by_key(event_key)
            if not event:
                raise ConnectionRefusedError()
            if user_token:
                token = args[0].get('auth', dict()).get('access_token')
                csrf_token = args[0].get('auth', dict()).get('csrf_access_token')

                token_data = decode_token(token, csrf_token)

                user = models.User.get_by_id(token_data.get("sub"))
                return fn(*args, event=event, current_user=user, **kwargs)
            return fn(*args, event=event, **kwargs)

        return decorated_event

    return wrapper


def socket_roles_required(roles: set[Role] = None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_event(*args, **kwargs):
            event = kwargs.get('event')
            user = kwargs.get('current_user')
            if user == event.creator or _has_role(roles, user, event):
                return fn(*args, **kwargs)
            raise Exception('User has not required role')

        return decorated_event

    return wrapper


def _has_role(roles: set[Role], user: models.User, event: models.Event):
    return any(filter(lambda member: member.role in roles and member.user == user, event.members))
