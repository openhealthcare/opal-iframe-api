from opal import models as opal_models
from django.db import models


class Demographics(opal_models.PatientSubrecord):
    _is_singleton = True
    hospital_number = models.CharField(max_length=200, blank=True, null=True)


class Allergies(opal_models.PatientSubrecord):
    provisional = models.NullBooleanField()
    details = models.CharField(max_length=255, blank=True)


class Antimicrobial(opal_models.EpisodeSubrecord):
    dose = models.CharField(max_length=255, blank=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["dose"]

class Diagnosis(opal_models.Diagnosis):
    pass
