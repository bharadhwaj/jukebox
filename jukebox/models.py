import datetime

from django.db import models
from django.utils import timezone

class Link(models.Model):
    name         = models.CharField(max_length=511)
    url          = models.CharField(max_length=200, unique=True)
    video_id     = models.CharField(max_length=15, unique=True)
    votes        = models.IntegerField(default=0)
    publish_date = models.DateTimeField('date added', auto_now_add=True)

    def __str__(self):
        return self.url

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.publish_date <= now