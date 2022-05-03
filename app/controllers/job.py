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

from app.services.pycemaker import Pycemaker
from app.services.reporter import Reporter

mongo = MongoClient(os.environ.get("MONGO_DB_URL"))

jobstores = {
    'default': MongoDBJobStore(database="pycemaker", client=mongo, collection="jobs")
}

scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

class ListJobs(Resource):

    def get(self) -> Response:

        lista = []

        for job in scheduler.get_jobs():
            date = scheduler.get_job(job.id).next_run_time
            date = date.strftime("%a, %d %B %Y %H:%M:%S")
            lista.append({"id": job.id, "next_run": date})

        return jsonify(lista)


class ScheduleReport(Resource):

    def post(self) -> Response:

        request_data = request.get_json()

        start_date = datetime.strptime(
            request_data.get('start_date'), '%d-%m-%Y-%H-%M-%S')

        date_now = datetime.today().strftime('%d-%m-%Y-%H-%M-%S')  # remover
        time_range = request_data.get('time_range') + 220  # remover
        email_to = request_data.get('email_to')
        report = Reporter(date_now, time_range, email_to)

        job = scheduler.add_job(func=report.get_report, trigger='interval',
                                hours=6, start_date=start_date, id="report")
        return jsonify("job details: %s" % (job))


class ModifyReport(Resource):

    def post(self) -> Response:

        request_data = request.get_json()

        start_date = datetime.strptime(
            request_data.get('start_date'), '%d-%m-%Y-%H-%M-%S')

        date_now = datetime.today().strftime('%d-%m-%Y-%H-%M-%S')  # remover
        time_range = request_data.get('time_range') + 229  # remover
        email_to = request_data.get('email_to')
        report = Reporter(date_now, time_range, email_to)

        scheduler.modify_job(job_id="report", func=report.get_report, args=[])
        job = scheduler.reschedule_job(job_id="report", trigger='interval',
                                       hours=6, start_date=start_date)

        return jsonify("job details: %s" % (job))


class RemoveJob(Resource):

    def get(self, job) -> Response:
        scheduler.remove_job(job)
        print("%s foi encerrada" % (job))
        return jsonify("%s foi encerrada" % (job))


class ScheduleMonitor(Resource):

    def get(self) -> Response:

        job = Pycemaker(
            prom_url="https://pcm-prometheus.herokuapp.com/api/v1/query")
        job = scheduler.add_job(job.save_data, 'interval',
                                seconds=5, id="pycemaker")
        return jsonify("job details: %s" % (job))
