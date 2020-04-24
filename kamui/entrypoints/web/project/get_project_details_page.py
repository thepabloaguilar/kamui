from typing import Union
from uuid import UUID

from flask import render_template, redirect, url_for
from flask.views import View
from werkzeug import Response

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.project import Project
from kamui.core.usecase.failure import FailureDetails
from kamui.core.usecase.project.get_project_details import (
    GetProjectDetailsUsecase,
    ProjectDetails,
)


class GetProjectDetailsPage(View):
    PATH = "/projects/<uuid:project_id>"
    methods = ["GET"]

    def __init__(self) -> None:
        self.__get_project_details: GetProjectDetailsUsecase = di_container.resolve(
            GetProjectDetailsUsecase
        )

    def dispatch_request(self, project_id: UUID):  # type: ignore
        return (
            self.__get_project_details(project_id)
            .map(self.__process_success)
            .fix(self.__process_failure)
            .unwrap()
        )

    def __process_success(self, project_details: Union[ProjectDetails, Project]) -> str:
        return render_template(
            "project_details_page.html", project_details=project_details
        )

    def __process_failure(self, failure_details: FailureDetails) -> Response:
        # TODO: verify if the failure is in fact a "NOT_FOUND" failure
        return redirect(url_for("web_core.not_found_page"))
