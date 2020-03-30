from flask import render_template, redirect, url_for
from flask.views import View

from .forms.create_project_form import CreateProjectForm
from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.project import Project
from kamui.core.entity.project_status import ProjectStatus
from kamui.core.usecase.project.create_new_project import CreateNewProjectUsecase


class CreateNewProject(View):
    PATH = "/projects/create"
    methods = ["POST"]

    def __init__(self):
        self.__create_new_project = di_container.resolve(CreateNewProjectUsecase)

    def dispatch_request(self):
        create_project_form = CreateProjectForm()
        if create_project_form.validate_on_submit():
            project_title = create_project_form.title.data
            self.__create_new_project(project_title)
            return redirect(url_for("web_project.web_get_projects_page"))
        return render_template("create_project_page.html", form=create_project_form)
