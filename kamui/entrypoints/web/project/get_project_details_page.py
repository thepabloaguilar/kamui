from uuid import UUID

from flask import render_template
from flask.views import View


class GetProjectDetailsPage(View):
    PATH = "/projects/<uuid:project_id>"
    methods = ["GET"]

    def dispatch_request(self, project_id: UUID):
        return render_template("project_details_page.html")
