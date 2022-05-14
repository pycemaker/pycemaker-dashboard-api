from mongoengine import Document, StringField, DateTimeField, FloatField, IntField


class JvmMemoryUsage(Document):
    consume_percent = StringField()
    origin_time_series = IntField()
    time_series = DateTimeField()
    criticity = StringField()
    value = FloatField()
