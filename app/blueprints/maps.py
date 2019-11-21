from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
bp = Blueprint('maps', __name__)


@bp.route('/maps/')
@bp.route('/maps')
def index():
    try:
        return render_template('maps/index.html')
    except TemplateNotFound:
        abort(404)