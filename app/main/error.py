from flask import render_template
# from app import app
from . import main

# @app.errorhandler(404)
@main.app_errorhandler(404)
def four_ow_four(error):
    return render_template("fourOwfour.html"),404