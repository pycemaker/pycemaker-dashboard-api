from mongoengine import Document, StringField, DateTimeField


class HttpFail(Document):
    consume_percent = StringField()
    time_series = StringField()
    convert_timeseries = StringField()
    criticity = StringField()
    value = StringField()
