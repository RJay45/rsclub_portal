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
    lastSuccess = models.DateTimeField(null=True)
    _date_format = "%d %b %Y, %H:%M:%S"

    def is_valid(self):
        """Returns True if this key is valid (now is between the start and end times)"""
        return self.startTime <= ApiKey.get_now() < self.endTime

    def update_last_valid(self):
        self.lastSuccess = ApiKey.get_now()
        self.save()

    @staticmethod
    def get_now():
        return timezone.make_aware(datetime.now(), timezone.get_current_timezone())

    @staticmethod
    def get_valid():
        """Get all ApiKeys that are valid."""
        now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
        keys = ApiKey.objects.all().filter(startTime__lte=now).filter(endTime__gt=now).order_by('-lastSuccess')
        # print(keys.query)
        return keys

    def formatted_url(self):
        if self.is_valid():
            return self.url
        else:
            return ApiKey._add_strike(self.url)
    formatted_url.short_description = "URL"

    def formatted_user_id(self):
        if self.is_valid():
            return self.userId
        else:
            return ApiKey._add_strike(self.userId)
    formatted_user_id.short_description = "User ID"

    def formatted_auth_key(self):
        if self.is_valid():
            return self.authKey
        else:
            return ApiKey._add_strike(self.authKey)
    formatted_auth_key.short_description = "Key"

    def formatted_start_time(self):
        if self.is_valid():
            return self.startTime.strftime(ApiKey._date_format)
        else:
            return ApiKey._add_strike(self.startTime.strftime(ApiKey._date_format))
    formatted_start_time.short_description = "Start Time"

    def formatted_end_time(self):
        if self.is_valid():
            return self.endTime.strftime(ApiKey._date_format)
        else:
            return ApiKey._add_strike(self.endTime.strftime(ApiKey._date_format))
    formatted_end_time.short_description = "End Time"

    def formatted_last_success(self):
        if self.is_valid():
            if self.lastSuccess is None:
                return "Never"
            else:
                return self.lastSuccess.strftime(ApiKey._date_format)
        else:
            if self.lastSuccess is None:
                return ApiKey._add_strike("Never")
            else:
                return ApiKey._add_strike(self.lastSuccess.strftime(ApiKey._date_format))
    formatted_last_success.short_description = "Last Success"

    @staticmethod
    def _add_strike(value):
        return format_html("<span style=\"text-decoration: line-through;\">" + value + "</span>")

    def __str__(self):
        return '%s:%s' % (self.userId, self.authKey)
