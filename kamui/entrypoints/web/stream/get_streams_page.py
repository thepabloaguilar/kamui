from flask import render_template
from flask.views import View

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.stream import StreamList
from kamui.core.usecase.stream import GetStreamsUsecase


class GetStreamsPage(View):
    PATH = "/streams"
    methods = ["GET"]

    def __init__(self) -> None:
        self.__get_streams: GetStreamsUsecase = di_container.resolve(GetStreamsUsecase)

    def dispatch_request(self) -> str:  # type: ignore
        return self.__get_streams().map(self.__process_success).unwrap()

    def __process_success(self, streams: StreamList) -> str:
        return render_template("streams_page.html", streams=streams)
