import pytest
from flask import Flask


@pytest.fixture(scope="session")
def flask_app() -> Flask:
    return Flask(__name__)
