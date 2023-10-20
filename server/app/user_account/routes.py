from flask import request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    current_user,
    jwt_required,
    unset_jwt_cookies,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    create_refresh_token
)

from . import user_account
from ..models.models import User, Location
from ..models.views import UserView, LocationView
from ...utils.mail_utils import send_password_reset_email, send_email_confirmation_mail


@user_account.route('/login', methods=["POST"])
def login():
    request_data = request.get_json()
    user = User.get_by_username(request_data.get('username'))
    if not user or not user.check_password(request_data.get('pwd')):
        return jsonify(msg='Wrong username or password'), 401

    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    response = jsonify(msg='login successful')
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response


@user_account.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    response = jsonify(msg='access token refreshed')
    access_token = create_access_token(identity=current_user)
    set_access_cookies(response, access_token)
    return response


@user_account.route('/registration', methods=["POST"])
def registration():
    request_data = request.get_json()
    user = User.create(request_data)
    if not user:
        return jsonify(msg='username is not allowed'), 400

    if current_app.config['SEND_MAIL']:
        send_email_confirmation_mail(user, request.headers.get('X-ORIGIN'))
        return jsonify(msg='Проверьте вашу почту и следуйте инструкциям для её подтверждения')
    return jsonify(
        msg='Отправка сообщений отключена',
        confirm_email_token=user.get_token('confirm_email'),
    )


@user_account.route('/reset_password_request', methods=['POST'])
@jwt_required(optional=True)
def reset_password_request():
    request_data = request.get_json()
    current_identity = get_jwt_identity()
    if current_identity:
        return jsonify(msg='user is already authenticated'), 403
    user = User.get_by_username(request_data.get('username'))
    if not user:
        return jsonify(msg='Проверьте вашу почту и следуйте инструкциям для сброса пароля')

    if current_app.config['SEND_MAIL']:
        send_password_reset_email(user, request.headers.get('X-ORIGIN'))
        return jsonify(msg='Проверьте вашу почту и следуйте инструкциям для сброса пароля')
    return jsonify(
        msg='Отправка сообщений отключена',
        reset_password_token=user.get_token('reset_password'),
    )


@user_account.route('/profile_settings')
@user_account.route('/profile_settings/<string:username>')
@jwt_required(optional=True)
def profile_settings(username: str = None):
    """view of `profile` page"""
    if username is None:
        if get_jwt_identity() is None:
            return jsonify(msg='Missing JWT in headers or cookies'), 401
        return jsonify(UserView(current_user).get_one(current_user))

    user = User.get_by_username(username=username)
    if not user:
        return jsonify(msg='user not found'), 404
    return jsonify(UserView(current_user).get_one(user))


@user_account.route('/confirm_email/<string:token>')
def confirm_email(token: str):
    user = User.verify_token(token, 'confirm_email')
    if not user:
        return jsonify(msg='Wrong token'), 400

    user.verify_email()
    return jsonify(msg='Your email has been confirmed.')


@user_account.route('/reset_password/<string:token>', methods=['POST'])
@jwt_required(optional=True)
def reset_password(token: str):
    current_identity = get_jwt_identity()
    if current_identity:
        return jsonify(msg='user is already authenticated'), 403

    request_data = request.get_json()
    user = User.verify_token(token, 'reset_password')
    if not user:
        return jsonify(msg='Wrong token'), 400

    new_pwd = request_data.get('pwd')
    new_pwd_repeat = request_data.get('pwd_repeat')
    if new_pwd == new_pwd_repeat:
        user.set_pwd(new_pwd)
        return jsonify(msg='Your password has been reset.')
    return jsonify(msg='passwords must match'), 400


@user_account.route('/locations', methods=["GET"])
@jwt_required()
def get_locations():
    return jsonify(LocationView(current_user).get_list(current_user.locations))


@user_account.route('/create_location', methods=["POST"])
@jwt_required()
def create_location():
    request_data = request.get_json()
    location = Location(request_data, current_user)
    return jsonify(msg='Location created.', data=LocationView(current_user).get_one(location))


@user_account.route('/location/<int:location_id>', methods=["GET", "POST", "DELETE"])
@jwt_required()
def modify_location(location_id: int):
    location = Location.validate_id_to_user(location_id, current_user)
    if not location:
        return jsonify(msg='Not allowed'), 403

    if request.method == 'GET':
        return jsonify(LocationView(current_user).get_one(location))

    if request.method == 'POST':
        location.update(request.get_json())
        return jsonify(msg='Location updated', data=LocationView(current_user).get_one(location))

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
