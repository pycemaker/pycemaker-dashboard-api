from mongoengine import Document, StringField


class AlertPredictArgs(Document):
    user_id = StringField()
    job_name = StringField()
    email_to = StringField()
    start_date = StringField()
    interval = StringField()
    cpu_trigger = StringField()
    ram_trigger = StringField()
    response_time_trigger = StringField()
    request_count_trigger = StringField()
