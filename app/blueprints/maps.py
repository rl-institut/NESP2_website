import os
import json
from flask import Blueprint, render_template, abort, request, Response, jsonify
from jinja2 import TemplateNotFound

if os.environ.get("POSTGRES_URL", None) is not None:
    from ..database import (
        get_state_codes,
        query_random_og_cluster,
        query_filtered_clusters,
        query_filtered_og_clusters,
        query_available_og_clusters
    )
    STATE_CODES_DICT = get_state_codes()
    CODES_STATE_DICT = {v: k for k, v in STATE_CODES_DICT.items()}

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


@bp.route('/csv-export', methods=["GET"])
def download_csv():
    args = request.args
    state = args.get("state")
    cluster_type = args.get("cluster_type")
    fname = args.get("state")

    if os.environ.get("POSTGRES_URL", None) is not None:
        if "og" in cluster_type:
            fname = fname + "_remotely_mapped_settlements"
            keys = (
                'adm1_pcode',
                'cluster_offgrid_id',
                'area_km2',
                'building_count',
                'percentage_building_area',
                'grid_dist_km'
            )
            records = query_filtered_og_clusters(
                state,
                STATE_CODES_DICT,
                area=[args.get("ogmin_area"), args.get("ogmax_area")],
                distance_grid=[args.get("ogmindtg"), args.get("ogmaxdtg")],
                building=[args.get("ogminb"), args.get("ogmaxb")],
                buildingfp=[args.get("ogminbfp"), args.get("ogmaxbfp")],
                keys=keys
            )
        else:
            fname = fname + "_identified_settlements_by_satellite"
            keys = (
                'adm1_pcode',
                'cluster_all_id',
                'fid',
                'area_km2',
                'grid_dist_km'
            )
            records = query_filtered_clusters(
                state,
                STATE_CODES_DICT,
                area=[args.get("min_area"), args.get("max_area")],
                distance_grid=[args.get("mindtg"), args.get("maxdtg")],
                keys=keys
            )

        csv = list()
        csv.append(", ".join(keys))
        for line in records:
            csv.append(", ".join([str(line[k]) for k in keys]))
        csv = "\n".join(csv) + "\n"
    else:
        csv = "1,2,3\n4,5,6\n"
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename={}.csv".format(fname)}
    )

@bp.route('/states-with-og-clusters', methods=["POST"])
def available_clusters():

    # query state codes for states with og clusters data
    resp = query_available_og_clusters()
    resp = jsonify({"states_with_og_clusters": [CODES_STATE_DICT[r.lower()] for r in resp]})
    resp.status_code = 200
    return resp


@bp.route('/random-cluster', methods=["POST"])
def random_clusters():

    state_name = request.form.get("state_name")
    # query centroid with geometry as geojson
    resp = query_random_og_cluster(state_name, STATE_CODES_DICT)
    geom = json.loads(resp.pop("geom"))
    feature = dict(
        lat=geom["coordinates"][1],
        lng=geom["coordinates"][0],
        properties=resp
    )
    resp = jsonify(feature)
    resp.status_code = 200
    return resp


@bp.route('/filtered-cluster', methods=["POST"])
def filtered_clusters():
    state = request.form.get("state_name")
    cluster_type = request.form.get("cluster_type")

    if os.environ.get("POSTGRES_URL", None) is not None:
        if "og" in cluster_type:
            keys = 'cluster_offgrid_id'

            records = query_filtered_og_clusters(
                state,
                STATE_CODES_DICT,
                area=[request.form.get("ogminarea"), request.form.get("ogmaxarea")],
                distance_grid=[request.form.get("ogmindtg"), request.form.get("ogmaxdtg")],
                building=[request.form.get("ogminb"), request.form.get("ogmaxb")],
                buildingfp=[request.form.get("ogminbfp"), request.form.get("ogmaxbfp")],
                keys=keys
            )
        else:

            keys = 'cluster_all_id'
            records = query_filtered_clusters(
                state,
                STATE_CODES_DICT,
                area=[request.form.get("minarea"), request.form.get("maxarea")],
                distance_grid=[request.form.get("mindtg"), request.form.get("maxdtg")],
                keys=keys
            )

    resp = jsonify(records[0].count)
    resp.status_code = 200
    return resp

