from flask import Blueprint

from .not_found_page import NotFoundPage


web_core_bp = Blueprint("web_core", __name__, template_folder="templates")

web_core_bp.add_url_rule(
    NotFoundPage.PATH, view_func=NotFoundPage.as_view("not_found_page")
)
