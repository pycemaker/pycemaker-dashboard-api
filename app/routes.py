from flask_restful import Api

from .controllers.job import ModifyReport, ListJobs, ScheduleMonitor, RemoveJob, ScheduleReport
from .controllers.cpu import CpuCurrentConsume, CpuIntervalConsume, CpuIntervalPrediction, CpuRandomPrediction
from .controllers.ram import RamCurrentConsume, RamIntervalConsume
from .controllers.disk import DiskCurrentConsume, DiskIntervalConsume
from .controllers.response_time import ResponseTimeCurrentConsume, ResponseTimeIntervalConsume
from .controllers.http_fail import HttpFailCurrentConsume, HttpFailIntervalConsume
from .controllers.report import Report


def create_routes(api: Api):
    api.add_resource(CpuIntervalConsume, '/cpu/<date_now>/<time_range>')
    api.add_resource(CpuCurrentConsume, '/cpu/<date_start>')
    api.add_resource(CpuIntervalPrediction, '/cpus/<date_start>')
    api.add_resource(CpuRandomPrediction, '/cpuss/<date_now>')

    api.add_resource(RamIntervalConsume, '/ram/<date_now>/<time_range>')
    api.add_resource(RamCurrentConsume, '/ram/<date_start>')

    api.add_resource(DiskIntervalConsume, '/disk/<date_now>/<time_range>')
    api.add_resource(DiskCurrentConsume, '/disk/<date_start>')

    api.add_resource(ResponseTimeIntervalConsume,
                     '/reponse_time/<date_now>/<time_range>')
    api.add_resource(ResponseTimeCurrentConsume, '/reponse_time/<date_start>')

    api.add_resource(HttpFailIntervalConsume,
                     '/http_fail/<date_now>/<time_range>')
    api.add_resource(HttpFailCurrentConsume, '/http_fail/<date_start>')

    api.add_resource(Report, '/report/<date_now>/<time_range>/<email_to>')

    api.add_resource(ListJobs, '/jobs')
    api.add_resource(ScheduleReport, '/jobs/schedule_report')
    api.add_resource(ModifyReport, '/jobs/modify_report')
    api.add_resource(RemoveJob, '/jobs/remove/<job>')
    api.add_resource(ScheduleMonitor, '/jobs/schedule_monitor')
