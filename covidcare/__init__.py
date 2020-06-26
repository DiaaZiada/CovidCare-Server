from flask import Flask
from covidcare.config import Config
import os
from py2neo import Graph
from covidcare.models import graph


try:
    graph.schema.create_uniqueness_constraint("AppInfo", "id")
    graph.schema.create_uniqueness_constraint("LocationTime", "hash")
except:
    pass

def create_app(config_class=Config):
    app = Flask(__name__)# app.config.from_object(Config)
    from covidcare.routes import routes
    app.register_blueprint(routes)
    return app