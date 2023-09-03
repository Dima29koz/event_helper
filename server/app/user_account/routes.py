from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    current_user,
    jwt_required,
    unset_jwt_cookies,
    get_jwt_identity, set_access_cookies
)

from . import user_account
from server.app.models.models import get_user_by_username
from ..models import models
from ...utils.hider import get_hidden_email, get_hidden_pwd
from ...utils.mail_utils import send_password_reset_email, send_email_confirmation_mail
from ...utils.route_handlers import handle_refresh_expiring_jwts


@user_account.after_request
def refresh_expiring_jwts(response):
    return handle_refresh_expiring_jwts(response)


@user_account.route('/login', methods=["POST"])
def login():
    request_data = request.get_json()
    user = get_user_by_username(request_data.get('username'))
    if not user or not user.check_password(request_data.get('pwd')):
        return jsonify(msg='Wrong username or password'), 401

    access_token = create_access_token(identity=user)
    response = jsonify(
        msg='login successful',
        token=access_token
    )
    set_access_cookies(response, access_token)
    return response


@user_account.route('/registration', methods=["POST"])
def registration():
    request_data = request.get_json()
    user = models.create_user(request_data)
    if not user:
        return jsonify(msg='username is not allowed'), 400

    send_email_confirmation_mail(user)
    return jsonify(msg='Проверьте вашу почту и следуйте инструкциям для её подтверждения')


@user_account.route('/reset_password_request', methods=['POST'])
@jwt_required(optional=True)
def reset_password_request():
    request_data = request.get_json()
    current_identity = get_jwt_identity()
    if current_identity:
        return jsonify(msg='user is already authenticated'), 403
    user = models.get_user_by_username(request_data.get('username'))
    if not user:
        return jsonify(msg='user not found'), 400

    send_password_reset_email(user)
    return jsonify(msg='Проверьте вашу почту и следуйте инструкциям для сброса пароля')


@user_account.route('/profile_settings')
@jwt_required()
def profile_settings():
    """view of `profile` page"""
    return jsonify(
        username=current_user.username,
        full_name=current_user.full_name,
        email=get_hidden_email(current_user.email),
        phone=current_user.phone,
        contacts=current_user.contacts,
        is_email_verified=current_user.is_email_verified,
        pwd=get_hidden_pwd(),
    )


@user_account.route('/confirm_email/<string:token>')
def confirm_email(token):
    user = models.User.verify_token(token, 'confirm_email')
    if not user:
        return jsonify(msg='Wrong token'), 400

    user.verify_email()
    return jsonify(msg='Your email has been confirmed.')


@user_account.route('/reset_password/<string:token>', methods=['POST'])
@jwt_required(optional=True)
def reset_password(token):
    current_identity = get_jwt_identity()
    if current_identity:
        return jsonify(msg='user is already authenticated'), 403

    request_data = request.get_json()
    user = models.User.verify_token(token, 'reset_password')
    if not user:
        return jsonify(msg='Wrong token'), 400

    user.set_pwd(request_data.get('new_pwd'))
    return jsonify(msg='Your password has been reset.')


@user_account.route('/locations', methods=["GET"])
@jwt_required()
def get_locations():
    return jsonify([location.to_dict() for location in current_user.locations])


@user_account.route('/create_location', methods=["POST"])
@jwt_required()
def create_location():
    request_data = request.get_json()
    location = models.Location(request_data, current_user)
    return jsonify(msg='Location created.', data=location.to_dict())


@user_account.route('/location/<int:location_id>', methods=["GET", "POST", "DELETE"])
@jwt_required()
def modify_location(location_id: int):
    location = models.get_location_by_id(location_id)
    if not location or location not in current_user.locations:
        return jsonify(msg='Not allowed'), 403

    if request.method == 'GET':
        return jsonify(location.to_dict())

    if request.method == 'POST':
        location.update(request.get_json())
        return jsonify(msg='Location updated', data=location.to_dict())

    if request.method == 'DELETE':
        location.delete()
        return jsonify(msg='Location deleted')


@user_account.route("/logout")
@jwt_required()
def logout():
    """logs out user"""
    response = jsonify(msg='logout successful')
    unset_jwt_cookies(response)
    return response
