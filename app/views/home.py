from app import app
from app.views import bp
from app.models.user import User
from flask import render_template, request, session, redirect, url_for
from app.controllers.home import HomeController


@bp.route('/')
def home():
    home_controller = HomeController()
    return home_controller.home()