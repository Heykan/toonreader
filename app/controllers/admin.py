from flask import render_template, request, request, session, current_app
from app.models.user import User, UserModel
from werkzeug.utils import secure_filename
from app.models.manga import Manga, MangaModel
from app.models.chapter import Chapter, ChapterModel
from app.models.comment import Comment, CommentModel
from bs4 import BeautifulSoup
import os, requests

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FOLDER = '/mangas'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, new_filename, subfolder):
    if file and allowed_file(file.filename):
        os.makedirs(os.path.join(current_app.config.get('UPLOAD_FOLDER') + FOLDER, subfolder), exist_ok=True)
        file.save(os.path.join(current_app.config.get('UPLOAD_FOLDER') + FOLDER, subfolder, new_filename))
        return True
    else:
        return False
    
def save_file_from_url(url, new_filename, manga_name, chapter_number):
    if allowed_file(new_filename):
        folder_path = os.path.join(current_app.config.get('UPLOAD_FOLDER') + FOLDER, manga_name, f'Chapitre {chapter_number}')
        os.makedirs(folder_path, exist_ok=True)
        filepath = os.path.join(folder_path, new_filename)

        with open(filepath, 'wb') as f:
            response = requests.get(url)
            f.write(response.content)

        return True
    else:
        return False

class AdminController:
    def __init__(self):
        self.manga_model = MangaModel()
        self.user_model = UserModel()
        self.chapter_model = ChapterModel()
        self.comment_model = CommentModel()
    
    def logged_admin(self):
        user = None
        if 'user_id' in session:
            user = self.user_model.get_user_by_id(session['user_id'])
        if user == None or (user and user.mod < 1):
            return render_template('error/404.html', user=user), 404
        return render_template('admin/index.html', user=user)
    
    def add_new_manga(self):
        user = None
        if 'user_id' in session:
            user = self.user_model.get_user_by_id(session['user_id'])
        if user == None or (user and user.mod != 1):
                return render_template('error/404.html', user=user), 404

        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            banner = ""
            cover = ""
            if 'cover' in request.files:
                cover_file = request.files['cover']
            if 'banner' in request.files:
                banner_file = request.files['banner']

            if self.manga_model.get_manga_by_name(name) != None:
                error_message = "Un manga du même nom existe déjà."
                return render_template('admin/add_toon.html', user=user, error_message=error_message)
            
            if cover_file:
                filename = secure_filename(cover_file.filename)
                ext = os.path.splitext(filename)[1]
                new_filename = "cover" + ext
                if save_file(cover_file, new_filename, f'{name}') == False:
                    error_message = "Erreur dans l'enregistrement de la couverture."
                    return render_template('admin/add_toon.html', user=user, error_message=error_message)
                cover = new_filename

            if banner_file:
                filename = secure_filename(banner_file.filename)
                ext = os.path.splitext(filename)[1]
                new_filename = "banner" + ext
                if save_file(banner_file, new_filename, f'{name}') == False:
                    error_message = "Erreur dans l'enregistrement de la bannière."
                    return render_template('admin/add_toon.html', user=user, error_message=error_message)
                banner = new_filename
            
            manga = Manga(0, name, description, banner, cover, "", "", "14/04/2023", "", "")
            self.manga_model.add_manga(manga)
            error_message = "Le manga à été ajouté avec succès."
            return render_template('admin/add_toon.html', user=user, error_message=error_message)
        return render_template('admin/add_toon.html', user=user)
    
    def edit_manga(self, manga_id):
        user = None
        if 'user_id' in session:
            user = self.user_model.get_user_by_id(session['user_id'])
        if user == None or (user and user.mod != 1):
                return render_template('error/404.html', user=user), 404
        
        mangas = self.manga_model.list_mangas()
        if request.method == 'POST':
                return self.add_chapter(user, mangas)
        return render_template('admin/manage_manga.html', user=user, mangas=mangas)
        
    def add_chapter(self, user, mangas):
        manga = self.manga_model.get_manga_by_id(request.form['manga_id'])
        # URL du site à analyser
        # name = manga.name.lower().replace(' ', '-')
        chapter_number = request.form['chapter_number']
        url = request.form['chapter_link']

        if manga == None or chapter_number == None:
            error = "Erreu lors de la récupération du manga."
            return render_template('admin/manage_manga.html', user=user, mangas=mangas, error=error)

        if self.chapter_model.get_chapter_by_number(manga, chapter_number) != None:
            error = "Le chapitre existe déjà."
            return render_template('admin/manage_manga.html', user=user, mangas=mangas, error=error)

        # Envoyer une requête HTTP pour récupérer le contenu HTML
        response = requests.get(url)

        # Analyser le HTML pour extraire les URLs des images
        soup = BeautifulSoup(response.content, 'html.parser')
        img_div = soup.find('div', {'class': 'reading-content'})
        if img_div == None:
            img_div = soup.find('div', {'id': 'readerarea'})
        if img_div == None:
            error = "Impossible de récupérer les images."
            return render_template('admin/manage_manga.html', user=user, mangas=mangas, error=error)
        
        img_urls = [img['src'] for img in img_div.find_all('img')]
        if len(img_urls) <= 0:
            error = "Auncun lien trouvé pour les images."
            return render_template('admin/manage_manga.html', user=user, mangas=mangas, error=error)


        for i, url in enumerate(img_urls):
            url_modified = url.replace('\t', '').replace('\n', '')
            extension = url.split('.')[-1]
            filename = f"{i+1}.{extension}"
            save_file_from_url(url=url_modified, new_filename=filename, manga_name=manga.name, chapter_number=chapter_number)

        chapter = Chapter(0, f'Chapitre {chapter_number}', chapter_number, True, manga.id)
        self.chapter_model.add_chapter(chapter)

        return render_template('admin/manage_manga.html', user=user, mangas=mangas, success=True)