from views import blueprint
from flask import Flask
from flask_cors import CORS

def create_flask_app(name):
    app = Flask(name)

    CORS(app)

    app.register_blueprint(blueprint)
    return app

app = create_flask_app(__name__)