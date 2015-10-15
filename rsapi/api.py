__author__ = 'jason'

from .models import ApiKey
from datetime import datetime

class Api:
    def __init__(self):
        now = datetime.now()
        keys = ApiKey.objects.all().filter(startTime__lte=now).filter(endTime__gt=now)
        print("Found the following keys:")
        print(keys)