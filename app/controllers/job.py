from datetime import datetime
import json
from random import triangular
import time
import traceback
from flask import Response, jsonify, request
from flask_restful import Resource
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pymongo import MongoClient
import os
from app.entities.alert_predict_args import AlertPredictArgs
from app.entities.report_args import ReportArgs

from app.services.pycemaker import Pycemaker
from app.services.reporter import Reporter
from app.entities.jobs_args import JobsArgs
from app.services.pcm_scheduler import PcmScheduler

mongo = MongoClient(os.environ.get("MONGO_DB_URL"))

jobstores = {
    'default': MongoDBJobStore(database="pycemaker", client=mongo, collection="jobs")
}

scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()


class JobsApi(Resource):

    def get(self) -> Response:

        try:
            pcm_scheduler = PcmScheduler(scheduler)
            lista = pcm_scheduler.get_jobs("admin")
            return jsonify(lista)

        except Exception as err:
            data = {'msg': err.message}
            return data, 400

    def post(self) -> Response:

        try:

            request_data = request.get_json()
            request_data["user_id"] = "admin"

            pcm_scheduler = PcmScheduler(scheduler)
            jobs = pcm_scheduler.schedule_jobs(request_data)

            return jsonify(jobs)

        except Exception as err:
            data = {'msg': err.message}
            return data, 400

    def put(self) -> Response:

        try:
            request_data = request.get_json()
            request_data["user_id"] = "admin"
            request_data["usesdsr_id"] = "admin"

            pcm_scheduler = PcmScheduler(scheduler)
            jobs = pcm_scheduler.modify_jobs(request_data)

            return jsonify(jobs)

        except Exception as err:
            data = {'msg': err.message}
            return data, 400

    def delete(self) -> Response:

        try:
            pcm_scheduler = PcmScheduler(scheduler)
            lista = pcm_scheduler.remove_jobs("admin")
            return jsonify(lista)

        except Exception as err:
            data = {'msg': err.message}
            return data, 400


class RemoveJob(Resource):

    def get(self, job) -> Response:
        scheduler.remove_job(job)
        return jsonify("%s foi encerrada" % (job))


class ScheduleMonitor(Resource):

    def get(self) -> Response:

        job = Pycemaker(
            prom_url="https://pcm-prometheus.herokuapp.com/api/v1/query")
        job = scheduler.add_job(job.save_data, 'interval',
                                seconds=5, id="pycemaker")
        return jsonify("job details: %s" % (job))
