from flask import Blueprint
from flask_restful import Api

rest_topic_bp = Blueprint("rest_topic", __name__)
rest_topic_api = Api(rest_topic_bp, prefix="/api")
