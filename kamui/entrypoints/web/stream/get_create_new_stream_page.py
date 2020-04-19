from flask import render_template
from flask.views import View
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

from kamui.configuration.dependency_injection import di_container
from kamui.core.usecase.topic.get_available_topic_names import (
    GetAvailableTopicNamesUsecase,
)


class CreateNewStreamForm(FlaskForm):
    topic = SelectField("Topic", choices=[])
    stream_name = StringField("Stream Name", validators=(DataRequired(),))
    topic_fields = SelectMultipleField("Topic Fields", choices=[("a", "a"), ("b", "b")])


class GetCreateNewStreamPage(View):
    PATH = "/streams/create/fromtopic"
    methods = ["GET"]

    def __init__(self):
        self.__get_available_topic_names = di_container.resolve(
            GetAvailableTopicNamesUsecase
        )

    def dispatch_request(self):
        create_new_stream_form = CreateNewStreamForm()
        available_topic_names = self.__get_available_topic_names()

        create_new_stream_form.topic.choices = [
            (topic_name, topic_name) for topic_name in available_topic_names
        ]

        return render_template(
            "create_new_stream_page.html", form=create_new_stream_form
        )
