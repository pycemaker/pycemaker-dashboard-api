from flask_restful import Api

from .controllers.job import RemoveJob, ScheduleMonitor, JobsApi
from .controllers.cpu import CpuCurrentConsume, CpuIntervalConsume, CpuIntervalPrediction, CpuRandomPrediction
from .controllers.ram import CurrentHeapConsume, CurrentNonheapConsume, RamCurrentConsume, RamDetailsCurrentConsume, RamDetailsIntervalConsume, RamIntervalConsume
from .controllers.disk import DiskCurrentConsume, DiskIntervalConsume
from .controllers.response_time import ResponseTimeCurrentConsume, ResponseTimeIntervalConsume
from .controllers.http_fail import HttpFailCurrentConsume, HttpFailIntervalConsume
from .controllers.report import Report


def create_routes(api: Api):
    api.add_resource(CpuIntervalConsume, '/cpu/<date_now>/<time_range>')
    api.add_resource(CpuCurrentConsume, '/cpu/<date_start>')
    api.add_resource(CpuIntervalPrediction,
                     '/cpu_predict/<date_start>')  # cpus
    api.add_resource(CpuRandomPrediction,
                     '/random/<date_now>')  # remover #cpuss

    api.add_resource(RamIntervalConsume, '/ram/<date_now>/<time_range>')
    api.add_resource(RamCurrentConsume, '/ram/<date_start>')

    # api.add_resource(RamDetailsIntervalConsume,
    #                  '/ram_details/<date_now>/<time_range>')

    api.add_resource(RamDetailsCurrentConsume, '/ram_details/<date_start>')
    api.add_resource(CurrentHeapConsume,
                     '/heap/<date_start>')
    api.add_resource(CurrentNonheapConsume,
                     '/nonheap/<date_start>')

    # api.add_resource(DiskIntervalConsume, '/disk/<date_now>/<time_range>')
    # api.add_resource(DiskCurrentConsume, '/disk/<date_start>')

    api.add_resource(ResponseTimeIntervalConsume,
                     '/reponse_time/<date_now>/<time_range>')
    api.add_resource(ResponseTimeCurrentConsume, '/reponse_time/<date_start>')

    api.add_resource(HttpFailIntervalConsume,
                     '/http_fail/<date_now>/<time_range>')
    api.add_resource(HttpFailCurrentConsume, '/http_fail/<date_start>')

    api.add_resource(
        Report, '/report/<date_now>/<time_range>/<email_to>')  # remover

    api.add_resource(JobsApi, '/jobs')
    api.add_resource(RemoveJob, '/job/<job>')  # remover
    api.add_resource(ScheduleMonitor, '/job/monitor')  # remover
