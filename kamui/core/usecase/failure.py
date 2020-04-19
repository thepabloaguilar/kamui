from dataclasses import dataclass
from functools import partial

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class FailureDetails:
    failure_message: str
    reason: str


def failure_details(failure_message):
    return partial(FailureDetails, failure_message)
