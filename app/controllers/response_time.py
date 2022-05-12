from flask import Response, jsonify
from flask_restful import Resource


from app.entities.response_time import ResponseTime
from app.services.monitoramento import Monitoramento


class ResponseTimeIntervalConsume(Resource):

    def get(self, date_now, time_range) -> Response:

        try:
            data = Monitoramento(ResponseTime, date_now, time_range)
            data = data.get_interval_data()
            return jsonify(data)
        except Exception:
            return jsonify({'msg': "Nenhum dado encontrado"})


class ResponseTimeCurrentConsume(Resource):

    def get(self, date_start) -> Response:

        try:
            dados = Monitoramento(ResponseTime, date_start, "30")
            dados = dados.get_current_data()
            return jsonify(dados)
        except:
            return jsonify({'msg': "Nenhum dado encontrado"})
