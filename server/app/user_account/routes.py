from flask import request, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from . import user_account
from server.app.models.models import get_user_by_username
from ..models import models
from ...utils.hider import get_hidden_email, get_hidden_pwd
from ...utils.mail_utils import send_password_reset_email


@user_account.route('/api/login', methods=["POST"])
def login():
    request_data = request.get_json()
    user = get_user_by_username(request_data.get('username'))
    if user and user.check_password(request_data.get('pwd')):
        rm = request_data.get('remember')
        login_user(user, remember=rm)

        return jsonify(
            status='OK',
            msg='success',
            data=dict(
                token='user_token',
            )
        )
    return jsonify(
        status='ERR',
        msg='user not found',
    )


@user_account.route('/api/registration', methods=["POST"])
def registration():
    request_data = request.get_json()
    user = models.create_user(request_data)
    if user:
        # send_email_confirmation_mail(user)
        return jsonify(
            status='OK',
            msg='Проверьте вашу почту и следуйте инструкциям для её подтверждения',
        )
    return jsonify(
        status='ERR',
        msg='username is not allowed',
    )


@user_account.route('/api/reset_password_request', methods=['POST'])
def reset_password_request():
    request_data = request.get_json()
    if current_user.is_authenticated:
        return jsonify(
            status='ERR',
            msg='user is already authenticated',
        )
    user = models.get_user_by_username(request_data.get('username'))
    if user:
        send_password_reset_email(user)
        return jsonify(
            status='OK',
            msg='Проверьте вашу почту и следуйте инструкциям для сброса пароля',
        )
    return jsonify(
        status='ERR',
        msg='user not found',
    )


@user_account.route('/api/profile_settings')
@login_required
def profile_settings():
    """view of `profile` page"""
    return jsonify(
        status='OK',
        msg='success',
        data=dict(
            username=current_user.username,
            full_name=current_user.full_name,
            email=get_hidden_email(current_user.email),
            phone=current_user.phone,
            contacts=current_user.contacts,
            is_email_verified=current_user.is_email_verified,
            pwd=get_hidden_pwd(),
        )
    )


@user_account.route('/api/confirm_email/<string:token>')
def confirm_email(token):
    user = models.User.verify_token(token, 'confirm_email')
    if not user:
        return jsonify(
            status='ERR',
            msg='user not found',
        )
    user.verify_email()
    return jsonify(
        status='OK',
        msg='Your email has been confirmed.',
    )


@user_account.route('/api/reset_password/<string:token>', methods=['POST'])
def reset_password(token):
    request_data = request.get_json()
    if current_user.is_authenticated:
        return jsonify(
            status='ERR',
            msg='user is already authenticated',
        )
    user = models.User.verify_token(token, 'reset_password')
    if not user:
        return jsonify(
            status='ERR',
            msg='user not found',
        )

    user.set_pwd(request_data.get('new_pwd'))
    return jsonify(
        status='OK',
        msg='Your password has been reset.',
    )


@user_account.route("/api/logout")
@login_required
def logout():
    """
    view of `logout` page
    logs out user
    """
    logout_user()
    return jsonify(
        status='OK',
        msg='user logout',
    )
