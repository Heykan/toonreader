from app import database
from app.models.user import UserModel
from app.models.chapter import Chapter, ChapterModel
from app.models.comment import Comment, CommentModel

class Manga():
    def __init__(self, id, name, description, banner, cover, type, author, release_date, status, gender, last_chapter = 0, note = 0, views = 0):
        self.id = id
        self.name = name
        self.description = description
        self.banner = banner
        self.cover = cover
        self.type = type
        self.author = author
        self.release_date = release_date
        self.status = status
        self.gender = gender
        self.last_chapter = last_chapter
        self.note = note
        self.views = views
        self.chapters = []
        self.comments = []

    def short_description(self, word_count):
        #troncate text
        words = self.description.split()
        if len(words) > word_count:
            words = words[:word_count]
            words[-1] += '...'
        return ' '.join(words)

class Gender():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MangaModel:
    def __init__(self):
        self.conn = database.get_db()

    def add_manga(self, manga):
        query = "INSERT INTO manga (name, description, banner, cover, last_chapter) VALUES (?, ?, ?, ?, ?)"
        self.conn.execute(query, (manga.name, manga.description, manga.banner, manga.cover, manga.last_chapter))
        self.conn.commit()
    
    def get_gender_by_id(self, id):
        query = "SELECT * FROM gender WHERE id = ?"  
        result = self.conn.execute(query, (id,))
        row = result.fetchone()

        if row is None:
            return None
        gender_info = row[:2]
        return Gender(*gender_info)
    
    def get_gender_by_name(self, name):
        query = "SELECT * FROM gender WHERE LOWER(name) = LOWER(?)"  
        result = self.conn.execute(query, (name,))
        row = result.fetchone()

        if row is None:
            return None
        gender_info = row[:2]
        return Gender(*gender_info)
    
    def get_manga_by_gender(self, gender):
        query = "SELECT * FROM manga WHERE INSTR('|' || gender || '|', ?) > 0"
        result = self.conn.execute(query, ('|' + str(gender) + '|',))
        rows = result.fetchall()

        mangas = []
        for row in rows:
            if row != None:
                # Nouveau manga
                manga_info = row[:13]
                current_manga = Manga(*manga_info)
                current_manga.chapters = []
                mangas.append(current_manga)

                # Ajout de la liste des chapitres à l'objet manga
                current_manga.chapters = ChapterModel().get_chapter_by_manga_id(current_manga.id)
            
                current_manga.comments = CommentModel().get_comments_by_manga_id(current_manga.id)

        return mangas

    def get_manga_by_name(self, name):
        return self.get_manga_by('name', name)
    
    def get_manga_by_id(self, id):
        return self.get_manga_by('id', id)
    
    def list_mangas(self):
        query = "SELECT * FROM manga"  
        result = self.conn.execute(query)
        rows = result.fetchall()

        mangas = []
        for row in rows:
            if row != None:
                # Nouveau manga
                manga_info = row[:13]
                current_manga = Manga(*manga_info)
                current_manga.chapters = []
                mangas.append(current_manga)

                # Ajout de la liste des chapitres à l'objet manga
                current_manga.chapters = ChapterModel().get_chapter_by_manga_id(current_manga.id)
            
                current_manga.comments = CommentModel().get_comments_by_manga_id(current_manga.id)

        return mangas
    
    def list_mangas_contains(self, search):
        query = "SELECT * FROM manga WHERE name LIKE ?"  
        result = self.conn.execute(query, ('%' + search + '%',))
        rows = result.fetchall()

        mangas = []
        for row in rows:
            if row != None:
                # Nouveau manga
                manga_info = row[:13]
                current_manga = Manga(*manga_info)
                current_manga.chapters = []
                mangas.append(current_manga)

                # Ajout de la liste des chapitres à l'objet manga
                current_manga.chapters = ChapterModel().get_chapter_by_manga_id(current_manga.id)
            
                current_manga.comments = CommentModel().get_comments_by_manga_id(current_manga.id)

        return mangas

    def get_top_mangas(self, quantity):
        query = f"SELECT * from manga ORDER BY note DESC LIMIT {quantity}"
        result = self.conn.execute(query)
        rows = result.fetchall()

        mangas = []
        current_manga = None
        for row in rows:
            if current_manga is None or current_manga.id != row[0]:
                # Nouveau manga
                manga_info = row[:12]
                current_manga = Manga(*manga_info)
                current_manga.chapters = []
                mangas.append(current_manga)

        return mangas
    
    def get_manga_by(self, query_name, value):
        if type(value) == str:
            query = f"SELECT * FROM manga m LEFT JOIN chapitre c ON m.id = c.manga_id WHERE LOWER(m.{query_name}) = LOWER(?)"
        else:
            query = f"SELECT * FROM manga m LEFT JOIN chapitre c ON m.id = c.manga_id WHERE m.{query_name} = ?"

        result = self.conn.execute(query, (value,))
        rows = result.fetchall()

        if not rows:
            return None

        # Récupération des informations du manga
        manga_info = rows[0][:13] # Les 13 premières colonnes correspondent aux informations du manga
        manga = Manga(*manga_info)

        # Création de la liste des chapitres
        chapitres = []
        for row in rows:
            if row != None:
                chapitre_info = row[13:] # Les colonnes suivant la 13ème correspondent aux informations du chapitre
                chapitre = Chapter(*chapitre_info)
                chapitres.append(chapitre)

        # Ajout de la liste des chapitres à l'objet manga
        manga.chapters = chapitres

        # on initialise les genre
        gender = manga.gender
        manga.gender = []
        genders = gender.split('|')
        for gen in genders:
            gender = self.get_gender_by_id(gen)
            manga.gender.append(gender)

        manga.comments = CommentModel().get_comments_by_manga_id(manga.id)

        # Retour de l'objet manga avec la liste des chapitres
        return manga
