from mongoengine import Document, StringField, DateTimeField


class DiskUsage(Document):
    consume_percent = StringField()
    time_series = StringField()
    convert_timeseries = DateTimeField()
    criticity = StringField()
    value = StringField()
