from flask import render_template, request, redirect, url_for, session, g
from app.models.user import User, UserModel
from app.models.manga import Manga, MangaModel

class HomeController:
    def __init__(self):
        self.user_model = UserModel()
        self.manga_model = MangaModel()
    
    def home(self):
        user = None
        if 'user_id' in session:
            user = self.user_model.get_user_by_id(session['user_id'])

        best_mangas = self.manga_model.get_top_mangas(3)
        return render_template('index.html', best_mangas=best_mangas, user=user)
