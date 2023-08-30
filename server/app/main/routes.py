from flask import render_template, jsonify

from . import main


@main.route('/')
def index():
    """Index page view"""
    return render_template('index.html')


@main.route('/api/test', methods=["GET"])
def test():
    return jsonify(
        status='OK',
        msg='hello'
    )
