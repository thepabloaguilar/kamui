from flask import render_template
from flask.views import View


class NotFoundPage(View):
    PATH = "/not-found"

    def dispatch_request(self) -> str:  # type: ignore
        return render_template("not_found.html")
