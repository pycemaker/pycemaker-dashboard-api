import traceback
from flask import Response, jsonify
from flask_restful import Resource


from app.entities.http_fail import HttpFail
from app.services.monitoramento import Monitoramento


class HttpFailIntervalConsume(Resource):

    def get(self, date_now, time_range) -> Response:

        try:
            data = Monitoramento(HttpFail, date_now, time_range)
            data = data.get_interval_data()
            return jsonify(data)
        except Exception:
            # traceback.print_exc()
            return jsonify({'msg': "Nenhum dado encontrado"})


class HttpFailCurrentConsume(Resource):

    def get(self, date_start) -> Response:

        try:
            dados = Monitoramento(HttpFail, date_start, "30")
            dados = dados.get_current_data()
            return jsonify(dados)
        except:
            return jsonify({'msg': "Nenhum dado encontrado"})
