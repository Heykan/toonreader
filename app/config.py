from flask import url_for
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SITE_NAME = 'ToonReader'
    DATABASE = 'database.db'
    UPLOAD_FOLDER = 'app/static/uploads'
