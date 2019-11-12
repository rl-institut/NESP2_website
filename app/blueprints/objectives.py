from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('objectives', __name__)


@bp.route('/objectives/')
@bp.route('/objectives')
@login_required
def index():
    return render_template("objectives/index.html")


