from flask import render_template, request, redirect, url_for, session
from app.models.user import User, UserModel

class ErrorController:
    def __init__(self):
        self.user_model = UserModel()
    
    def error(self):
        user = None
        if 'user_id' in session:
            user = self.user_model.get_user_by_id(session['user_id'])
        return render_template('error/404.html', user=user)
