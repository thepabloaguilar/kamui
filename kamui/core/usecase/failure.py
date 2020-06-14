from typing import Any, Dict, Optional

from pydantic.dataclasses import dataclass


@dataclass
class FailureDetails:
    reason: str


@dataclass
class BusinessFailureDetails(FailureDetails):
    failure_message: str
    failure_due: Optional[Any] = None


@dataclass
class DataProviderFailureDetails(FailureDetails):
    dataprovider_type: str
    attributes: Optional[Dict[str, Any]]
