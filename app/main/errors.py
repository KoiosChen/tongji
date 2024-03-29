from flask import render_template, jsonify
from . import main


@main.app_errorhandler(403)
def page_not_found(e):
    return render_template('403.html')


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')