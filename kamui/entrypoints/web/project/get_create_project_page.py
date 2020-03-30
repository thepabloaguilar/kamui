from flask import render_template
from flask.views import View

from .forms.create_project_form import CreateProjectForm


class GetCreateProjectPage(View):
    PATH = "/projects/create"
    methods = ["GET"]

    def dispatch_request(self):
        create_project_form = CreateProjectForm()
        return render_template("create_project_page.html", form=create_project_form)
