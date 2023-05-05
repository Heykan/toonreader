from flask import Flask, session
from app.views import bp
from app.controllers.manga import MangaController

@bp.route('/manga/<string:manga_name>')
@bp.route('/manga/<string:manga_name>/')
def detail(manga_name):
    manga_controller = MangaController()
    return manga_controller.read_manga(manga_name)

@bp.route('/manga/<string:manga_name>/<string:chapter_title>', methods=['GET', 'POST'])
@bp.route('/manga/<string:manga_name>/<string:chapter_title>/', methods=['GET', 'POST'])
def read_chapter(manga_name, chapter_title):
    manga_controller = MangaController()
    return manga_controller.read_chapter(manga_name, chapter_title)

@bp.route('/manga', methods=['GET', 'POST'])
@bp.route('/manga/', methods=['GET', 'POST'])
def list_manga():
    manga_controller = MangaController()
    return manga_controller.list_manga()

@bp.route('/categories/<string:name>')
@bp.route('/categories/<string:name>/')
def category(name):
    manga_controller = MangaController()
    return manga_controller.list_category(name)