from project_kirjuri.juttu.models import Juttu
from django.test import TestCase
from .models import Juttu

# Create your tests here.

class JuttuTestCase(TestCase):

    def test_juttu_created(self):
        juttu_obj = Juttu.objects.create(juttunumero="5530/R/TEST/20", slug="feqfq", nimike="Homo", tutkinnnanjohtaja="bögolle", tutkija="Fjalle", ryhma="ESPRIKTA", kohdehenkilo="Olli")
        self.assertEqual(juttu_obj.id, 1)