from flask import Response, jsonify
from flask_restful import Resource


from app.entities.success_request_count import SuccessRequestCount
from app.services.monitoramento import Monitoramento


class SRequestCountIntervalConsume(Resource):

    def get(self, date_now, time_range) -> Response:

        try:
            data = Monitoramento(SuccessRequestCount, date_now, time_range)
            data = data.get_interval_data()
            return jsonify(data)
        except Exception:
            return jsonify({'msg': "Nenhum dado encontrado"})


class SRequestCountCurrentConsume(Resource):

    def get(self, date_start) -> Response:

        try:
            dados = Monitoramento(SuccessRequestCount, date_start, "30")
            dados = dados.get_current_data()
            return jsonify(dados)
        except:
            return jsonify({'msg': "Nenhum dado encontrado"})
