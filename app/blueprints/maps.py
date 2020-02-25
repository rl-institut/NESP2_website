import os
from flask import Blueprint, render_template, abort, request, Response, jsonify
from jinja2 import TemplateNotFound

if os.environ.get("POSTGRES_URL", None) is not None:
    from ..database import get_state_codes, query_random_og_cluster

    STATE_CODES_DICT = get_state_codes()

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


@bp.route('/filter-cluster', methods=["POST"])
def filter_clusters():

    state_name = request.form.get("state_name")
    if os.environ.get("POSTGRES_URL", None) is not None:
        resp = jsonify(query_random_og_cluster(state_name, STATE_CODES_DICT))
    else:
        resp=jsonify("dummy data")
    resp.status_code = 200
    return resp
