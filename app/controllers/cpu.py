import traceback
from flask import Response, jsonify
from flask_restful import Resource
import datetime


from app.entities.cpu_usage import CpuUsage
from app.services.monitoramento import Monitoramento
from app.services.monitoramento2 import Monitoramento2


class CpuAnalytics(Resource):

    def convert_date(self, date):
        converted_date = int(date)
        converted_date = converted_date / 1000
        converted_date = datetime.datetime.fromtimestamp(
            converted_date).strftime('%Y-%m-%d %H:%M:%S.%f')

        return converted_date

    def get(self, date_now, time_range) -> Response:

        data_agora = datetime.datetime.strptime(date_now, '%d-%m-%Y-%H-%M-%S')
        data_passado = data_agora - datetime.timedelta(hours=int(time_range))
        data_periodo_anterior = data_passado - \
            datetime.timedelta(hours=int(time_range))

        # tratando dados de 11 horas atras
        dados = CpuUsage.objects(
            time_series__gte=data_passado, time_series__lte=data_agora)
        # dados = CpuUsage.objects
        dados = [x.to_mongo() for x in dados]
        dados = [x.to_dict() for x in dados]

        # [d.update({"time_series": self.convert_date((d["time_series"][:-2]).replace(".", ""))})
        #  for d in dados]
        [d.update({"value": float(d["value"]) * 100}) for d in dados]
        [d.update({"_id": str(d["_id"])}) for d in dados]

        monitoramento_atual = Monitoramento2(dados, "value")

        # tratando dados de 22 horas atras
        dados_anteriores = CpuUsage.objects(
            time_series__gte=data_periodo_anterior, time_series__lte=data_passado)
        # dados_anteriores = CpuUsage.objects
        dados_anteriores = [x.to_mongo() for x in dados_anteriores]
        dados_anteriores = [x.to_dict() for x in dados_anteriores]

        # [d.update({"time_series": self.convert_date((d["time_series"][:-2]).replace(".", ""))})
        #  for d in dados]
        [d.update({"value": float(d["value"]) * 100})
         for d in dados_anteriores]
        [d.update({"_id": str(d["_id"])}) for d in dados_anteriores]

        monitoramento_anterior = Monitoramento2(dados_anteriores, "value")

        if dados:
            mean = monitoramento_atual.get_mean()
            lower = monitoramento_atual.get_lower()
            higher = monitoramento_atual.get_higher()
            mean_anterior = monitoramento_anterior.get_mean()
            growth = monitoramento_atual.get_growth(mean, mean_anterior)
            return jsonify({'mean': mean,
                            'mean_anterior': mean_anterior,
                            'lower': lower, 'higher': higher,
                            'data': dados,
                            'data_anterior': dados_anteriores,
                            'growth': growth,
                            'datas': [data_agora, data_passado, data_periodo_anterior]})
        return jsonify({'msg': "Nenhum dado encontrado"})


class CpuAnalytics_2(Resource):

    def get(self, date_now, time_range) -> Response:

        try:
            data = Monitoramento(CpuUsage, date_now, time_range)
            data = data.get_data()
            return jsonify(data)
        except Exception:
            traceback.print_exc()
            return jsonify({'msg': "Nenhum dado encontrado"})


class CpuAnalytics_3(Resource):

    def get(self, date_start) -> Response:

        try:

            date_start = datetime.datetime.strptime(
                date_start, '%d-%m-%Y-%H-%M-%S')

            print(date_start)

            dados = CpuUsage.objects(
                time_series__gte=date_start)

            dados = [x.to_mongo() for x in dados]
            dados = [x.to_dict() for x in dados]

            [d.update({"value": float(d["value"]) * 100}) for d in dados]
            [d.update({"_id": str(d["_id"])}) for d in dados]

            return jsonify(dados)
        except:
            return jsonify({'msg': "Nenhum dado encontrado"})
