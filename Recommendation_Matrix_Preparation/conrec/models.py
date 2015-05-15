from django.db import models

'''
    Ignore stores info about ignores.
    NOTE: To work with the database in Django you need to "makemigrations" and then "migrate".
    https://docs.djangoproject.com/en/1.7/topics/migrations/
'''


class Ignore(models.Model):
    uuid = models.CharField(max_length=30)
    ignored = models.CharField(max_length=30)


class Area(models.Model):
    lat_id = models.IntegerField()
    lng_id = models.IntegerField()


class Keys(models.Model):
    temp = models.CharField(max_length=60)
    real = models.CharField(max_length=40)
    time = models.DateTimeField(auto_now=True, auto_now_add=False)

