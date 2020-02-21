from flask import Blueprint, render_template, abort, request, Response
from jinja2 import TemplateNotFound
bp = Blueprint('maps', __name__)


@bp.route('/maps/')
@bp.route('/maps')
def index():
    defaultArgs = {
        "states_content": 1,
        "grid_content": 1
    }
    if request.args == {}:
        request.args = defaultArgs

    try:
        return render_template('maps/index.html', **request.args)
    except TemplateNotFound:
        abort(404)


@bp.route('/csv-export')
def download_csv():

    print(request.args)
    args = dict(request.args)
    # TODO: perform a db search

    csv = '1,2,3\n4,5,6\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename={}.csv".format(args["state"])}
    )
