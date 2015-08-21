from django.contrib import admin
import reversion
from iframeapi import models


class ApiKeyAdmin(reversion.VersionAdmin):
    list_display = ['name', 'key', 'last_used']

admin.site.register(models.ApiKey, ApiKeyAdmin)
