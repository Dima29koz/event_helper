from flask import render_template, jsonify, request, Response

from . import main
from ...utils.route_handlers import handle_refresh_expiring_jwts


@main.after_app_request
def refresh_expiring_jwts(response):
    if request.endpoint == 'user_account.logout':
        return response
    return handle_refresh_expiring_jwts(response)


@main.before_app_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res


@main.route('/')
def index():
    """Index page view"""
    return render_template('index.html')


@main.route('/test', methods=["GET"])
def test():
    return jsonify(msg='hello')
