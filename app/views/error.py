from app.views import bp
from app.controllers.error import ErrorController
from flask import session

@bp.app_errorhandler(404)
def page_not_found(error):
    error_controller = ErrorController()
    return error_controller.error()