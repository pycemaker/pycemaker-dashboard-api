from flask import Response, jsonify
from flask_restful import Resource


from app.entities.fail_request_count import FailRequestCount
from app.services.monitoramento import Monitoramento


class FRequestCountIntervalConsume(Resource):

    def get(self, date_now, time_range) -> Response:

        try:
            data = Monitoramento(FailRequestCount, date_now, time_range)
            data = data.get_interval_data()
            return jsonify(data)
        except Exception:
            return jsonify({'msg': "Nenhum dado encontrado"})


class FRequestCountCurrentConsume(Resource):

    def get(self, date_start) -> Response:

        try:
            dados = Monitoramento(FailRequestCount, date_start, "30")
            dados = dados.get_current_data()
            return jsonify(dados)
        except:
            return jsonify({'msg': "Nenhum dado encontrado"})
