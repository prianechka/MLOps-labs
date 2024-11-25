import os

import flask
from flask_bootstrap import Bootstrap
from . import db, homepage, predict

def create_app(cfg: flask.Config=None):
    app = flask.Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'heart.sqlite'),
    )

    if cfg is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(cfg)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    app.register_blueprint(homepage.bp)
    app.register_blueprint(predict.bp)

    bootstrap = Bootstrap(app)
    return app

def make_config(app: flask.Flask):
    pass


