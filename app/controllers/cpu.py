import traceback
from flask import Response, jsonify
from flask_restful import Resource
from dateutil.parser._parser import UnknownTimezoneWarning

from app.entities.cpu import CpuUsage
from app.services.monitoramento import Monitoramento


class CpuIntervalConsume(Resource):

    def get(self, date_now, time_range) -> Response:

        try:
            data = Monitoramento(CpuUsage, date_now, time_range)
            data = data.get_interval_data()
            return jsonify(data)
        except UnknownTimezoneWarning:
            # traceback.print_exc()
            return jsonify({'msg': "Nenhum dado encontrado"})


class CpuCurrentConsume(Resource):

    def get(self, date_start) -> Response:

        try:
            dados = Monitoramento(CpuUsage, date_start)
            dados = dados.get_current_data()
            return jsonify(dados)
        except:
            return jsonify({'msg': "Nenhum dado encontrado"})


class CpuIntervalPrediction(Resource):

    def get(self, date_start) -> Response:

        try:
            dados = Monitoramento(CpuUsage, date_start)
            dados = dados.get_prediction_data()
            return jsonify(dados)
        except:
            return jsonify({'msg': "Nenhum dado encontrado"})


class CpuRandomPrediction(Resource):

    def get(self, date_now) -> Response:

        try:
            dados = Monitoramento(CpuUsage, date_now)
            dados = dados.get_random_data()
            return jsonify(dados)
        except:
            return jsonify({'msg': "Nenhum dado encontrado"})
