from datetime import date
from flask import Blueprint, render_template
from ..database import query_dashboard_data, query_generation_assets

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard/")
@bp.route("/dashboard")
def index():
    assets = query_generation_assets()

    gen_lat = []
    gen_lon = []
    gen_txt = []
    for ft in assets["features"]:
        lon, lat = ft["geometry"]["coordinates"]
        gen_txt.append(str(ft["properties"]["capacity_kw"]))
        gen_lat.append(lat)
        gen_lon.append(lon)

    years, cum_cap, percent_renewable, re_type = query_dashboard_data()

    year_id = years.index(date.today().year)
    current_cap_installed = int(cum_cap[year_id])
    current_percent_renewable = int(percent_renewable[year_id])

    print(f"{current_cap_installed:,}")

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

    graphs = dict(
        generation_cap=dict(
            title="Total generation capacity installed and planned",
            tooltip="Installed and planned generation capacity until 2030 based on power plants in the planning phase "
                    "and sector projections",
            data=[
                dict(
                    x=years,
                    y=cum_cap_initial,
                    type="bar",
                    marker=dict(color="#1DD069"),
                    name="Installed",
                ),
                dict(
                    x=years,
                    y=cum_cap_planned,
                    type="bar",
                    marker=dict(color="#ffbb00"),
                    name="Planned",
                ),
                dict(
                    x=[y for y in range(years[0] - 1, years[-1] + 2, 1)],
                    y=[target for y in range(years[0] - 1, years[-1] + 2, 1)],
                    type="scatter",
                    mode="lines",
                    line=dict(color="red", dash="dashdot"),
                    name="Target",
                ),
            ],
        ),
        renewables_percentage=dict(
            title="Percentage renewables installed and planned",
            tooltip="Installed and planned generation capacity as renewable share in %. Based on power plants "
                  "in the planning phase and sector projections",
            data=[
                dict(
                    x=years,
                    y=percent_renewable,
                    type="bar",
                    marker=dict(color="#1DD069"),
                    name="% renewable",
                ),
                dict(
                    x=[y for y in range(years[0] - 1, years[-1] + 2, 1)],
                    y=[30 for y in range(years[0] - 1, years[-1] + 2, 1)],
                    type="scatter",
                    mode="lines",
                    line=dict(color="red", dash="dashdot"),
                    name="Target",
                ),
            ],
        ),
        renewable_types=dict(
            title="Renewables installed by technology type",
            tooltip="Installed and planned generation capacities until 2030 seperated into technology types. Based "
                    "on power plants in the planning phase and sector projections",
            data=[
                dict(
                    x=years,  # (2020, 2030),
                    y=re_type["Hydro"],
                    type="bar",
                    marker=dict(color="#0088A0"),
                    name="Hydro",
                ),
                dict(
                    x=years,  # (2020, 2030),
                    y=re_type["PV"],
                    type="bar",
                    marker=dict(color="#FFCC15"),
                    name="PV",
                ),
                dict(
                    x=years,  # (2020, 2030),
                    y=re_type["Wind"],
                    type="bar",
                    marker=dict(color="#B91109"),
                    name="Wind",
                ),
            ],
        ),
    )
    return render_template(
        "dashboard/index.html",
        **{
            "graphs": graphs,
            "generation_assets": assets,
            "cap_installed": f"{current_cap_installed}",
            "cap_installed_txt": f"{current_cap_installed:,}",
            "cap_installed_target": "30000",
            "percent_renewable_target": "30",
            "percent_renewable": f"{current_percent_renewable}",
        }
    )
