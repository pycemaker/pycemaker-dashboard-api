from datetime import datetime
import json
from app.entities.alert_predict_args import AlertPredictArgs
from app.entities.jobs_args import JobsArgs
from app.entities.report_args import ReportArgs

from app.services.reporter import Reporter


class PcmScheduler:

    def __init__(self, scheduler):

        self.scheduler = scheduler

        self.user_id = ""

        self.start_date = ""
        self.start_time = ""
        self.interval = ""
        self.email_to = ""

        self.cpu_trigger = ""
        self.ram_trigger = ""
        self.response_time_trigger = ""
        self.request_count_trigger = ""

        self.report = ""

    # def save_jobs_args(self, data):

    #     jobs_args = JobsArgs(**data)
    #     jobs_args.save()

    #     return json.loads(jobs_args.to_json())

    def save_report_args(self, data):

        report_args = ReportArgs(**data)
        report_args.save()

        return json.loads(report_args.to_json())

    def save_alert_predict_args(self, data):

        alert_predict_args = AlertPredictArgs(**data)
        alert_predict_args.save()

        return json.loads(alert_predict_args.to_json())

    def schedule_report(self):

        id = self.user_id + "-report"
        job = self.scheduler.add_job(func=self.report.get_report, trigger='interval',
                                     hours=int(self.interval), start_date=self.start_date, id=id)

        return "job details: %s" % (job)

    # def schedule_alert_predict(self):

        # return "job details: %s" % (job)

    def schedule_jobs(self, request_data):

        lista =[]

        self.user_id = request_data.get("user_id")

        self.start_date = datetime.strptime(
            request_data.get('start_date'), '%d-%m-%Y-%H-%M-%S')
        self.start_time = self.start_date.strftime("%H-%M-%S")
        self.interval = request_data.get('interval')
        self.email_to = request_data.get('email_to')

        alert_predict = request_data.get('alert_predict')

        self.report = Reporter(self.interval, self.email_to)

        data = {
            "user_id": self.user_id,
            "job_name": self.user_id + "-report",
            "email_to": self.email_to,
            "start_date": self.start_time,
            "interval": self.interval,
        }

        job = self.schedule_report()

        report_args = self.save_report_args(data)

        lista.append(job)

        if (alert_predict):
            self.cpu_trigger = request_data.get('cpu_trigger')
            self.ram_trigger = request_data.get('ram_trigger')
            self.response_time_trigger = request_data.get(
                'response_time_trigger')
            self.request_count_trigger = request_data.get(
                'request_count_trigger')

            data = {
                "user_id": self.user_id,
                "job_name": self.user_id + "-alert_predict",
                "email_to": self.email_to,
                "start_date": self.start_date,
                "interval": self.interval,
                "cpu_trigger": self.cpu_trigger,
                "ram_trigger": self.ram_trigger,
                "response_time_trigger": self.response_time_trigger,
                "request_count_trigger": self.request_count_trigger
            }

            alert_predict_args = self.save_alert_predict_args(data)

            # lista.append(job)

            return lista

        return lista

    def modify_report_args(self, data):

        report_args = ReportArgs.objects(user_id=self.user_id).first()

        report_args.update(**data)

        return json.loads(report_args.to_json())

    def modify_alert_predict_args(self, data):

        alert_predict_args = AlertPredictArgs.objects(
            user_id=self.user_id).first()

        alert_predict_args.update(**data)

        return json.loads(alert_predict_args.to_json())

    # def modify_jobs_args(self):

    #     jobs_args = JobsArgs.objects(user_id=self.user_id).first()

    #     jobs_args.update(**self.request_data)

    #     return json.loads(jobs_args.to_json())

    def modify_schedule_report(self):

        id = self.user_id + "-report"

        self.scheduler.modify_job(
            job_id=id, func=self.report.get_report, args=[])
        job = self.scheduler.reschedule_job(job_id=id, trigger='interval',
                                            hours=int(self.interval), start_date=self.start_date)

        return "job details: %s" % (job)

    # def modify_schedule_alert_predict(self):

    #     return "job details: %s" % (job)

    def modify_jobs(self, request_data):

        lista =[]

        self.user_id = request_data.get("user_id")

        self.start_date = datetime.strptime(
            request_data.get('start_date'), '%d-%m-%Y-%H-%M-%S')
        self.start_time = self.start_date.strftime("%H-%M-%S")
        self.interval = request_data.get('interval')
        self.email_to = request_data.get('email_to')

        self.cpu_trigger = request_data.get('cpu_trigger')
        self.ram_trigger = request_data.get('ram_trigger')
        self.response_time_trigger = request_data.get('response_time_trigger')
        self.request_count_trigger = request_data.get('request_count_trigger')

        alert_predict = request_data.get('alert_predict')

        self.report = Reporter(self.interval, self.email_to)

        data = {
            "user_id": self.user_id,
            "job_name": self.user_id + "-report",
            "email_to": self.email_to,
            "start_date": self.start_time,
            "interval": self.interval,
        }

        job = self.modify_schedule_report()

        report_args = self.modify_report_args(data)

        lista.append(job)

        if (alert_predict):
            self.cpu_trigger = request_data.get('cpu_trigger')
            self.ram_trigger = request_data.get('ram_trigger')
            self.response_time_trigger = request_data.get(
                'response_time_trigger')
            self.request_count_trigger = request_data.get(
                'request_count_trigger')

            data = {
                "user_id": self.user_id,
                "job_name": self.user_id + "-alert_predict",
                "email_to": self.email_to,
                "start_date": self.start_date,
                "interval": self.interval,
                "cpu_trigger": self.cpu_trigger,
                "ram_trigger": self.ram_trigger,
                "response_time_trigger": self.response_time_trigger,
                "request_count_trigger": self.request_count_trigger
            }

            alert_predict_args = self.modify_alert_predict_args(data)

            # lista.append(job)

            return lista

        return lista

    def get_jobs(self, user_id):

        jobs = []
        report_args = ReportArgs.objects(user_id=user_id).first()
        if report_args:
            report_args = json.loads(report_args.to_json())

        alert_predict_args = AlertPredictArgs.objects(user_id=user_id).first()
        if alert_predict_args:
            alert_predict_args = json.loads(alert_predict_args.to_json())

        for x in self.scheduler.get_jobs():
            if report_args:
                if report_args["job_name"] == x.id:
                    # convverter date

                    report_args["next_run_time"] = x.next_run_time
                    jobs.append(report_args)
            if alert_predict_args:
                if alert_predict_args["job_name"] == x.id:
                    # convverter date
                    alert_predict_args["next_run_time"] = x.next_run_time
                    jobs.append(alert_predict_args)

        return jobs

    def remove_jobs(self, user_id):

        report_args = ReportArgs.objects(user_id=user_id).first()
        report_args_json = None
        if report_args:
            report_args_json = json.loads(report_args.to_json())

        alert_predict_args = AlertPredictArgs.objects(user_id=user_id).first()
        alert_predict_args_json = None
        if alert_predict_args:
            alert_predict_args_json = json.loads(alert_predict_args.to_json())

        lista = []
        for x in self.scheduler.get_jobs():
            if report_args_json:
                if report_args_json["job_name"] == x.id:
                    report_args.delete()
                    self.scheduler.remove_job(x.id)
                    lista.append("%s foi encerrada" % (x.id))
            if alert_predict_args_json:
                if alert_predict_args_json["job_name"] == x.id:
                    alert_predict_args.delete()
                    self.scheduler.remove_job(x.id)
                    lista.append("%s foi encerrada" % (x.id))

        return lista
