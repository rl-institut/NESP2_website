from flask import Blueprint, render_template

bp = Blueprint('objectives', __name__)


@bp.route('/objectives/')
@bp.route('/objectives')
def index():
    return render_template("objectives/index.html")


