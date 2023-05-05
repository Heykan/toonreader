from datetime import datetime
from flask import render_template, request, redirect, url_for, session, current_app, request
from app.models.user import UserModel
from app.models.manga import MangaModel
from app.models.chapter import ChapterModel
from app.models.comment import CommentModel
import os
from natsort import natsorted

class MangaController:
    def __init__(self):
        self.manga_model = MangaModel()
        self.user_model = UserModel()
        self.chapter_model = ChapterModel()
        self.comment_model = CommentModel()
    
    def list_manga(self):
        user = None
        searching = None
        if 'user_id' in session:
            user = self.user_model.get_user_by_id(session['user_id'])
        mangas = self.manga_model.list_mangas()

        if request.method == 'POST':
            search = request.form['search-input']
            mangas = self.manga_model.list_mangas_contains(search)
            searching = True
        return render_template('manga/list.html', user=user, mangas=mangas, searching=searching)
    
    def read_manga(self, manga_name):
        user = None
        if 'user_id' in session:
            user = self.user_model.get_user_by_id(session['user_id'])
        name = manga_name.replace('-', ' ').replace('/', '')
        manga = self.manga_model.get_manga_by_name(name)
        if manga == None:
            return render_template('error/404.html', user=user), 404
        
        return render_template('manga/detail.html', user=user, manga=manga)
    
    def read_chapter(self, manga_name, chapter_title):
        user = None
        if 'user_id' in session:
            user = self.user_model.get_user_by_id(session['user_id'])

        name = manga_name.replace('-', ' ').replace('/', '')
        chapter_name = chapter_title.replace('-', ' ').replace('/', '')
        manga = self.manga_model.get_manga_by_name(name)

        if manga == None:
            return render_template('error/404.html', user=user), 404    
        chapter = self.chapter_model.get_chapter_by_title(manga, chapter_name)
        if chapter == None:
            return redirect(url_for('views.read', manga_name=manga_name))

        if request.method == 'POST':
            if user == None:
                return redirect(url_for('views.login'))
            comment = request.form['comment']
            if comment != None or (comment and comment.strip() != ""):
                self.comment_model.add_comment(user.id, comment, chapter.id, manga.id, datetime.now())
        
        comments = self.comment_model.get_comments_by_chapter_id(chapter.id)
        folder_path = os.path.join(current_app.config.get('UPLOAD_FOLDER') + '/mangas', manga.name, chapter.title)
        files = os.listdir(folder_path)

        if request.method == 'POST':
            return redirect(url_for('views.read_chapter', _anchor='comment', chapter_title=chapter_title, manga_name=manga_name))

        return render_template('manga/read.html', user=user, chapter=chapter, manga=manga, comments=comments, files=files, natsorted=natsorted)
    
    def list_category(self, name):
        user = None
        if 'user_id' in session:
            user = self.user_model.get_user_by_id(session['user_id'])
        
        if name != '4-koma':
            gender = self.manga_model.get_gender_by_name(name.replace('-', ' '))
        else:
            gender = self.manga_model.get_gender_by_name(name)

        if gender == None:
            return render_template('error/404.html', user=user)
        
        mangas = self.manga_model.get_manga_by_gender(gender.id)
        return render_template('manga/category.html', user=user, gender=gender, mangas=mangas)