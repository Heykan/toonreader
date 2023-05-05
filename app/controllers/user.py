from flask import render_template, request, redirect, url_for, session
import bcrypt
from app.models.user import User, UserModel
from app import bcrypt

class UserController:
    def __init__(self):
        self.model = UserModel()

    def register_user(self):
        if 'user_id' in session:
            return redirect(url_for('views.home'))
        
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm-password']

            if self.model.get_user_by_email(email) != None:
                error_message = "L'adresse email est déjà utilisé."
                return render_template('user/register.html', username=username, error_message=error_message)
            
            if self.model.get_user_by_username(username) != None:
                error_message = "Le nom d'utilisateur existe déjà."
                return render_template('user/register.html', email=email, error_message=error_message)
            
            if password != confirm_password:
                error_message = "Les deux mot de passe ne correspondent pas."
                return render_template('user/register.html', username=username, email=email, error_message=error_message)
            
            hashed_password = bcrypt.generate_password_hash(password)
            
            user = User(0, username, hashed_password, email)
            self.model.add_user(user)

            user = self.model.get_user_by_username(username)
            session['user_id'] = user.id
            return redirect(url_for('views.home'))
        return render_template('user/register.html')
    
    def login_user(self):
        if 'user_id' in session:
            return redirect(url_for('views.home'))
        
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = self.model.get_user_by_username(username)
            if user is None or bcrypt.check_password_hash(user.password, password) is False:
                error_message = 'Utilisateur ou mot de passe incorrect.'
                return render_template('user/login.html', error_message=error_message)
            
            session["user_id"] = user.id
            return redirect(url_for('views.home'))
        
        return render_template('user/login.html')
    
    def logout_user(self):
        session.clear()
        return redirect(url_for('views.home'))
    
    def setting_user(self):
        user = None
        if 'user_id' in session:
            user = self.model.get_user_by_id(session['user_id'])
            
        return render_template('user/setting.html', user=user)
