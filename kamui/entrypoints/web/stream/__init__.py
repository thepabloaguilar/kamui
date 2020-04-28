from flask import Blueprint

from .get_create_new_stream_from_topic_page import GetCreateNewStreamPage


web_stream_bp = Blueprint("web_stream", __name__, template_folder="templates")

web_stream_bp.add_url_rule(
    GetCreateNewStreamPage.PATH,
    view_func=GetCreateNewStreamPage.as_view("web_get_create_new_stream_page"),
)
