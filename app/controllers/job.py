from flask import Response, jsonify, request
from flask_restful import Resource
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pymongo import MongoClient
import os

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
