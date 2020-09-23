from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

# define global variables here
db = SQLAlchemy()


def create_app():
    package_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    templates = os.path.join(
        package_dir, "templates"
    )

    app = Flask('this is a simple web application', template_folder=templates)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    from qa327.backend import backend
    app.register_blueprint(backend)
    from qa327.frontend import frontend
    app.register_blueprint(frontend)

    return app
