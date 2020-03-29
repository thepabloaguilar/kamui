from flask import render_template
from flask.views import View


class GetProjectsPage(View):
    PATH = "/projects"
    methods = ["GET"]

    def dispatch_request(self):
        return render_template("projects_page.html", projects=[])
