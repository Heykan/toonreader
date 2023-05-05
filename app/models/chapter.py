from app import database

class Chapter():
    def __init__(self, id, title, number, visible, manga_id):
        self.id = id
        self.title = title
        self.number = number
        self.visible = visible
        self.manga_id = manga_id

class ChapterModel():
    def __init__(self):
        self.conn = database.get_db()
    
    def add_chapter(self, chapter):
        query = "INSERT INTO chapitre (title, number, visible, manga_id) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (chapter.title, chapter.number, chapter.visible, chapter.manga_id))
        self.conn.commit()

    def get_chapter_by_number(self, manga, number):
        query = "SELECT * FROM chapitre WHERE number = ? AND manga_id = ?"  
        result = self.conn.execute(query, (number, manga.id))
        row = result.fetchone()
        if row is None:
            return None
        chapter_info = row[:5]
        return Chapter(*chapter_info)
    
    def get_chapter_by_id(self, id):
        query = "SELECT * FROM chapitre WHERE id = ?"  
        result = self.conn.execute(query, (id,))
        row = result.fetchone()
        if row is None:
            return None
        chapter_info = row[:5]
        return Chapter(*chapter_info)
    
    def get_chapter_by_title(self, manga, title):
        query = "SELECT * FROM chapitre WHERE LOWER(title) = LOWER(?) AND manga_id = ?"  
        result = self.conn.execute(query, (title, manga.id))
        row = result.fetchone()

        if row is None:
            return None
        chapter_info = row[:5]
        return Chapter(*chapter_info)
    
    def get_chapter_by_manga_id(self, manga_id):
        query = "SELECT * FROM chapitre WHERE manga_id = ?"  
        result = self.conn.execute(query, (manga_id,))
        rows = result.fetchall()

        if rows is None:
            return None
        
        chapters = []
        for row in rows:
            chapter_info = row[:5]
            chapter = Chapter(*chapter_info)
            chapters.append(chapter)
        return chapters