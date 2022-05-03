
import json
import time
from datetime import date, datetime
from pathlib import Path
import pandas as pd
import requests
from hurry.filesize import si, size


class Pycemaker:
    def __init__(self, prom_url=None) -> None:
        self.prom_url = prom_url

    def __get_cpu_usage__(self) -> float:
        """Método de acesso ao uso de cpu em certo momento.

        Returns:
            float: Porcentagem do uso de cpu do processo.
        """

        response = requests.get(self.prom_url, params={
                                'query': 'process_cpu_usage'})
        result = response.json()['data']['result'][0]['value'][1]
        percentage_result = "{:.2%}".format(abs(float(result)))

        return result, percentage_result

    def __get_used_memory__(self) -> str:
        """Método de acesso ao uso de memória da JVM em certo momento.

        Returns:
            str: Quantidade de memória usada da JVM no momento.
        """
        response = requests.get(self.prom_url, params={
            'query': 'sum(jvm_memory_used_bytes)'})
        response = response.json()
        sum_result = response['data']['result'][0]['value'][1]
        memory_used = str(size(int(sum_result), system=si))

        return sum_result, memory_used

    def __get_total_used_memory__(self) -> str:
        """Método de acesso ao uso de memória da JVM em certo momento.

        Returns:
            str: Quantidade de memória usada da JVM no momento.
        """
        response = requests.get(self.prom_url, params={
            'query': 'sum(jvm_memory_used_bytes)/sum(jvm_memory_max_bytes)'})
        response = response.json()
        sum_result = response['data']['result'][0]['value'][1]
        percentage_result = "{:.2%}".format(abs(float(sum_result)))

        return sum_result, percentage_result

    def __get_used_heap_memory__(self) -> str:
        response = requests.get(self.prom_url, params={
            'query': 'sum(jvm_memory_used_bytes{area="heap"})/sum(jvm_memory_max_bytes{area="heap"})'})
        response = response.json()
        result = response['data']['result'][0]['value'][1]
        percentage_result = "{:.2%}".format(abs(float(result)))

        return result, percentage_result

    def __get_used_nonheap_memory__(self) -> str:
        response = requests.get(self.prom_url, params={
            'query': 'sum(jvm_memory_used_bytes{area="nonheap"})/sum(jvm_memory_max_bytes{area="nonheap"})'})
        response = response.json()
        result = response['data']['result'][0]['value'][1]
        percentage_result = "{:.2%}".format(abs(float(result)))

        return result, percentage_result

    def __get_disk_usage__(self) -> str:
        """Método de acesso ao uso de memória da JVM em certo momento.

        Returns:
            str: Quantidade de memória usada da JVM no momento.
        """
        response = requests.get(self.prom_url, params={
            'query': 'disk_total_bytes-disk_free_bytes'})
        response = response.json()
        sum_result = response['data']['result'][0]['value'][1]
        disk_used = str(size(int(sum_result), system=si))

        return sum_result, disk_used

    def __get_total_disk_usage__(self) -> str:
        """Método de acesso ao uso de memória da JVM em certo momento.

        Returns:
            str: Quantidade de memória usada da JVM no momento.
        """
        response = requests.get(self.prom_url, params={
            'query': '(disk_total_bytes-disk_free_bytes)/disk_total_bytes'})
        response = response.json()
        sum_result = response['data']['result'][0]['value'][1]
        percentage_result = "{:.2%}".format(abs(float(sum_result)))

        return sum_result, percentage_result

    # Ignore
    def __get_http_request_count__(self, outcome, uri) -> str:
        query = 'http_server_requests_seconds_count{outcome="%s", uri="/%s"}[10s]' % (
            outcome, uri)
        response = requests.get(self.prom_url, params={
            'query': query})
        response = response.json()

        value = 0
        if len(response['data']['result']) > 0:
            value_old = int(response['data']['result'][0]['values'][0][1])
            value_actual = int(response['data']['result'][0]['values'][1][1])
            value = value_actual - value_old

        return value

    # Ignore
    def __get_http_request_time_response__(self, outcome, uri) -> str:
        query_count = 'http_server_requests_seconds_count{outcome="%s", uri="/%s"}[10s]' % (
            outcome, uri)
        query_sum = 'http_server_requests_seconds_sum{outcome="%s", uri="/%s"}[10s]' % (
            outcome, uri)
        response_count = requests.get(self.prom_url, params={
            'query': query_count})
        response_sum = requests.get(self.prom_url, params={
            'query': query_sum})
        response_count = response_count.json()
        response_sum = response_sum.json()

        value_count = 0
        if len(response_count['data']['result']) > 0:
            value_old = float(response_count['data']
                              ['result'][0]['values'][0][1])
            value_actual = float(
                response_count['data']['result'][0]['values'][1][1])
            value_count = value_actual - value_old

        value_sum = 0
        if len(response_sum['data']['result']) > 0:
            value_old = float(
                response_sum['data']['result'][0]['values'][0][1])
            value_actual = float(
                response_sum['data']['result'][0]['values'][1][1])
            value_sum = value_actual - value_old

        value = 0
        if value_count != 0:
            value = value_sum / value_count

        return value * 1000

    def __get_http_request_success_count__(self) -> str:
        query = 'avg(rate(http_server_requests_seconds_count{outcome="SUCCESS", uri!~"/actuator.*"}[10s]))'
        response = requests.get(self.prom_url, params={
            'query': query})
        response = response.json()

        if len(response['data']['result']) > 0:
            return response['data']['result'][0]['value'][1] if response['data']['result'][0]['value'][1] != "NaN" else "0"
        else:
            return "0"

    def __get_http_request_success_time_response__(self) -> str:
        query = 'avg(irate(http_server_requests_seconds_sum{outcome="SUCCESS", uri!~"/actuator.*"}[10s])/irate(http_server_requests_seconds_count{outcome="SUCCESS", uri!~"/actuator.*"}[10s]))'
        response = requests.get(self.prom_url, params={
            'query': query})
        response = response.json()

        if len(response['data']['result']) > 0:
            return response['data']['result'][0]['value'][1] if response['data']['result'][0]['value'][1] != "NaN" else "0"
        else:
            return "0"

    def __get_http_request_fail_count__(self) -> str:
        query = 'avg(rate(http_server_requests_seconds_count{outcome="CLIENT_ERROR", uri!~"/actuator.*"}[10s]))'
        response = requests.get(self.prom_url, params={
            'query': query})
        response = response.json()

        if len(response['data']['result']) > 0:
            return response['data']['result'][0]['value'][1] if response['data']['result'][0]['value'][1] != "NaN" else "0"
        else:
            return "0"

    def __get_http_request_fail_time_response__(self) -> str:
        query = 'avg(irate(http_server_requests_seconds_sum{outcome="CLIENT_ERROR", uri!~"/actuator.*"}[10s])/irate(http_server_requests_seconds_count{outcome="CLIENT_ERROR", uri!~"/actuator.*"}[10s]))'
        response = requests.get(self.prom_url, params={
            'query': query})
        response = response.json()

        if len(response['data']['result']) > 0:
            return response['data']['result'][0]['value'][1] if response['data']['result'][0]['value'][1] != "NaN" else "0"
        else:
            return "0"

    def __get_data__(self) -> dict:
        """Modelo de dicionário dos dados obtidos da aplicação SpringBoot selecionada.

        Returns:
            dict: Retorna um dicionário com o modelo preenchido com os dados obtidos.
        """

        cpu, cpu_percentage = self.__get_cpu_usage__()
        disk, disk_percentage = self.__get_disk_usage__()
        total_disk, total_disk_percentage = self.__get_total_disk_usage__()
        jvm_memory_usage, jvm_memory_usage_mb = self.__get_used_memory__()
        memory, memory_percentage = self.__get_total_used_memory__()
        heap_memory, heap_percentage = self.__get_used_heap_memory__()
        nonheap_memory, nonheap_percentage = self.__get_used_nonheap_memory__()
        # http_usuarios_request_count_now = self.__get_http_request_count__("SUCCESS",
        #                                                                   "usuarios")
        success = self.__get_http_request_success_count__()
        success_ms = self.__get_http_request_success_time_response__()
        fail = self.__get_http_request_fail_count__()
        fail_ms = self.__get_http_request_fail_time_response__()

        data = {"datetime": str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                "cpu_usage": float(cpu),
                "cpu_percentage": cpu_percentage,
                "disk_usage": int(disk),
                "disk_mb": disk_percentage,
                "total_disk_usage": float(total_disk),
                "total_disk_percentage": total_disk_percentage,
                "memory_usage": float(memory),
                "memory_percentage": memory_percentage,
                "jvm_memory_usage": int(jvm_memory_usage),
                "jvm_memory_usage_mb": jvm_memory_usage_mb,
                "heap_memory": float(heap_memory),
                "heap_percentage": heap_percentage,
                "nonheap_memory": float(nonheap_memory),
                "nonheap_percentage": nonheap_percentage,
                "success_request_count": float(success),
                "success_request_ms": float(success_ms),
                "fail_request_count": float(fail),
                "fail_request_ms": float(fail_ms),
                }
        return data

    def save_data(self, doc_count=0, time_to_save=0):
        """Salva os dados obtidos na coleção instanciada pelo objeto da classe.

        Args:
            doc_count (int, optional): Quantidade de documentos que vão ser salvos.
            time_to_save (int, optional): Intervalo de tempo em segundos em que os documentos serão salvos.
        """
        result = self.__get_data__()
        print(json.dumps(result, indent=3))
