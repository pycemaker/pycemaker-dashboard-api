from mongoengine import Document, StringField, DateTimeField


class JvmMemoryUsageDetails(Document):
    time_series = StringField()
    convert_timeseries = StringField()
    jvm_memory_area_id = StringField()
    value = StringField()
    jvm_memory_area = StringField()
