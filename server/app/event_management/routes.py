from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

from . import event_management
from ..models import models


@event_management.route('/create_event', methods=["POST"])
@jwt_required()
def create_event():
    request_data = request.get_json()
    event = models.create_event(request_data, current_user)
    if not event:
        return jsonify(msg='Not allowed'), 403
    return jsonify(msg='Event created.', key=event.key)


@event_management.route('/events', methods=["GET"])
@jwt_required()
def get_events():
    # todo events where cur_user is creator and all events where cur_user is member
    return jsonify(
        creator_on=[event.as_dict() for event in current_user.events],
        member_on=[]
    )
