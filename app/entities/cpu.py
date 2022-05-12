from mongoengine import Document, StringField, DateTimeField, FloatField


class CpuUsage(Document):
    consume_percent = StringField()
    time_series = DateTimeField()
    criticity = StringField()
    value = FloatField()
