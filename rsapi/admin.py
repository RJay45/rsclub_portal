from django.contrib import admin
from .models import ApiKey


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('formatted_user_id', 'formatted_auth_key', 'formatted_start_time', 'formatted_end_time',
                    'formatted_last_success', 'formatted_url')
    search_fields = ('userId', 'authKey', 'url')
    ordering = ['-endTime']


# Register your models here.
admin.site.register(ApiKey, ApiKeyAdmin)
