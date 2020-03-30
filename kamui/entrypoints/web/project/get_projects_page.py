from flask import render_template
from flask.views import View

from kamui.core.usecase.project.get_projects_list import GetProjectsListUsecase
from kamui.configuration.dependency_injection import di_container


class GetProjectsPage(View):
    PATH = "/projects"
    methods = ["GET"]

    def __init__(self):
        self.__get_projects_list_usecase = di_container.resolve(GetProjectsListUsecase)

    def dispatch_request(self):
        projects = self.__get_projects_list_usecase()
        return render_template("projects_page.html", projects=projects)
