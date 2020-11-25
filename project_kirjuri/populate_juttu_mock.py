import os
from random import randint
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_kirjuri.settings')

import django
django.setup()

#FAKE POP SCRIPT

import random
import uuid
from juttu.models import Juttu
from faker import Faker

fakegen = Faker()

fake_juttunumero = "5530_R_1234_20"
fake_number = set(fakegen.unique.random_int(min=1, max=400) for i in range(200))

def populate(N):

    for entry in range(N):
        j = Juttu(
                #id=fake_number.pop(),
                juttunumero=fake_juttunumero, #[0]
                slug= uuid.uuid1(),
                nimike="test_nim",
                ryhma="ESPRIKTA",
                kiireellisyys="Normaali",
                etunimi="TestEtu",
                sukunimi="TestSuku",
                paattaja="TestPaat",
            )[0]
        #j.save()

if __name__ == '__main__':
    print("Populating")
    populate(1)
    print("Done!")
