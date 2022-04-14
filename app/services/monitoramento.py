import json
import numpy as np
import datetime
import pandas as pd


class Monitoramento:
    def __init__(self, classe_do_dado, date_now, time_range="0") -> None:

        self.dados_atuais = None
        self.dados_anteriores = None
        self.classe_do_dado = classe_do_dado
        self.nome_do_dado = "value"
        self.data_final_atual = datetime.datetime.strptime(
            date_now, '%d-%m-%Y-%H-%M-%S')
        self.data_inicial_atual = self.data_final_atual - \
            datetime.timedelta(hours=int(time_range))
        self.data_inicial_anterior = self.data_inicial_atual - \
            datetime.timedelta(hours=int(time_range))

    def transform_data(self, data_inicial, data_final):
        classe_do_dado = self.classe_do_dado
        dados = classe_do_dado.objects(
            time_series__gte=data_inicial, time_series__lte=data_final)

        dados = [x.to_mongo() for x in dados]
        dados = [x.to_dict() for x in dados]

        [d.update({"value": float(d["value"])}) for d in dados]
        [d.update({"_id": str(d["_id"])}) for d in dados]
        return dados

    def pandas_transform_data(self, data_inicial, data_final):
        classe_do_dado = self.classe_do_dado
        # dados = classe_do_dado.objects(
        #     time_series__gte=data_inicial, time_series__lte=data_final)
        dados = classe_do_dado.objects

        dados = [x.to_mongo() for x in dados]
        dados = [x.to_dict() for x in dados]

        [d.update({"value": float(d["value"])}) for d in dados]
        [d.update({"_id": str(d["_id"])}) for d in dados]
        [d.update({"time_series": self.convert_date(
            (d["time_series"][:-2]).replace(".", ""))}) for d in dados]

        df = pd.DataFrame(dados)
        df['time_series'] = pd.to_datetime(df['time_series'])
        df = df[(df['time_series'] > data_inicial)
                & (df['time_series'] < data_final)]
        df = df.to_json(orient="table")
        parsed = json.loads(df)
        return parsed['data']

    def get_mean(self, dados):
        if dados:
            mean = np.mean([x[self.nome_do_dado] for x in dados])
            return mean
        return 0

    def get_higher(self):
        higher = max(self.dados_atuais, key=lambda x: x[self.nome_do_dado])
        all_higher = [x for x in self.dados_atuais if x[self.nome_do_dado]
                      == higher[self.nome_do_dado]]
        return all_higher

    def get_lower(self):
        lower = min(self.dados_atuais, key=lambda x: x[self.nome_do_dado])
        all_lower = [x for x in self.dados_atuais if x[self.nome_do_dado]
                     == lower[self.nome_do_dado]]
        return all_lower

    def get_growth(self, mean_atual, mean_anterior):
        if mean_anterior != 0:
            growth = (mean_atual - mean_anterior) / mean_anterior
            return growth
        return 0

    def get_criticity_classification(self):
        df = pd.DataFrame(self.dados_atuais)
        print(len(df))
        df = df.replace(np.nan, 0)
        df = df.groupby(['criticity'])['value'].count() / len(df)
        df = df.to_json(orient="table")
        parsed = json.loads(df)
        return parsed['data']

    def convert_date(self, date):
        converted_date = int(date)
        converted_date = converted_date / 1000
        converted_date = datetime.datetime.fromtimestamp(
            converted_date).strftime('%Y-%m-%d %H:%M:%S.%f')

        return converted_date

    def get_data(self):
        self.dados_atuais = self.pandas_transform_data(
            self.data_inicial_atual, self.data_final_atual)
        self.dados_anteriores = self.pandas_transform_data(
            self.data_inicial_anterior, self.data_inicial_atual)

        mean_atual = self.get_mean(self.dados_atuais)
        mean_anterior = self.get_mean(self.dados_anteriores)
        lower = self.get_lower()
        higher = self.get_higher()
        growth = self.get_growth(mean_atual, mean_anterior)
        criticity_classification = self.get_criticity_classification()

        return {'data': self.dados_atuais,
                'data_anterior': self.dados_anteriores,
                'mean': mean_atual,
                'mean_anterior': mean_anterior,
                'lower': lower,
                'higher': higher,
                'growth': growth,
                'criticity_classification': criticity_classification,
                'datas': [self.data_final_atual, self.data_inicial_atual,
                          self.data_inicial_anterior]}

    def get_current_data(self):
        classe_do_dado = self.classe_do_dado
        # dados = classe_do_dado.objects(
        #     time_series__gte=data_inicial)
        dados = classe_do_dado.objects
        dados = [x.to_mongo() for x in dados]
        dados = [x.to_dict() for x in dados]

        [d.update({"value": float(d["value"])}) for d in dados]
        [d.update({"_id": str(d["_id"])}) for d in dados]
        [d.update({"time_series": self.convert_date(
            (d["time_series"][:-2]).replace(".", ""))}) for d in dados]

        df = pd.DataFrame(dados)
        df['time_series'] = pd.to_datetime(df['time_series'])
        df = df[df['time_series'] >= self.data_final_atual]
        df = df.to_json(orient="table")
        parsed = json.loads(df)
        return parsed['data']
