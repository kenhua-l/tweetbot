from django.db import models
from botapp import models as botappmodel

# Create your models here.
class History(models.Model):
    note_id = models.IntegerField(editable=False)
    topic = models.CharField(max_length=200, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    class Meta:
        ordering = ['-timestamp',]

class Note(models.Model):
    note = models.CharField(max_length=200)
    link = models.CharField(max_length=80, null=True, blank=True)
    topic = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
    class Meta:
        ordering = ['pk',]
