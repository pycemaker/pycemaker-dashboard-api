from mongoengine import Document, StringField, DateTimeField, FloatField, IntField


class ResponseTime(Document):
    origin_time_series = IntField()
    time_series = DateTimeField()
    criticity = StringField()
    value = FloatField()
    status = StringField()
