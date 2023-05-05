from flask import Flask, session
from app.views import bp
from app.controllers.user import UserController


@bp.route('/register', methods=['GET', 'POST'])
@bp.route('/register/', methods=['GET', 'POST'])
def register():
    user_controller = UserController()
    return user_controller.register_user()

@bp.route('/login', methods=['GET', 'POST'])
@bp.route('/login/', methods=['GET', 'POST'])
def login():
    user_controller = UserController()
    return user_controller.login_user()

@bp.route('/logout')
@bp.route('/logout/')
def logout():
    user_controller = UserController()
    return user_controller.logout_user()

@bp.route('/settings')
@bp.route('/settings/')
def setting():
    user_controller = UserController()
    return user_controller.setting_user()