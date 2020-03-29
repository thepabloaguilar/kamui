from flask import Blueprint

from .get_home_page import GetHomePage


web_home_bp = Blueprint("web_home", __name__, template_folder="templates")

web_home_bp.add_url_rule(
    GetHomePage.PATH, view_func=GetHomePage.as_view("web_get_home_page")
)
