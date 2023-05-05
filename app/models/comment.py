from app import database
from app.models.user import User, UserModel
from app.models.chapter import Chapter, ChapterModel
from datetime import datetime

class Comment():
    def __init__(self, id, user_id, comment, chapter_id, manga_id, date):
        self.id = id
        self.user_id = user_id
        self.comment = comment
        self.chapter_id = chapter_id
        self.manga_id = manga_id,
        self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        self.date_text = self.temps_ecoule(self.date)
        self.user = None
        self.chapter = None

    def temps_ecoule(self, date_reference):
        maintenant = datetime.now()
        difference = maintenant - date_reference
        # Formatage du temps écoulé
        if difference.days < 2 and difference.days > 0:
            temps_ecoule = f"Il y a {difference.days} jour"# et {difference.seconds//3600} heure(s)"
        elif difference.days >= 2:
            temps_ecoule = f"Il y a {difference.days} jours"# et {difference.seconds//3600} heure(s)"
        else:
            if difference.seconds//3600 < 1:
                if (difference.seconds//60)%60 < 2:
                    temps_ecoule = f"Il y a {(difference.seconds//60)%60} minute"
                else:
                    temps_ecoule = f"Il y a {(difference.seconds//60)%60} minutes"
            else:
                if difference.seconds//3600 < 2:
                    temps_ecoule = f"Il y a {difference.seconds//3600} heure"# et {(difference.seconds//60)%60} minute(s)"
                else:
                    temps_ecoule = f"Il y a {difference.seconds//3600} heures"# et {(difference.seconds//60)%60} minute(s)"
        return temps_ecoule
    
class CommentModel():
    def __init__(self):
        self.conn = database.get_db()
    
    def add_comment(self, user_id, comment, chapter_id, manga_id, date):
        query = "INSERT INTO comments (user_id, comment, chapter_id, manga_id, date) VALUES (?, ?, ?, ?, ?)"
        self.conn.execute(query, (user_id, comment, chapter_id, manga_id, date))
        self.conn.commit()
    
    def get_comments_by_manga_id(self, manga_id):
        query = "SELECT * FROM comments WHERE manga_id = ? ORDER BY date DESC LIMIT 5"  
        result = self.conn.execute(query, (manga_id,))
        rows = result.fetchall()

        comments = []
        current_comment = None
        for row in rows:
            if current_comment is None or current_comment.id != row[0]:
                # Nouveau manga
                comment_info = row[:6]
                current_comment = Comment(*comment_info)
                um = UserModel()
                current_comment.user = um.get_user_by_id(current_comment.user_id)
                current_comment.chapter = ChapterModel().get_chapter_by_id(current_comment.chapter_id)
                comments.append(current_comment)
            
        return comments
    
    def get_comments_by_chapter_id(self, chapter_id):
        query = "SELECT * FROM comments WHERE chapter_id = ? ORDER BY date DESC"  
        result = self.conn.execute(query, (chapter_id,))
        rows = result.fetchall()

        comments = []
        current_comment = None
        for row in rows:
            if current_comment is None or current_comment.id != row[0]:
                # Nouveau manga
                comment_info = row[:6]
                current_comment = Comment(*comment_info)
                um = UserModel()
                current_comment.user = um.get_user_by_id(current_comment.user_id)
                comments.append(current_comment)
            
        return comments