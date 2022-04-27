from datetime import datetime
import time
import traceback
from flask import Response, jsonify
from flask_restful import Resource
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pymongo import MongoClient

from app.services.pycemaker import Pycemaker

mongo = MongoClient('localhost', 27017)

jobstores = {
    'default': MongoDBJobStore(database="pycemaker", client=mongo, collection="schedulejob")
}

scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()


def printing_something(text):
    print("%s: %s" % (text, datetime.now()))


def do_this_first():
    if any(job.id == 'job1' for job in scheduler.get_jobs()):
        print("Achou")
    if not any(job.id == 'job1' for job in scheduler.get_jobs()):
        print("Não achou")
        scheduler.add_job(printing_something, 'interval',
                          seconds=5, id="job1", args=["job1"])


class listar(Resource):

    def get(self) -> Response:

        lista = []

        for job in scheduler.get_jobs():
            lista.append({"id": job.id})
            print("id: %s" % (job.id))

        return jsonify(lista)


class adicionar(Resource):

    def get(self, job) -> Response:

        scheduler.add_job(printing_something, 'interval',
                          seconds=5, id=job, args=[job])
        return jsonify("job details: %s" % (scheduler))


class remover(Resource):

    def get(self, job) -> Response:
        time.sleep(1)
        scheduler.remove_job(job)
        print("%s foi encerrada" % (job))
        return jsonify("%s foi encerrada" % (job))


class new_job(Resource):

    def get(self) -> Response:

        job = Pycemaker(prom_url="http://localhost:9090/api/v1/query")
        scheduler.add_job(job.save_data, 'interval',
                          seconds=5, id="job1")
        return jsonify("Criando job")
