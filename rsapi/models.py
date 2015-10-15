from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.html import format_html


# Create your models here.
class ApiKey(models.Model):
    url = models.TextField()
    userId = models.CharField(max_length=255)
    authKey = models.CharField(max_length=255)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    def is_valid(self):
        now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
        return self.startTime >= now or self.endTime < now

    def formatted_url(self):
        if self.is_valid():
            return self.url
        else:
            return ApiKey._add_strike(self.url)

    def formatted_user_id(self):
        if self.is_valid():
            return self.userId
        else:
            return ApiKey._add_strike(self.userId)

    def formatted_auth_key(self):
        if self.is_valid():
            return self.authKey
        else:
            return ApiKey._add_strike(self.authKey)

    def formatted_start_time(self):
        if self.is_valid():
            return datetime.strftime(self.startTime, "%c")
        else:
            return ApiKey._add_strike(datetime.strftime(self.startTime, "%c"))

    def formatted_end_time(self):
        if self.is_valid():
            return datetime.strftime(self.endTime, "%c")
        else:
            return ApiKey._add_strike(datetime.strftime(self.endTime, "%c"))

    @staticmethod
    def _add_strike(value):
        return format_html("<span style=\"text-decoration: line-through;\">" + value + "</span>")

    def __unicode__(self):
        return u'%s:%s' % (self.userId, self.authKey)
