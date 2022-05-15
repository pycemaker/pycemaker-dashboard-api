from flask_restful import Api

from .controllers.job import JobsApi
from .controllers.cpu import CpuCurrentConsume, CpuIntervalConsume, CpuIntervalPrediction, CpuRandomPrediction
from .controllers.ram import RamCurrentConsume, RamIntervalConsume, RamIntervalPrediction
from .controllers.response_time import ResponseTimeCurrentConsume, ResponseTimeIntervalConsume
from .controllers.request_count import RequestCountCurrentConsume, RequestCountIntervalConsume
from .controllers.report import Report


def create_routes(api: Api):
    api.add_resource(CpuIntervalConsume, '/cpu/<date_now>/<time_range>')
    api.add_resource(CpuCurrentConsume, '/cpu/<date_start>')
    api.add_resource(CpuIntervalPrediction,
                     '/cpu_predict/<date_start>/<time_range>')
    api.add_resource(CpuRandomPrediction,
                     '/random/<date_now>')

    api.add_resource(RamIntervalConsume, '/ram/<date_now>/<time_range>')
    api.add_resource(RamCurrentConsume, '/ram/<date_start>')
    api.add_resource(RamIntervalPrediction,
                     '/ram_predict/<date_start>/<time_range>')

    # api.add_resource(RamDetailsCurrentConsume, '/ram_details/<date_start>')
    # api.add_resource(CurrentHeapConsume,
    #                  '/heap/<date_start>')
    # api.add_resource(CurrentNonheapConsume,
    #                  '/nonheap/<date_start>')

    api.add_resource(ResponseTimeIntervalConsume,
                     '/response_time/<date_now>/<time_range>')
    api.add_resource(ResponseTimeCurrentConsume, '/response_time/<date_start>')

    api.add_resource(RequestCountIntervalConsume,
                     '/request_count/<date_now>/<time_range>')
    api.add_resource(RequestCountCurrentConsume, '/request_count/<date_start>')

    api.add_resource(
        Report, '/report/<time_range>/<email_to>')  # remover

    api.add_resource(JobsApi, '/jobs')
