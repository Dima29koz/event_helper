from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

from . import event_management
from ..models import models
from ...utils.route_handlers import handle_refresh_expiring_jwts


@event_management.after_request
def refresh_expiring_jwts(response):
    return handle_refresh_expiring_jwts(response)


@event_management.route('/create_event', methods=["POST"])
@jwt_required()
def create_event():
    request_data = request.get_json()
    event = models.Event(request_data, current_user)
    return jsonify(msg='Event created.')


@event_management.route('/events', methods=["GET"])
@jwt_required()
def get_events():
    # todo events where cur_user is creator and all events where cur_user is member
    return jsonify()
