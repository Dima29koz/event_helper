from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

from . import event_management
from ..models import models
from ...common.enums import Role
from ...utils.role_required import roles_required
from ...utils.route_handlers import handle_refresh_expiring_jwts


@event_management.after_request
def refresh_expiring_jwts(response):
    return handle_refresh_expiring_jwts(response)


@event_management.route('/create_event', methods=["POST"])
@jwt_required()
def create_event():
    request_data = request.get_json()
    event = models.create_event(request_data, current_user)
    if not event:
        return jsonify(msg='Not allowed'), 403
    return jsonify(msg='Event created.', data=event.as_dict())


@event_management.route('/events', methods=["GET"])
@jwt_required()
def get_events():
    # todo events where cur_user is creator and all events where cur_user is member
    return jsonify(
        creator_on=[event.as_dict() for event in current_user.events],
        member_on=[]
    )


@event_management.route('/event/<int:event_id>/add_member', methods=["POST"])
@jwt_required()
@roles_required({Role.organizer, })
def add_event_member(event_id: int):
    request_data = request.get_json()
    event = models.get_event_by_id(event_id)
    member = models.EventMember(request_data)
    event.add_member(member)

    return jsonify(msg='ok')
