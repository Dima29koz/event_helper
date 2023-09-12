from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

from . import event_management
from ..models.models import Event
from ..models.views import EventView


@event_management.route('/create_event', methods=["POST"])
@jwt_required()
def create_event():
    request_data = request.get_json()
    event = Event.create(request_data, current_user)
    if not event:
        return jsonify(msg='Not allowed'), 403
    return jsonify(msg='Event created.', key=event.key)


@event_management.route('/events', methods=["GET"])
@jwt_required()
def get_events():
    event_view = EventView(current_user)
    return jsonify(
        creator_on=event_view.get_list(current_user.events),
        member_on=event_view.get_list_with_data(current_user.get_events_where_member())
    )
