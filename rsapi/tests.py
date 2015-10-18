from django.test import TestCase
from rsapi.models import ApiKey
from datetime import datetime, timedelta
from django.utils import timezone


class ApiKeyTestCase(TestCase):
    def setUp(self):
        self.expired_key = ApiKey()
        self.valid_key = ApiKey()
        self.valid_key.userId = "12345"
        self.valid_key.authKey = "ABCDEF0123456789"
        self.valid_key.url = "https://test.httpapi.com/api/"
        self.valid_key.startTime = timezone.make_aware(
            datetime.strptime("01 Jan 1970, 00:00:00", ApiKey._date_format)
        )
        self.valid_key.endTime = timezone.make_aware(
            datetime.strptime("01 Jan 2100, 00:00:00", ApiKey._date_format)
        )

        self.expired_key.userId = "12345"
        self.expired_key.authKey = "ABCDEF0123456789"
        self.expired_key.url = "https://test.httpapi.com/api/"
        self.expired_key.startTime = timezone.make_aware(
            datetime.strptime("01 Jan 1970, 00:00:00", ApiKey._date_format)
        )
        self.expired_key.endTime = timezone.make_aware(
            datetime.strptime("01 Jan 1971, 00:00:00", ApiKey._date_format)
        )

        self.expired_key.save()
        self.valid_key.save()

    def test_date_form(self):
        self.assertEqual(ApiKey._date_format, "%d %b %Y, %H:%M:%S", "ApiKet date format string has changed.")

    def test_expired_key(self):
        self.assertEqual(self.expired_key.is_valid(), False, "Expired key is_valid()")

    def test_last_valid(self):
        self.valid_key.update_last_valid()
        verify = ApiKey.objects.get(pk=self.valid_key.pk)
        self.assertAlmostEquals(self.valid_key.lastSuccess, self.valid_key.get_now(), delta=timedelta(seconds=2))
        self.assertEquals(verify.lastSuccess, self.valid_key.lastSuccess)
