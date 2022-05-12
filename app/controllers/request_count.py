from flask import Response, jsonify
from flask_restful import Resource


from app.entities.request_count import RequestCount
from app.services.monitoramento import Monitoramento


class RequestCountIntervalConsume(Resource):

    def get(self, date_now, time_range) -> Response:

        try:
            data = Monitoramento(RequestCount, date_now, time_range)
            data = data.get_interval_data()
            return jsonify(data)
        except Exception:
            return jsonify({'msg': "Nenhum dado encontrado"})


class RequestCountCurrentConsume(Resource):

    def get(self, date_start) -> Response:

        try:
            dados = Monitoramento(RequestCount, date_start, "30")
            dados = dados.get_current_data()
            return jsonify(dados)
        except:
            return jsonify({'msg': "Nenhum dado encontrado"})
