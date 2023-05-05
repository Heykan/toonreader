from app import app
from app.database import *

if __name__ == '__main__':
    app.run(host='::', port=80, debug=True)