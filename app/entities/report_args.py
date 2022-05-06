from mongoengine import Document, StringField


class ReportArgs(Document):
    user_id = StringField()
    job_name = StringField()
    email_to = StringField()
    start_date = StringField()
    interval = StringField()
