from flask_restful import Api

from app.controllers.cpu import CpuCurrentConsume, CpuIntervalConsume, CpuIntervalPrediction, CpuRandomPrediction
from app.controllers.fail_request_count import FRequestCountCurrentConsume, FRequestCountIntervalConsume
from app.controllers.job import JobsApi
from app.controllers.ram import RamCurrentConsume, RamDetailsCurrentConsume, RamIntervalConsume, RamIntervalPrediction
from app.controllers.report import Report
from app.controllers.request_count import RequestCountCurrentConsume, RequestCountIntervalConsume
from app.controllers.response_time import ResponseTimeCurrentConsume, ResponseTimeIntervalConsume
from app.controllers.success_request_count import SRequestCountCurrentConsume, SRequestCountIntervalConsume


def create_routes(api: Api):
    api.add_resource(CpuIntervalConsume,
                     '/cpu/<date_now>/<time_range>')
    api.add_resource(CpuCurrentConsume,
                     '/cpu/<date_start>')
    api.add_resource(CpuIntervalPrediction,
                     '/cpu_predict/<date_start>/<time_range>')
    api.add_resource(CpuRandomPrediction,
                     '/random/<date_now>')

    api.add_resource(RamIntervalConsume,
                     '/ram/<date_now>/<time_range>')
    api.add_resource(RamCurrentConsume,
                     '/ram/<date_start>')
    api.add_resource(RamIntervalPrediction,
                     '/ram_predict/<date_start>/<time_range>')

    api.add_resource(RamDetailsCurrentConsume,
                     '/ram_details/<date_start>')

    api.add_resource(ResponseTimeIntervalConsume,
                     '/res_time/<date_now>/<time_range>')
    api.add_resource(ResponseTimeCurrentConsume,
                     '/res_time/<date_start>')

    api.add_resource(RequestCountIntervalConsume,
                     '/req_count/<date_now>/<time_range>')
    api.add_resource(RequestCountCurrentConsume,
                     '/req_count/<date_start>')

    api.add_resource(FRequestCountIntervalConsume,
                     '/fail_req_count/<date_now>/<time_range>')
    api.add_resource(FRequestCountCurrentConsume,
                     '/fail_req_count/<date_start>')

    api.add_resource(SRequestCountIntervalConsume,
                     '/success_req_count/<date_now>/<time_range>')
    api.add_resource(SRequestCountCurrentConsume,
                     '/success_req_count/<date_start>')

    api.add_resource(Report,
                     '/report/<time_range>/<email_to>')  # remover

    api.add_resource(JobsApi, '/jobs')
