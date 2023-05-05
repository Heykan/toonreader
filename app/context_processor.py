from flask import current_app
from app import database
from app.models.manga import Gender
import os

def file_exists(file_path):
    return os.path.exists(file_path)

def string(val):
    return str(val)

def get_genders():
        conn = database.get_db()
        query = "SELECT * FROM gender"  
        result = conn.execute(query)
        rows = result.fetchall()

        if rows is None:
            return None
        
        genders = []
        for row in rows:
            gender_info = row[:2]
            genders.append(Gender(*gender_info))

        return genders

def inject_globals():
    return dict(site_name = current_app.config.get('SITE_NAME'), 
                upload_folder = current_app.config.get('UPLOAD_FOLDER'),
                file_exists=file_exists,
                string=string,
                genders=get_genders())
