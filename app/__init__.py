import os
import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask_wtf.csrf import CSRFProtect


from .blueprints import resources, about, maps, objectives
if os.environ.get("POSTGRES_URL", None) is not None:
    from .database import (
        db_session,
        query_electrified_km,
        query_mapped_villages,
        query_mapped_buildings,
        PROGRESS_NUMBER_MAX,
        query_gauge_maximum
    )
else:
    db_session = None

    def query_se4all_numbers():
        return 1

templates_dir = os.path.join(os.path.abspath(os.curdir), "app", "templates")


db = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))

from . import auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        static_folder='static',
        instance_relative_config=True,
    )
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # add CSRF token
    csrf = CSRFProtect(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

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



    # register blueprints (like views in django)
    app.register_blueprint(resources.bp)
    app.register_blueprint(objectives.bp)
    app.register_blueprint(maps.bp)
    app.register_blueprint(about.bp)
    app.register_blueprint(auth.bp)

    @app.route('/')
    @login_required
    def landing():

        kwargs = {}
        if os.environ.get("POSTGRES_URL", None) is not None:
            for k, desc in PROGRESS_NUMBER_MAX.items():
                kwargs[k] = query_gauge_maximum(desc)

            kwargs['km_electricity'] = query_electrified_km()
            kwargs['mapped_villages'] = query_mapped_villages()
            kwargs['mapped_buildings'] = query_mapped_buildings()

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

        return render_template('landing/index.html', **kwargs)

    @app.route('/termsofservice')
    def termsofservice():
        return render_template('termsofservice.html')

    @app.route('/privacypolicy')
    def privacypolicy():
        return render_template('privacypolicy.html')

    @app.route('/about-map')
    def about_map():
        return render_template('credits.html', about_map=True)

    @app.route('/developed-by')
    def developed_by():
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
