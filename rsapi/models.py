from django.db import models


# Create your models here.
class ApiKey(models.Model):
    url = models.TextField()
    userId = models.CharField(max_length=255)
    authKey = models.CharField(max_length=255)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
