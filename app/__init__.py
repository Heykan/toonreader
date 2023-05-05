from flask import Flask
from app.config import Config
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)

from app import routes
from app import database
from .context_processor import inject_globals
app.context_processor(inject_globals)