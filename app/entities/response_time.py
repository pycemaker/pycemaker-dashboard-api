from mongoengine import Document, StringField, DateTimeField, FloatField


class ResponseTime(Document):
    time_series = DateTimeField()
    criticity = StringField()
    value = FloatField()
