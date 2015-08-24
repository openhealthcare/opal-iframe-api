"""
Unittests for opat
"""
from datetime import date, timedelta
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from opal.models import Patient
from iframeapi.models import ApiKey
from iframeapi.tests.models import (
    Demographics, Allergies, Antimicrobial, Diagnosis
)
from iframeapi.templatetags.datefuns import age

HOSPITAL_NUMBER = "AA00"
CONDITION_1 = "itching"
CONDITION_2 = "sweating"


class TemplateTagTest(TestCase):
    def test_age(self):
        last_year = date.today() - timedelta(days=370)
        self.assertEqual(age(last_year), 1)


class ModelTests(TestCase):
    def test_key_creation(self):
        """ key should be created when the api is created """
        key = ApiKey.objects.create(name="testing")
        self.assertTrue(bool(key.key))


class IframeApiTest(TestCase):

    urls = 'iframeapi.tests.urls'

    @classmethod
    def setUpClass(cls):
        cls.key = ApiKey.objects.create(name="testing")
        cls.patient = Patient.objects.create()
        cls.demographics = Demographics.objects.create(
            patient=cls.patient,
            hospital_number=HOSPITAL_NUMBER
        )
        cls.episode = cls.patient.create_episode()
        cls.client = Client()
        cls.url = reverse("iframe_api")
        super(IframeApiTest, cls).setUpClass()

    def get_request_dict(self, **kwargs):
        request_dict = {
            "hospitalNumber": self.demographics.hospital_number,
            "column": "allergies",
            "key": self.key.key
        }.copy()

        request_dict.update(**kwargs)
        return request_dict

    def test_empty_allergies(self):
        ''' an empty result set return blank html '''
        ApiKey.objects.create(name="testing")
        response = self.client.get(self.url, self.get_request_dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(strip_tags(response.content).strip()), 0)

    def test_allergies(self):
        allergy_detail = "fake allergy"
        Allergies.objects.create(
            details=allergy_detail,
            patient=self.patient
        )
        response = self.client.get(self.url, self.get_request_dict())

        self.assertContains(response, allergy_detail)

    def test_demographics(self):
        rd = self.get_request_dict(column="demographics")
        response = self.client.get(self.url, rd)
        self.assertContains(response, HOSPITAL_NUMBER)

    def create_diagnosis(self):
        today = date.today()
        yesterday = today - timedelta(1)
        d1 = Diagnosis.objects.create(
            condition=CONDITION_1,
            episode=self.episode,
            date_of_diagnosis=yesterday
        )
        d2 = Diagnosis.objects.create(
            condition=CONDITION_2,
            episode=self.episode,
            date_of_diagnosis=today
        )
        return d1, d2

    def test_diagnosis(self):
        condition = "itching"
        Diagnosis.objects.create(
            condition=condition,
            episode=self.episode
        )
        rd = self.get_request_dict(column="diagnosis")
        response = self.client.get(self.url, rd)
        self.assertContains(response, condition)

    def test_multiple_results(self):
        self.create_diagnosis()
        rd = self.get_request_dict(column="diagnosis")
        response = self.client.get(self.url, rd)
        self.assertContains(response, CONDITION_1)
        self.assertContains(response, CONDITION_2)

    def test_latest(self):
        self.create_diagnosis()
        rd = self.get_request_dict(column="diagnosis", latest=True)
        response = self.client.get(self.url, rd)
        self.assertContains(response, CONDITION_2)
        self.assertFalse(CONDITION_1 in response.content)

    def test_no_sort(self):
        Antimicrobial.objects.create(
            dose="dose 1",
            episode=self.episode
        )
        Antimicrobial.objects.create(
            dose="dose 2",
            episode=self.episode
        )
        rd = self.get_request_dict(column="antimicrobial", latest=True)
        response = self.client.get(self.url, rd)

        self.assertContains(
            response,
            "dose 2",
        )

        self.assertFalse("dose 1" in response)

    def test_missing_hospital_number(self):
        rd = self.get_request_dict(column="antimicrobial")
        del rd["hospitalNumber"]
        response = self.client.get(self.url, rd)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.template_name, "iframe_templates/bad_request.html")

    def test_missing_column(self):
        rd = self.get_request_dict(column="antimicrobial")
        del rd["column"]
        response = self.client.get(self.url, rd)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.template_name, "iframe_templates/bad_request.html")

    def test_model_with_no_template(self):
        # if they try and use a model with no template we let the know
        # they're doing it wrong
        rd = self.get_request_dict(column="notemplate")
        response = self.client.get(self.url, rd)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.template_name, "iframe_templates/template-not-found.html")
