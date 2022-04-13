from flask_restful import Api

from .controllers.cpu import CpuCurrentConsume, CpuIntervalConsume
from .controllers.ram import RamCurrentConsume, RamIntervalConsume
from .controllers.disk import DiskCurrentConsume, DiskIntervalConsume
from .controllers.response_time import ResponseTimeCurrentConsume, ResponseTimeIntervalConsume
from .controllers.http_fail import HttpFailCurrentConsume, HttpFailIntervalConsume
from .controllers.report import Report


def create_routes(api: Api):
    api.add_resource(CpuIntervalConsume, '/cpu/<date_now>/<time_range>')
    api.add_resource(CpuCurrentConsume, '/cpu/<date_start>')
    
    api.add_resource(RamIntervalConsume, '/ram/<date_now>/<time_range>')
    api.add_resource(RamCurrentConsume, '/ram/<date_start>')
    
    api.add_resource(DiskIntervalConsume, '/disk/<date_now>/<time_range>')
    api.add_resource(DiskCurrentConsume, '/disk/<date_start>')
    
    api.add_resource(ResponseTimeIntervalConsume, '/reponse_time/<date_now>/<time_range>')
    api.add_resource(ResponseTimeCurrentConsume, '/reponse_time/<date_start>')
    
    api.add_resource(HttpFailIntervalConsume, '/http_fail/<date_now>/<time_range>')
    api.add_resource(HttpFailCurrentConsume, '/http_fail/<date_start>')

    api.add_resource(Report, '/report/<date_now>/<time_range>/<email_to>')