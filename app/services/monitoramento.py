import numpy as np
import datetime
import math


class Monitoramento:
    def __init__(self, classe_do_dado, date_now, time_range) -> None:

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

        [d.update({"value": float(d["value"]) * 100}) for d in dados]
        [d.update({"_id": str(d["_id"])}) for d in dados]

        return dados

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
            return growth * 100
        return 0

    def get_data(self):
        self.dados_atuais = self.transform_data(
            self.data_inicial_atual, self.data_final_atual)
        self.dados_anteriores = self.transform_data(
            self.data_inicial_anterior, self.data_inicial_atual)

        mean_atual = self.get_mean(self.dados_atuais)
        mean_anterior = self.get_mean(self.dados_anteriores)
        lower = self.get_lower()
        higher = self.get_higher()
        growth = self.get_growth(mean_atual, mean_anterior)

        return {'data': self.dados_atuais,
                'data_anterior': self.dados_anteriores,
                'mean': mean_atual,
                'mean_anterior': mean_anterior,
                'lower': lower,
                'higher': higher,
                'growth': growth,
                'datas': [self.data_final_atual, self.data_inicial_atual,
                          self.data_inicial_anterior]}
