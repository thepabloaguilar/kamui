from dataclasses import dataclass
from typing import Any, Dict, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class FailureDetails:
    reason: str


@dataclass_json
@dataclass
class BusinessFailureDetails(FailureDetails):
    failure_message: str
    failure_due: Optional[Any] = None


@dataclass_json
@dataclass
class DataProviderFailureDetails(FailureDetails):
    dataprovider_type: str
    attributes: Optional[Dict[str, Any]]
