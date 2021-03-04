from flask import Blueprint, render_template
from ..database import query_dashboard_data

bp = Blueprint('dashboard', __name__)


@bp.route('/dashboard/')
@bp.route('/dashboard')
def index():
    years, cum_cap, percent_renewable, re_type = query_dashboard_data()

    cum_cap_initial = []
    cum_cap_planned = []
    target = 30000
    for i, c in enumerate(cum_cap):
        # if i == 0:
        cum_cap_initial.append(cum_cap[0])
        cum_cap_planned.append(c - cum_cap[0])
        # else:
        #     cum_cap_initial.append(cum_cap[i-1])
        #     cum_cap_planned.append(c - cum_cap[i-1])

    a = [1, 2, 3]
    graphs = dict(
        generation_cap=[
                           dict(x=years, y=cum_cap_initial, type="bar", marker=dict(color="#1DD069"), name="Installed"),
                           dict(x=years, y=cum_cap_planned, type="bar", marker=dict(color="#ffbb00"), name="Planned"),
                           dict(x=[years[0], years[-1]], y=[target, target], type="scatter", mode="lines", line=dict(color="red"), name="Target"),
                       ],
        renewables_percentage=dict(x=years, y=percent_renewable, type="bar", marker=dict(color="#1DD069"), name="% renewable"),
        renewable_types=[
            dict(x=(2020, 2030), y=re_type["Hydro"], type="bar", marker=dict(color="#0088A0"), name="Hydro"),
            dict(x=(2020, 2030), y=re_type["PV"], type="bar", marker=dict(color="#FFCC15"), name="PV"),
            dict(x=(2020, 2030), y=re_type["Wind"], type="bar", marker=dict(color="#B91109"), name="Wind"),
        ],
        location_plants=dict(x=a, y=a),

    )
    return render_template('dashboard/index.html', **{"graphs": graphs})
