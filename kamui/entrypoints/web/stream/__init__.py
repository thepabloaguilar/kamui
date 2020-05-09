from flask import Blueprint

from .get_create_new_stream_from_stream_page import GetCreateNewStreamFromStreamPage
from .get_create_new_stream_from_topic_page import GetCreateNewStreamFromTopicPage
from .get_streams_page import GetStreamsPage
from .get_stream_details_page import GetStreamDetailsPage


web_stream_bp = Blueprint("web_stream", __name__, template_folder="templates")

web_stream_bp.add_url_rule(
    GetCreateNewStreamFromTopicPage.PATH,
    view_func=GetCreateNewStreamFromTopicPage.as_view(
        "web_get_create_new_stream_from_topic_page"
    ),
)
web_stream_bp.add_url_rule(
    GetCreateNewStreamFromStreamPage.PATH,
    view_func=GetCreateNewStreamFromStreamPage.as_view(
        "web_get_create_new_stream_from_stream_page"
    ),
)
web_stream_bp.add_url_rule(
    GetStreamsPage.PATH, view_func=GetStreamsPage.as_view("web_get_streams_page")
)
web_stream_bp.add_url_rule(
    GetStreamDetailsPage.PATH,
    view_func=GetStreamDetailsPage.as_view("web_get_stream_details_page"),
)
