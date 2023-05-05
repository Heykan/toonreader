from app import app
from app.views import bp

app.register_blueprint(bp)