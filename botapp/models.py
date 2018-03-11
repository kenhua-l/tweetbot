from django.db import models

# Create your models here.
class TwitterProfile(models.Model):
    consumer_token = models.CharField(max_length=200)
    consumer_secret = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    access_secret = models.CharField(max_length=200)

class Topic(models.Model):
    title = models.CharField(max_length=200)
    rank = models.IntegerField()
    def getChoices():
        if Topic.objects.all().exists():
            return tuple((tc.title, tc.title) for tc in Topic.objects.all())
        else:
            return (('general topic', 'general topic'))

    def getDefault():
        if Topic.objects.all().exists():
            return Topic.objects.all()[0].title
        else:
            return 'generic topic'

class Schedule(models.Model):
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
