from flask import Blueprint
from flask import render_template
from flask import request

from app.helpers.data import save_to_db
from app.helpers.data_getter import DataGetter
from app.models.modules import Module
from app.views.super_admin import MODULES, check_accessible

sadmin_modules = Blueprint('sadmin_modules', __name__, url_prefix='/admin/modules')


@sadmin_modules.before_request
def verify_accessible():
    return check_accessible(MODULES)


@sadmin_modules.route('/', methods=['GET', 'POST'])
def index_view():
    module = DataGetter.get_module()
    if request.method == 'GET':
        if not module:
            module = Module()
            save_to_db(module)
    elif request.method == 'POST':
        form = request.form
        module.ticket_include = True if form.get('ticketing') == 'on' else False
        module.payment_include = True if form.get('payments') == 'on' else False
        module.donation_include = True if form.get('donations') == 'on' else False
        save_to_db(module)

    return render_template('gentelella/admin/super_admin/modules/modules.html', module=module)
