from typing import Union
from uuid import UUID

from flask import render_template, redirect, url_for
from flask.views import View
from werkzeug import Response

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.stream import Stream
from kamui.core.usecase.failure import FailureDetails
from kamui.core.usecase.stream import GetStreamDetailsUsecase
from kamui.core.usecase.stream.get_stream_details import StreamDetails


class GetStreamDetailsPage(View):
    PATH = "/streams/<uuid:stream_id>"
    methods = ["GET"]

    def __init__(self) -> None:
        self.__get_stream_details: GetStreamDetailsUsecase = di_container.resolve(
            GetStreamDetailsUsecase
        )

    def dispatch_request(self, stream_id: UUID) -> Union[str, Response]:  # type: ignore
        return (
            self.__get_stream_details(stream_id)
            .map(self.__process_success)
            .fix(self.__process_failure)
            .unwrap()
        )

    def __process_success(self, stream_details: Union[StreamDetails, Stream]) -> str:
        return render_template(
            "stream_details_page.html", stream_details=stream_details,
        )

    def __process_failure(self, failure_details: FailureDetails) -> Response:
        # TODO: verify if the failure is in fact a "NOT_FOUND" failure
        return redirect(url_for("web_core.not_found_page"))
