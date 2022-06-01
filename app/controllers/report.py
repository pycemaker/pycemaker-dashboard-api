from flask import Response, jsonify
from flask_restful import Resource

from app.services.reporter import Reporter


class Report(Resource):

    def get(self, time_range, email_to) -> Response:

        try:
            report = Reporter(time_range, email_to)
            report = report.get_report()

            return jsonify({'msg': report})

        except Exception as err:
            data = {'msg': err}
            return data, 400
