from typing import Dict, Tuple

from flask_restful import Resource

from kamui.entrypoints.rest.helpers import json_response


class GetHealthStatus(Resource):
    API_PATH = "/health/status"

    @json_response
    def get(self) -> Tuple[Dict[str, str], int]:
        return {"status": "ok"}, 200
