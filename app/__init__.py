import os
import datetime
import warnings
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import DBAPIError

from .blueprints import resources, about, maps, objectives

# By default we assume pessimistically that the database is down
DB_UP = "1"
DB_DOWN = "0"
os.environ["DB_STATUS"] = DB_DOWN
db_session = None

if os.environ.get("POSTGRES_URL", None) is not None:

    try:
        from .database import (
            db_session,
            query_electrified_km,
            query_mapped_villages,
            query_mapped_buildings,
            PROGRESS_NUMBER_MAX,
            query_gauge_maximum
        )

        os.environ["DB_STATUS"] = DB_UP
    except DBAPIError as e:
        warnings.warn(repr(e))





templates_dir = os.path.join(os.path.abspath(os.curdir), "app", "templates")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        static_folder='static',
        instance_relative_config=True,
    )
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # add CSRF token
    csrf = CSRFProtect(app)

    # register blueprints (like views in django)
    app.register_blueprint(resources.bp)
    app.register_blueprint(objectives.bp)
    app.register_blueprint(maps.bp)
    app.register_blueprint(about.bp)

    @app.route('/')
    def landing():

        kwargs = {}
        if os.environ.get("DB_STATUS") == DB_UP:
            try:
                kwargs["DB_STATUS"] = "up"
                for k, desc in PROGRESS_NUMBER_MAX.items():
                    kwargs[k] = query_gauge_maximum(desc)

                kwargs['km_electricity'] = query_electrified_km()
                kwargs['mapped_villages'] = query_mapped_villages()
                kwargs['mapped_buildings'] = query_mapped_buildings()
            except DBAPIError as e:
                kwargs["DB_STATUS"] = "down"
                warnings.warn(repr(e))
        else:
            kwargs["DB_STATUS"] = "down"

        if os.path.exists(os.path.join(templates_dir, "maps", "sidebar_checkbox.html")):
            kwargs['website_app'] = True
        else:
            kwargs['website_app'] = False
            print("\n\n*** warning ***\n")
            print(
                "The webmap will not be able to work correctly because it is missing a file, "
                "please run 'python app/setup_maps.py'"
            )
            print("\n***************\n\n")


        user_agent = request.headers.get('User-Agent')
        not_supported = False
        if user_agent is None or not isinstance(user_agent, str):
            not_supported = True
        else:
            for ua in maps.UNSUPPORTED_USER_AGENT_STRINGS:
                if ua in user_agent:
                    not_supported = True
        kwargs['not_supported'] = not_supported
        kwargs['website_welcome_video_id'] = "D37icUKT3LQ"
        return render_template('landing/index.html', **kwargs)

    @app.route('/termsofservice')
    def termsofservice():
        return render_template('termsofservice.html')

    @app.route('/privacypolicy')
    def privacypolicy():
        return render_template('privacypolicy.html')

    @app.route('/about-map')
    def about_map():
        return render_template('credits.html', about_map=True, video_id=maps.VIDEO_ID)

    @app.route('/accreditation')
    def accreditation():
        return render_template('credits.html', about_map=False)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if db_session is not None:
            db_session.remove()

    # set a global variable to indicate it is the website
    app.jinja_env.globals.update(nesp2_website=True)
    app.jinja_env.globals.update(current_year=datetime.datetime.today().year)

    try:
        from .maps_utils import define_function_jinja
        define_function_jinja(app)
    except ModuleNotFoundError:
        print("\n\n*** warning ***\n")
        print(
            "The webmap will not be able to work correctly, please run 'python "
            "app/setup_maps.py'"
        )
        print("\n***************\n\n")
    except ImportError:
        print("\n\n*** warning ***\n")
        print(
            "The webmap will not be able to work correctly, you are missing the function "
            "'define_function_jinja' into the app/maps_utils.py file, please run 'python "
            "app/setup_maps.py'"
        )
        print("\n***************\n\n")

    return app
