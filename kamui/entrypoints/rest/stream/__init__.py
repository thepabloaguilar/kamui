from flask import Blueprint
from flask_restful import Api


rest_stream_bp = Blueprint("rest_stream", __name__)
rest_stream_api = Api(rest_stream_bp, prefix="/api")
