from flask import Blueprint

from .get_projects_page import GetProjectsPage
from .get_create_project_page import GetCreateProjectPage
from .create_new_project import CreateNewProject
from .get_project_details_page import GetProjectDetailsPage


web_project_bp = Blueprint("web_project", __name__, template_folder="templates")

web_project_bp.add_url_rule(
    GetProjectsPage.PATH, view_func=GetProjectsPage.as_view("web_get_projects_page")
)
web_project_bp.add_url_rule(
    GetCreateProjectPage.PATH,
    view_func=GetCreateProjectPage.as_view("web_get_create_project_page"),
)
web_project_bp.add_url_rule(
    CreateNewProject.PATH, view_func=CreateNewProject.as_view("web_create_new_project")
)
web_project_bp.add_url_rule(
    GetProjectDetailsPage.PATH,
    view_func=GetProjectDetailsPage.as_view("web_get_project_details_page"),
)
