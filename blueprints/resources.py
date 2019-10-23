from flask import Blueprint, render_template

bp = Blueprint('resource', __name__)


@bp.route('/resources')
def resources():
    return render_template('resources/index.html')
