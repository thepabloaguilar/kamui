from flask import render_template
from flask.views import View


class GetHomePage(View):
    PATH = "/home"
    methods = ["GET"]

    def dispatch_request(self) -> str:  # type: ignore
        return render_template("home_page.html")
