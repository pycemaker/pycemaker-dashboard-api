from mongoengine import Document, StringField, DateTimeField


class JvmMemoryUsage(Document):
    consume_percent = StringField()
    time_series = StringField()
    convert_timeseries = StringField()
    criticity = StringField()
    value = StringField()
