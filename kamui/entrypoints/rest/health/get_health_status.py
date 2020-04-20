from typing import Dict

from flask_restful import Resource


class GetHealthStatus(Resource):
    API_PATH = "/health/status"

    def get(self) -> Dict[str, str]:
        return {"status": "ok"}
