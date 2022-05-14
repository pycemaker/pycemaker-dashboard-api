from mongoengine import Document, StringField, DateTimeField, FloatField, IntField


class CpuUsage(Document):
    consume_percent = StringField()
    origin_time_series = IntField()
    time_series = DateTimeField()
    criticity = StringField()
    value = FloatField()
