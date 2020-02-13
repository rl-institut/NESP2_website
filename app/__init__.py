import os
from flask import Flask, render_template
try:
    from blueprints import resources, about, maps
    if os.environ.get("POSTGRES_URL", None) is not None:
        from database import (
            db_session,
            query_se4all_numbers,
            PROGRESS_NUMBER_MAX,
            query_gauge_maximum
        )
    else:
        db_session = None

        def query_se4all_numbers():
            return 1

except ModuleNotFoundError:
    from .blueprints import resources, about, maps
    if os.environ.get("POSTGRES_URL", None) is not None:
        from .database import (
            db_session,
            query_se4all_numbers,
            PROGRESS_NUMBER_MAX,
            query_gauge_maximum
        )
    else:
        db_session = None

        def query_se4all_numbers():
            return 1


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

    # register blueprints (like views in django)
    app.register_blueprint(resources.bp)
    app.register_blueprint(maps.bp)
    app.register_blueprint(about.bp)

    @app.route('/')
    def landing():

        kwargs = {}
        for k, desc in PROGRESS_NUMBER_MAX.items():
            kwargs[k] = query_gauge_maximum(desc)

        kwargs['km_electricity'] = query_se4all_numbers()
        print(kwargs)
        return render_template('landing/index.html', **kwargs)

    @app.route('/termsofservice')
    def termsofservice():
        return render_template('termsofservice.html')

    @app.route('/privacypolicy')
    def privacypolicy():
        return render_template('privacypolicy.html')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if db_session is not None:
            db_session.remove()

    return app
