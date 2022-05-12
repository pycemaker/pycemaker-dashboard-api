from mongoengine import Document, StringField, DateTimeField, FloatField


class RequestCount(Document):
    time_series = DateTimeField()
    criticity = StringField()
    value = FloatField()
