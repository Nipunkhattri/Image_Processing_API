from flask import Blueprint
from flask_restx import Api
from views.image import image_api

blueprint = Blueprint("api","Object Detection Api")
api = Api(blueprint,title='Apis',version="1.0",description="Api")

api.add_namespace(image_api)