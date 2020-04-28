from flask import render_template, request
from flask.views import View
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.topic import TopicNames
from kamui.core.usecase.failure import FailureDetails
from kamui.core.usecase.topic.get_available_topic_names import (
    GetAvailableTopicNamesUsecase,
)


class CreateNewStreamForm(FlaskForm):
    topic = SelectField("Topic", choices=[])
    stream_name = StringField("Stream Name", validators=(DataRequired(),))
    topic_fields = SelectMultipleField("Topic Fields", choices=[("a", "a"), ("b", "b")])


class GetCreateNewStreamFromTopicPage(View):
    PATH = "/streams/create/fromtopic"
    methods = ["GET"]

    def __init__(self) -> None:
        self.__get_available_topic_names = di_container.resolve(
            GetAvailableTopicNamesUsecase
        )

    def dispatch_request(self) -> str:  # type: ignore
        available_topic_names = self.__get_available_topic_names()
        return (  # type: ignore
            available_topic_names.map(self.__process_success_return)
            .fix(self.__process_failure_return)
            .unwrap()
        )

    def __process_success_return(self, available_topic_names: TopicNames) -> str:
        create_new_stream_form = CreateNewStreamForm()

        create_new_stream_form.topic.choices = [
            (topic_name, topic_name) for topic_name in available_topic_names
        ]

        return render_template(
            "create_new_stream_page.html",
            form=create_new_stream_form,
            project_id=request.args.get("project_id"),
        )

    def __process_failure_return(self, failure_details: FailureDetails) -> str:
        return render_template("create_new_stream_page.html", error=failure_details)
