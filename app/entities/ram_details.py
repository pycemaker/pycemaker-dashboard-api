from mongoengine import Document, StringField, DateTimeField, FloatField, LongField


class JvmMemoryUsageDetails(Document):
    time_series = DateTimeField()
    heap_value_bytes = LongField()
    heap_consume_bytes = StringField()
    heap_value_percent = FloatField()
    heap_consume_percent = StringField()
    nonheap_value_bytes = LongField()
    nonheap_consume_bytes = StringField()
    nonheap_value_percent = FloatField()
    nonheap_consume_percent = StringField()
