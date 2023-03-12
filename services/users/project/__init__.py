import os
# import sys
# import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

# app_settings = os.getenv('APP_SETTINGS')
# app.config.from_object('project.config.DevelopmentConfig')

db = SQLAlchemy()
toolbar = DebugToolbarExtension()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)

    # register blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})

    # print(app.config, file=sys.stderr)
    return app
