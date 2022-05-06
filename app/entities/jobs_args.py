from xmlrpc.client import Boolean
from mongoengine import Document, StringField, ListField, BooleanField


class JobsArgs(Document):
    user_id = StringField()
    report = BooleanField()
    alert_predict = BooleanField()
    email_to = StringField()
    start_date = StringField()
    interval = StringField()
    cpu_trigger = StringField()
    ram_trigger = StringField()
    response_time_trigger = StringField()
    request_count_trigger = StringField()
