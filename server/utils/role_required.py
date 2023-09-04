from functools import wraps

from flask import jsonify
from flask_jwt_extended import current_user

from server.app.models.models import get_event_by_id
from server.common.enums import Role


def roles_required(roles: set[Role] = None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            event = get_event_by_id(kwargs.get('event_id'))
            if not event:
                return jsonify(msg='Event id not found'), 404
            if (current_user == event.creator or
                    any(filter(lambda member: member.role in roles and member.user == current_user, event.members))):
                return fn(*args, **kwargs)
            return jsonify(msg='Not allowed'), 403

        return decorated_view

    return wrapper
