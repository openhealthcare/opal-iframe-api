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
from iframeapi.tests.models import Demographics, Allergies, Antimicrobial


class ModelTests(TestCase):
    def test_key_creation(self):
        """ key should be created when the api is created """
        key = ApiKey.objects.create(name="testing")
        self.assertTrue(bool(key.key))


class IframeApiTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = ApiKey.objects.create(name="testing")
        cls.patient = Patient.objects.create()
        cls.demographics = Demographics.objects.create(
            patient=cls.patient,
            hospital_number="AA00"
        )
        cls.episode_1 = cls.patient.create_episode()
        cls.episode_1.date_of_episode = date.today() - timedelta(1)
        cls.episode_1.save()
        cls.episode_2 = cls.patient.create_episode()
        cls.episode_2.date_of_episode = date.today()
        cls.episode_2.save()
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

    def test_multiple_antimicrobial(self):
        Antimicrobial.objects.create(
            dose="dose 1",
            episode=self.episode_1
        )
        Antimicrobial.objects.create(
            dose="dose 2",
            episode=self.episode_2
        )
        rd = self.get_request_dict(column="antimicrobial")
        response = self.client.get(self.url, rd)
        self.assertContains(response, "dose 1")
        self.assertContains(response, "dose 2")

    def test_most_recent_antimicrobial(self):
        Antimicrobial.objects.create(
            dose="dose 1",
            episode=self.episode_1
        )
        Antimicrobial.objects.create(
            dose="dose 2",
            episode=self.episode_2
        )
        rd = self.get_request_dict(column="antimicrobial", mostRecent=True)
        response = self.client.get(self.url, rd)

        self.assertContains(response, "dose 2")
        self.assertFalse("dose 1" in response)

    def test_missing_hospital_number(self):
        rd = self.get_request_dict(column="antimicrobial")
        del rd["hospitalNumber"]
        response = self.client.get(self.url, rd)
        self.assertContains(
            response,
            "missing hospital number or column",
            status_code=400
        )

    def test_missing_column(self):
        rd = self.get_request_dict(column="antimicrobial")
        del rd["column"]
        response = self.client.get(self.url, rd)
        self.assertContains(
            response,
            "missing hospital number or column",
            status_code=400
        )
