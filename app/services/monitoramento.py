import json
from time import sleep
import numpy as np
import datetime
import pandas as pd
import requests
from mongoengine import Q


class Monitoramento:
    """Classe que observa uma collection do MongoDB e obtém dados filtrados e analíticos.
    """

    def __init__(self, classe_do_dado, date_now, time_range="0"):
        """Classe que observa uma collection do MongoDB e obtém dados filtrados e analíticos.

        Args:
            classe_do_dado (class): Classe da collection que será analisada.
            date_now (str): Data de base para filtragem dos dados.
            time_range (str, optional): Intervalo de horas para filtragem. Defaults to "0".
        """

        self.time_range = int(time_range)
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

    def transform_data(self):
        """Busca no banco todos os dados de consumo e converte para os tipos desejados.

        Returns:
            list: Lista com todos os dados encontrados.
        """

        # classe_do_dado = self.classe_do_dado
        # dados = classe_do_dado.objects(
        #     time_series__gte=data_inicial, time_series__lte=data_final)

        # dados = [x.to_mongo() for x in dados]
        # dados = [x.to_dict() for x in dados]

        # [d.update({"value": float(d["value"])}) for d in dados]
        # [d.update({"_id": str(d["_id"])}) for d in dados]
        # return dados

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

        return df

    def get_mean(self, dados):
        """Calcula a média a partir de uma lista de dados.

        Args:
            dados (list): Lista de dados.

        Returns:
            float: Valor com a média obtida em decimal.
        """

        if dados:
            mean = np.mean([x[self.nome_do_dado] for x in dados])
            return mean
        return 0

    def get_higher(self):
        """Filtra todos os maiores valores a partir de uma lista de dados.

        Returns:
            list: Lista filtrada com os maiores valores.
        """

        if (self.dados_atuais):
            higher = max(self.dados_atuais, key=lambda x: x[self.nome_do_dado])
            all_higher = [x for x in self.dados_atuais if x[self.nome_do_dado]
                          == higher[self.nome_do_dado]]
            return all_higher
        return []

    def get_lower(self):
        """Filtra todos os menores valores a partir de uma lista de dados.

        Returns:
            list: Lista filtrada com os menores valores.
        """

        if (self.dados_atuais):
            lower = min(self.dados_atuais, key=lambda x: x[self.nome_do_dado])
            all_lower = [x for x in self.dados_atuais if x[self.nome_do_dado]
                         == lower[self.nome_do_dado]]
            return all_lower
        return []

    def get_growth(self, mean_atual, mean_anterior):
        """Calcula o crescimento médio da lista de dados do intervalo atual.

        Args:
            mean_atual (float): Média da lista de dados do intervalo atual.
            mean_anterior (float): Média da lista de dados do intervalo anterior.

        Returns:
            float: Valor com o crescimento médio obtido em decimal.
        """

        if mean_anterior != 0:
            growth = (mean_atual - mean_anterior) / mean_anterior
            return growth
        return 0

    def get_criticity_classification(self):
        """Gera uma lista de classificação de criticidade a partir de uma lista de dados.

        Returns:
            list: Lista de classificação de dados.
        """

        if (self.dados_atuais):
            df = pd.DataFrame(self.dados_atuais)
            df = df.replace(np.nan, 0)
            df = df.groupby(['criticity'])['value'].count() / len(df)
            df = df.to_json(orient="table")
            parsed = json.loads(df)
            return parsed['data']
        return []

    def convert_date(self, date):
        """Converte uma string de milisegundos para datetime.

        Args:
            date (str): String de uma timestamp em milisegundos

        Returns:
            datetime: A data/hora em datetime.
        """

        converted_date = int(date)
        converted_date = converted_date / 1000
        converted_date = datetime.datetime.fromtimestamp(
            converted_date).strftime('%Y-%m-%d %H:%M:%S.%f')

        return converted_date

    def find_data_interval(self, data_inicial, data_final):
        """Filtra uma lista de dados dentro de um intervalo de tempo.

        Args:
            data_inicial (datetime): Data/Hora inicial do intervalo.
            data_final (datetime): Data/Hora final do intervalo.

        Returns:
            list: Lista com os dados encontrados.
        """

        # data_final = datetime.datetime.utcnow() # The end date
        # data_inicial = data_final - datetime.timedelta(days=120) # The start date
        data_final = data_final + datetime.timedelta(hours=3)
        data_inicial = data_inicial + datetime.timedelta(hours=3)
        # print(data_inicial, data_final)

        classe_do_dado = self.classe_do_dado
        dados = classe_do_dado.objects(
            time_series__gte=data_inicial, time_series__lte=data_final)
        # print(dados._query)
        # print(dados)

        dados = [x.to_mongo() for x in dados]
        dados = [x.to_dict() for x in dados]

        [d.update({"_id": str(d["_id"])}) for d in dados]

        # df = pd.DataFrame(dados)

        # df['time_series'] = pd.to_datetime(df['time_series'])

        # print(dados)

        # df = self.transform_data()
        # df = df[(df['time_series'] >= data_inicial)
        #         & (df['time_series'] <= data_final)]
        # df = df.to_json(orient="table")
        # parsed = json.loads(df)
        # return parsed['data']
        return dados

    def find_current_data(self, data_inicial):
        """Filtra uma lista de dados a partir de uma data.

        Args:
            data_inicial (datetime): Data/Hora inicial do intervalo.

        Returns:
            list: Lista com os dados encontrados.
        """

        data_inicial = data_inicial + datetime.timedelta(hours=3)

        classe_do_dado = self.classe_do_dado
        dados = classe_do_dado.objects(
            time_series__gte=data_inicial)
        # print(dados._query)

        # dados = classe_do_dado.objects(Q(time_series__gte=data_inicial)).to_json()

        dados = [x.to_mongo() for x in dados]
        dados = [x.to_dict() for x in dados]

        [d.update({"_id": str(d["_id"])}) for d in dados]

        # df = pd.DataFrame(dados)
        # df['time_series'] = pd.to_datetime(df['time_series'])

        # df = self.transform_data()
        # df = df[df['time_series'] >= data_inicial]
        # df = df.to_json(orient="table")
        # parsed = json.loads(df)
        # return parsed['data']
        return dados

    def get_interval_data(self):
        """Procedimento que retorna uma lista de dados de um intervalo, uma lista de dados do intervalo anterior ao atual,
        a média do intervalo atual, a média do intervalo anterior, uma lista de dados com os menores dados, uma
        lista de dados com os maiores dados, o crescimento médio do intervalo atual, uma lista de classificação dos dados
        do intervalo atual, e as datas dos intervalos analisados.

        Returns:
            dict: Dicionário com todos os resultados obtidos.
        """

        self.dados_atuais = self.find_data_interval(
            self.data_inicial_atual, self.data_final_atual)
        self.dados_anteriores = self.find_data_interval(
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
        """Procedimento que retorna uma lista de dados a partir de uma data.

        Returns:
            list: Lista com os dados encontrados.
        """

        dados = self.find_current_data(self.data_final_atual)

        return dados

    def get_interval_req_count_data(self):
        """Procedimento que retorna uma lista de dados de um intervalo, uma lista de dados do intervalo anterior ao atual,
        a média do intervalo atual, a média do intervalo anterior, uma lista de dados com os menores dados, uma
        lista de dados com os maiores dados, o crescimento médio do intervalo atual, uma lista de classificação dos dados
        do intervalo atual, e as datas dos intervalos analisados.

        Returns:
            dict: Dicionário com todos os resultados obtidos.
        """

        self.dados_atuais = self.find_data_interval(
            self.data_inicial_atual, self.data_final_atual)

        [d.update({"value": d["value_success"] + d["value_fail"]})
         for d in self.dados_atuais]

        self.dados_anteriores = self.find_data_interval(
            self.data_inicial_anterior, self.data_inicial_atual)

        [d.update({"value": d["value_success"] + d["value_fail"]})
         for d in self.dados_anteriores]

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

    def get_prediction_data(self):
        """Procedimento que retorna uma lista de dados de um intervalo de tempo com a previsão para esse intervalo
         e para o intervalo posterior, a última data do intervalo, e a data final do intervalo.

        Returns:
            dict: Dicionário com todos os resultados obtidos.
        """

        # Periodicidade deve ser 5s
        current_data = self.get_current_data()

        import random

        dados = []
        t = self.data_final_atual

        size = int((self.time_range * 60 * 60) / 5)

        # Chamada do predict
        predict = [0 for x in range(0, size)]

        for i in range(0, size):
            t = t + datetime.timedelta(seconds=5)
            if i < len(current_data) - 1:
                row = {
                    "id": i+1,
                    # "time_series": t,
                    "time_series": current_data[i]["time_series"],
                    "value": current_data[i]["value"],
                    "predict_range":  [predict[i], predict[i]],
                    "predict_value": predict[i]
                }
                dados.append(row)
            else:
                row = {
                    "id": i+1,
                    "time_series": t,
                    "predict_range":  [predict[i], predict[i]],
                    "predict_value": predict[i]
                }
                dados.append(row)

        df = pd.DataFrame(dados)
        # df['time_series'] = pd.date_range(
        #     self.data_final_atual + datetime.timedelta(hours=3), freq='5S', periods=size)
        df['time_series'] = pd.to_datetime(df['time_series'])

        df = df.to_json(orient="table")
        dados = json.loads(df)

        return dados["data"]

    # Para testes
    def get_random_data(self):
        """Função para randonizar dados, não será utilizada.

        Returns:
            list: Lista de dados randonizados.
        """

        import random

        t = datetime.datetime.now()
        t = t + datetime.timedelta(seconds=3)

        dados = [{
            "id": i+1,
            "time_series": t,
            "value": random.randint(3, 7) / 10
        } for i in range(0, 1)]

        df = pd.DataFrame(dados)
        df['time_series'] = pd.to_datetime(df['time_series'])
        df = df.to_json(orient="table")
        dados = json.loads(df)

        return dados['data']
