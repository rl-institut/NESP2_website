import os

from flask import Flask, render_template
try:
    from blueprints import resources, about, maps
except ModuleNotFoundError:
    from .blueprints import resources, about, maps


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
        return render_template('landing/index.html')

    @app.route('/termsofservice')
    def termsofservice():
        return render_template('termsofservice.html')

    @app.route('/privacypolicy')
    def privacypolicy():
        return render_template('privacypolicy.html')

    return app
