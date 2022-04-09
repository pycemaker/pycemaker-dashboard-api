import time
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import requests
from bson.json_util import dumps
from hurry.filesize import si, size
from pymongo import MongoClient


class Pycemaker:
    def __init__(self, db_host: str, db_port: int, db: str, collection: str, prom_url=None) -> None:
        """Classe de gerenciamento das métricas de aplicações SpringBoot expostas pela API do Prometheus

        Args:
            prom_url (str, optional): URL da API do Prometheus
            db_host (str): URL do client
            db_port (int): Porta do client
            db (str): Banco de dados selecionado
            collection (str): Coleção do banco de dados
        """
        self.prom_url = prom_url
        self.db_host = db_host
        self.db_port = db_port
        self.db = db
        self.collection = collection
        self.client = MongoClient(host=self.db_host, port=int(self.db_port))

    
    def __get_cpu_usage__(self) -> float:
        """Método de acesso ao uso de cpu em certo momento.

        Returns:
            float: Porcentagem do uso de cpu do processo.
        """

        response = requests.get(self.prom_url, params={
                                'query': 'process_cpu_usage'})
        result = response.json()['data']['result'][0]['value'][1]
        percentage_result = "{:.2%}".format(abs(float(result)))

        return percentage_result

    def __get_used_memory__(self) -> str:
        """Método de acesso ao uso de memória da JVM em certo momento.

        Returns:
            str: Quantidade de memória usada da JVM no momento.
        """
        response = requests.get(self.prom_url, params={
            'query': 'jvm_memory_used_bytes'})

        result = response.json()['data']['result'][0]['value'][1]
        memory_used = str(size(int(result), system=si))

        return memory_used

    def __get_data__(self) -> dict:
        """Modelo de dicionário dos dados obtidos da aplicação SpringBoot selecionada.

        Returns:
            dict: Retorna um dicionário com o modelo preenchido com os dados obtidos.
        """
        
        data = {"date": str(date.today()),
                "time":str(datetime.now().strftime("%H:%M:%S")),
                "cpu_usage": float(Pycemaker.__get_cpu_usage__(self).strip('%'))/100.0,
                "jvm_memory_usage": Pycemaker.__get_used_memory__(self)}
        return data

    def save_data(self, doc_count=0, time_to_save=0):
        """Salva os dados obtidos na coleção instanciada pelo objeto da classe.

        Args:
            doc_count (int, optional): Quantidade de documentos que vão ser salvos.
            time_to_save (int, optional): Intervalo de tempo em segundos em que os documentos serão salvos.
        """
        c = 0
        client = self.client
        database = client[self.db]
        col_dst = database[self.collection]

        if doc_count > c:
            while c in range(doc_count):
                c = c + 1
                col_dst.insert_one(Pycemaker.__get_data__(self))
                time.sleep(time_to_save)
        else:
            col_dst.insert_one(Pycemaker.__get_data__(self))

    def export_data_json(self, dst=Path.cwd()):
        """Exporta a coleção instanciada pelo objeto da classe como JSON

        Args:
            dst (str, optional): Destino do arquivo JSON. Diretório atual é o padrão.
        """

        client = self.client
        database = client[self.db]
        col_dst = database[self.collection]
        cursor = col_dst.find({})

        with open(str(Path(dst, 'pycedata.json')), 'w') as file:
            file.write('[')
            for document in cursor:
                file.write(dumps(document))
                file.write(',')
            file.write(']')

    def export_data_csv(self, dst=Path.cwd()):
        """Exporta a coleção instanciada pelo objeto da classe como CSV

        Args:
            dst (str, optional): Destino do arquivo CSV. Diretório atual é o padrão.
        """
        client = self.client
        database = client[self.db]
        col_dst = database[self.collection]
        cursor = col_dst.find({})

        docs = pd.DataFrame(cursor)
        docs.pop("_id")
        docs.to_csv(Path(dst, 'pycedata.csv'), index=None)
