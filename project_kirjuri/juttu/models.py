from django.db import models
from django.db.models.deletion import CASCADE
from django.forms import widgets
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.db.models import F
#import misaka
import datetime
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library() #Custom template tags

#SIGNAL TESTING
from django.db.models.signals import post_save
import smtplib
from django.core.mail import send_mail
from datetime import date, datetime


class Juttu(models.Model):

    #Here we gather all the multiple choises options:

    #kiireellisyys
    KIIREELLISYYS_LUOKAT = (
        ('Kiireellinen','Kiireellinen'),
        ('Normaali', 'Normaali'),
    )


    ASIANOSAISUUS = (
        ('Asianomistaja', 'AO'),
        ('Rikoksesta epäilty', 'RE'),
        ('Todistaja', 'Todistaja'),
        ('Muu', 'Muu'),
    )


    juttunumero = models.CharField(max_length=512, blank=False, default="")
    case_nimi = models.CharField(max_length=512, blank=True, null=True)
    nimike = models.CharField(max_length=512, blank=False, null=False, default="") #List of all available crimes?
    tutkija = models.CharField(max_length=512, blank=False, default="")
    ryhma = models.ForeignKey("TutkintaRyhma", related_name="jutun_ryhma", on_delete=models.CASCADE, limit_choices_to={'on_aktiivinen':True})
    kiireellisyys = models.CharField(max_length=512, choices=KIIREELLISYYS_LUOKAT, default='Normaali')
    etunimi = models.CharField(max_length=512, blank=True)
    sukunimi = models.CharField(max_length=512, blank=True)
    user = models.ForeignKey(User, related_name="user_juttus", blank=True, null=True, on_delete=models.CASCADE) # = it-tutkija
    teon_kuvaus = models.CharField(max_length=512, blank=True)
    toimenpidepyynto = models.CharField(max_length=512, blank=True)
    salasana = models.CharField(max_length=512, blank=True) #Tästä oma taulu
    pin_koodi = models.CharField(max_length=512, blank=True)
    kirjauspvm = models.DateTimeField(blank=True, null=True, default=timezone.now)
    juttu_status = models.ForeignKey("JuttuStatus", related_name="jutun_status", on_delete=models.CASCADE, default=1, limit_choices_to={'on_aktiivinen':True})
    asianosaisuus = models.CharField(max_length=512, choices=ASIANOSAISUUS, default='Rikoksesta epäilty')
    paattaja = models.CharField(max_length=512, blank=False, null=True) #Laite-etsinnän päättäjä
    paatos_pvm = models.DateField(widgets.SelectDateWidget, default=timezone.now) #Päätöksen pvm


    def __str__(self):
        #return self.juttunumero + " " + "(" + self.sukunimi + ", " + self.etunimi + ")"
        return f'{self.juttunumero} ({self.sukunimi.upper()}, {self.etunimi})'

    def get_kohdehenkilo(self):
        return f'{self.sukunimi.upper()}, {self.etunimi}'


    #Where to redirect after submitting form
    def get_absolute_url(self):
        return reverse("juttu:single_juttu", kwargs={"pk":self.pk})
        #return reverse("juttu:juttu_list")
    

    def save(self, *args, **kwargs):
        super().save() #first save, so that we get an primary key to refer to in our slugify
        super().save(*args, **kwargs)


## TESTING SIGNAL ##
def alert_user(sender, **kwargs):
    if kwargs['created']:
        pvm = datetime.now()
        aika = pvm.strftime("%d.%m.%Y, %H:%M:%S")
        print("UUSI JUTTU KIRJATTU: " + aika)

post_save.connect(alert_user, sender=Juttu)


class Muistiinpanot(models.Model):
    juttu = models.ForeignKey(Juttu,related_name='juttu_notes',on_delete=models.CASCADE)
    it_tutkija =  models.ForeignKey(User,related_name='user_muistiinpano', blank=True, null=True, on_delete=models.CASCADE, verbose_name= _('IT-Tutkija'))
    muistiinpano = models.TextField()
    kirjauspvm = models.DateField(widgets.SelectDateWidget, default=timezone.now)
    raporttiin = models.BooleanField(default=True)


    def __str__(self):
        return self.muistiinpano #Change this to something better

    def save(self, *args, **kwargs):
        super().save() #first save, so that we get an primary key to refer to in our slugify
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("juttu:juttu_muistiinpano", kwargs={"pk":self.juttu_id})



class Poikkeamat(models.Model):
    
    juttu = models.ForeignKey(Juttu,related_name='juttu_poikkeamat',on_delete=models.CASCADE)
    laite = models.ForeignKey('laite.Laite', related_name='laite_poikkeamat', null=True, blank=True, on_delete=CASCADE)
    poikkeama = models.TextField()
    kirjauspvm = kirjauspvm = models.DateField(widgets.SelectDateWidget, default=timezone.now)
    raporttiin = models.BooleanField(default=False)
    it_tutkija = models.ForeignKey(User,related_name='user_poikkeamat', blank=True, null=True, on_delete=models.CASCADE, verbose_name= _('IT-Tutkija'))
    
    def __str__(self):
        return self.poikkeama #Change this to something better

    def save(self, *args, **kwargs):
        super().save() 
        self.juttu_pk = self.juttu
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("juttu:juttu_poikkeamat", kwargs={"pk":self.juttu_id})



class Nimikkeet(models.Model):
    pass
    #nimike = "Multiple options"


class JuttuStatus(models.Model):
    status = models.CharField(max_length=512, blank=True)
    on_aktiivinen = models.BooleanField(default=True)
    valmis_status = models.BooleanField(default=False)
    aloittamatta_status = models.BooleanField(default=False)
    odottaa_status = models.BooleanField(default=False)
    aloitettu_status = models.BooleanField(default=False)

    def __str__(self):
        return self.status


class TutkintaRyhma(models.Model):
    tutkintaryhma = models.CharField(max_length=512, blank=True)
    on_aktiivinen = models.BooleanField(default=True)

    def __str__(self):
        return self.tutkintaryhma


class Salasanat(models.Model):
    
    juttu = models.ForeignKey(Juttu,related_name='juttu_salasanat',on_delete=models.CASCADE)
    juttu_salasana = models.CharField(max_length=512, blank=True)


    def __str__(self):
        return self.juttu_salasana #Change this to something better

    def save(self, *args, **kwargs):
        super().save() #first save, so that we get an primary key to refer to in our slugify
        self.juttu_pk = self.juttu
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("juttu:jutun_salasanat", kwargs={"pk":self.juttu_id})







