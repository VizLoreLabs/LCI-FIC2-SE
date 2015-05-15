from django.db import models
from djangotoolbox.fields import ListField, DictField, EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager

activity_table = {1: "Sitting Hand",
                  2: "Sitting Pocket",
                  3: "Walking Hand",
                  4: "Walking Pocket",
                  5: "Standing Hand",
                  6: "Standing Pocket",
                  7: "Upstairs",
                  8: "Downstairs"}

reduced_activity_table = {
    0: 0,
    1: 0,
    2: 1,
    3: 1,
    4: 2,
    5: 2,
    6: 3,
    7: 4
}

reduced_activity_table_json = {
    1: "sitting",
    2: "walking",
    3: "standing",
    4: "upstairs",
    5: "downstairs",
}


activity_table_json = {
    1: "sitting",
    2: "sitting",
    3: "walking",
    4: "walking",
    5: "standing",
    6: "standing",
    7: "upstairs",
    8: "downstairs"
}


class WifiEntry(models.Model):
    time_stamp = models.BigIntegerField()
    ssids = ListField()


class LocationEntry(models.Model):
    time_stamp = models.BigIntegerField()
    lat = models.FloatField()
    lon = models.FloatField()


class ActivityEntry(models.Model):
    svm_ech = ListField()
    svm = ListField()
    dt_ech = ListField()
    dt = ListField()


class DataRecord(models.Model):
    user_id = models.CharField(max_length=40)
    date_time = models.DateTimeField()
    objects = MongoDBManager()

    activity = EmbeddedModelField('ActivityEntry')
    wifi = ListField(EmbeddedModelField('WifiEntry'))
    location = ListField(EmbeddedModelField('LocationEntry'))

