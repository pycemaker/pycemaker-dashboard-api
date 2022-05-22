from flask import Response, jsonify
from flask_restful import Resource


from app.entities.ram import JvmMemoryUsage
from app.entities.ram_details import JvmMemoryUsageDetails
from app.services.monitoramento import Monitoramento


class RamIntervalConsume(Resource):

    def get(self, date_now, time_range) -> Response:

        try:
            data = Monitoramento(JvmMemoryUsage, date_now, time_range)
            data = data.get_interval_data()
            return jsonify(data)
        except Exception:
            # traceback.print_exc()
            # return jsonify({'msg': "Nenhum dado encontrado"})
            data = {{'msg': "Nenhum dado encontrado"}}
            return data, 400


class RamDetailsIntervalConsume(Resource):

    def get(self, date_now, time_range) -> Response:

        try:
            data = Monitoramento(JvmMemoryUsageDetails, date_now, time_range)
            data = data.get_current_ram_details_data()
            return jsonify(data)
        except Exception:
            # traceback.print_exc()
            # return jsonify({'msg': "Nenhum dado encontrado"})
            data = {{'msg': "Nenhum dado encontrado"}}
            return data, 400


class RamCurrentConsume(Resource):

    def get(self, date_start) -> Response:

        try:
            dados = Monitoramento(JvmMemoryUsage, date_start, "30")
            dados = dados.get_current_data()
            return jsonify(dados)
        except:
            data = {{'msg': "Nenhum dado encontrado"}}
            return data, 400


class RamIntervalPrediction(Resource):

    def get(self, date_start, time_range) -> Response:

        try:
            dados = Monitoramento(JvmMemoryUsage, date_start, time_range)
            dados = dados.get_prediction_data()
            return jsonify(dados)
        except:
            data = {{'msg': "Nenhum dado encontrado"}}
            return data, 400


class RamDetailsCurrentConsume(Resource):

    def get(self, date_start) -> Response:

        try:
            dados = Monitoramento(JvmMemoryUsageDetails, date_start, "30")
            dados = dados.get_current_data()
            return jsonify(dados)
        except:
            data = {{'msg': "Nenhum dado encontrado"}}
            return data, 400
