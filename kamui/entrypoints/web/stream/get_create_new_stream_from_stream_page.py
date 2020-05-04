from typing import List

from flask import render_template, request
from flask.views import View
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.stream import KSQLStream
from kamui.core.usecase.failure import FailureDetails
from kamui.core.usecase.stream.get_ksql_streams import GetKSQLStreamsUsecase


class CreateNewStreamForm(FlaskForm):
    from_stream = SelectField("Stream", choices=[])
    stream_name = StringField("Stream Name", validators=(DataRequired(),))
    stream_fields = SelectMultipleField("Stream Fields", choices=[])


class GetCreateNewStreamFromStreamPage(View):
    PATH = "/streams/create/from-stream"
    methods = ["GET"]

    def __init__(self) -> None:
        self.__get_ksql_streams = di_container.resolve(GetKSQLStreamsUsecase)

    def dispatch_request(self) -> str:  # type: ignore
        available_topic_names = self.__get_ksql_streams()
        return (  # type: ignore
            available_topic_names.map(self.__process_success_return)
            .fix(self.__process_failure_return)
            .unwrap()
        )

    def __process_success_return(self, streams: List[KSQLStream]) -> str:
        create_new_stream_form = CreateNewStreamForm()

        create_new_stream_form.from_stream.choices = [
            (stream.name, stream.name) for stream in streams
        ]

        return render_template(
            "create_new_stream_from_stream_page.html",
            form=create_new_stream_form,
            project_id=request.args.get("project_id"),
        )

    def __process_failure_return(self, failure_details: FailureDetails) -> str:
        return render_template(
            "create_new_stream_from_stream_page.html", error=failure_details
        )
