import os

import flask
from flask_bootstrap import Bootstrap
import db
import homepage
import predict
import logging

LOG_REQUEST_ID_FRAMEWORK_SUPPORT=flask

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

    app.logger = create_logger()
    
    db.init_app(app)
    app.register_blueprint(homepage.bp)
    app.register_blueprint(predict.bp)

    bootstrap = Bootstrap(app)
    
    return app

def make_config(app: flask.Flask):
    pass


def create_logger() -> logging.Logger:
    lg = logging.getLogger(__name__)
    lg.setLevel(logging.DEBUG)
    
    # настройка обработчика и форматировщика для logger2
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f"{__name__}.log", mode='a')
    
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    
    # добавление обработчика к логгеру
    lg.addHandler(file_handler)
    lg.addHandler(stream_handler)

    return lg

if __name__ == '__main__':
    app = create_app()  
    app.run(host='0.0.0.0', debug=True)  
