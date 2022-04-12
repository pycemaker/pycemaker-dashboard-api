import traceback
from flask import Response, jsonify
from flask_restful import Resource


from app.entities.ram import RamUsage
from app.services.monitoramento import Monitoramento


class RamIntervalConsume(Resource):

    def get(self, date_now, time_range) -> Response:

        try:
            data = Monitoramento(RamUsage, date_now, time_range)
            data = data.get_data()
            return jsonify(data)
        except Exception:
            traceback.print_exc()
            return jsonify({'msg': "Nenhum dado encontrado"})


class RamCurrentConsume(Resource):

    def get(self, date_start) -> Response:

        try:
            dados = Monitoramento(RamUsage, date_start, "30")
            dados = dados.get_current_data()
            return jsonify(dados)
        except:
            return jsonify({'msg': "Nenhum dado encontrado"})
