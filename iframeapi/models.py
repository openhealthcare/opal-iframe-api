"""
Models for iframeapi
"""
import string
import random
from django.db import models
from django.utils import timezone

KEY_LENGTH = 50


def generate_api_key():
    charset = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(charset) for _ in range(KEY_LENGTH))


class ApiKey(models.Model):
    key = models.CharField(max_length=KEY_LENGTH, editable=False, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    last_used = models.DateTimeField(editable=False, null=True, blank=True)

    def used(self):
        self.last_used = timezone.now()
        self.save()

    def get_api_key(self):
        while True:
            key = generate_api_key()
            if not self.__class__.objects.filter(key=key).exists():
                return key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.get_api_key()

        super(ApiKey, self).save(*args, **kwargs)
