from flask import Blueprint

bp = Blueprint('views', __name__)

from .home import *
from .user import *
from .error import *
from .admin import *
from .manga import *