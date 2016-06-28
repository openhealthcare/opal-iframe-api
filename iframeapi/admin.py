from django.contrib import admin
from reversion.admin import VersionAdmin
from iframeapi import models


class ApiKeyAdmin(VersionAdmin):
    list_display = ['name', 'key', 'last_used']

admin.site.register(models.ApiKey, ApiKeyAdmin)
