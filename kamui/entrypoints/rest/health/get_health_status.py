from flask_restful import Resource


class GetHealthStatus(Resource):
    API_PATH = "/health/status"

    def get(self):
        return {"status": "ok"}
