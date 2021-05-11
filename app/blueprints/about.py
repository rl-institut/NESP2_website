from flask import Blueprint, render_template

bp = Blueprint("about", __name__)


@bp.route("/about")
def about():
    # change height of the stakeholder logos such that the circles in the logos all have same
    # diameter
    logo_diameter = 200
    args = dict(
        rea_height=logo_diameter * (119.0 / 103),
        nerc_height=logo_diameter * (516.0 / 500),
        tcn_height=logo_diameter * (176.0 / 144),
        # height for green energy investment logo static
        gei_height=120,
    )
    return render_template("about.html", **args)
