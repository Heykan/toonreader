from app.views import bp
from app.controllers.admin import AdminController
from app.controllers.manga import MangaController

@bp.route('/admin')
@bp.route('/admin/')
def admin():
    admin_controller = AdminController()
    return admin_controller.logged_admin()

@bp.route('/add-manga', methods=['GET', 'POST'])
@bp.route('/add-manga/', methods=['GET', 'POST'])
def add_manga():
    admin_controller = AdminController()
    return admin_controller.add_new_manga()

@bp.route('/edit-manga', methods=['GET', 'POST'])
@bp.route('/edit-manga/<int:manga_id>', methods=['GET', 'POST'])
@bp.route('/edit-manga/', methods=['GET', 'POST'])
@bp.route('/edit-manga/<int:manga_id>/', methods=['GET', 'POST'])
def edit_manga(manga_id=None):
    admin_controller = AdminController()
    return admin_controller.edit_manga(manga_id)
