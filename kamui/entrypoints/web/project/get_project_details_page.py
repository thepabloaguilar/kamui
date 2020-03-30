from uuid import UUID

from flask import render_template
from flask.views import View


class GetProjectDetailsPage(View):
    PATH = "/projects/<uuid:project_key>"
    methods = ["GET"]

    def dispatch_request(self, project_key: UUID):
        return render_template("project_details_page.html")
