from flask import render_template

from . import main
from . import models


@main.route('/')
def index():
    """view of `game` page"""
    return render_template('index.html')
