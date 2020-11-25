''' LAITE MODELS '''
from typing import Tuple
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.utils.text import slugify
from django.forms import widgets
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

#import misaka

from juttu.models import Juttu, Salasanat


class Laite(models.Model):

    juttu = models.ForeignKey(Juttu, related_name='juttus', null=True, blank=True, on_delete=models.CASCADE)#"foreign key"
    #slug = models.SlugField(allow_unicode=True, unique=True, default='')
    IMEI = models.CharField(max_length=512, null=True, blank=True, default="")
    IMEI2 = models.CharField(max_length=512, null=True, blank=True, default="")
    IMEI3 = models.CharField(max_length=512, null=True, blank=True, default="")
    sarjanumero = models.CharField(max_length=512, null=True, blank=True, default="")
    sinettipussi_id = models.CharField(max_length=512, null=True, blank=True, default="")
    valmistaja = models.CharField(max_length=512, null=True, blank=True, default="")
    malli = models.CharField(max_length=512, null=True, blank=True, default="")
    laite_tyyppi = models.ForeignKey("LaiteTyyppi", related_name='laite_laitetyyppi', null=True, on_delete=models.SET_NULL)
    # laite_tyyppi = models.CharField(max_length=512, choices=LAITE_TYYPPI, default='', verbose_name= _('Laitetyyppi'))
    kapasiteetti = models.IntegerField(default=0, verbose_name= _('Koko (GB)'))
    kayttojarjestelma = models.CharField(max_length=512, null=True, blank=True, default="", verbose_name= _('Käyttöjärjestelmä'))
    chipset = models.CharField(max_length=512, null=True, blank=True, default="")
    #laite_status = models.CharField(max_length=512, choices=LAITE_STATUS, default='Otettu vastaan', verbose_name= _('Status'))
    laite_status = models.ForeignKey("LaiteStatus", related_name="laite_laitestatus", null=True, on_delete=models.SET_NULL) #default="Otettu vastaan"
    laite_suojakoodi = models.CharField(max_length=512, null=True, blank=True, default="")
    pakkokeinonro = models.CharField(max_length=512, null=True, blank=True, default="")
    esinenro = models.CharField(max_length=512, null=True, blank=True, default="")
    kirjauspvm = models.DateField(widgets.SelectDateWidget, default=timezone.now)
    lisatietoja = models.CharField(max_length=512, null=True, blank=True, default="", verbose_name= _('Lisätietoja'))
    sijainti = models.ForeignKey("LaiteSijainti", related_name="laite_laitesijainti",null=True, on_delete=models.SET_NULL)
    # sijainti = models.CharField(max_length=512, choices=LAITE_SIJAINTI, default='Vastaan.ot. lokerossa')
    raporttiin = models.BooleanField(default=True)
    laite_data_status = models.ForeignKey("LaiteDataStatus", null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'on_aktiivinen':True})



    def __str__(self):
        if ( str(self.malli) and str(self.valmistaja) == "None" ):
            return "Tuntematon laite"

        if ( str(self.malli) == "None"):
            return self.valmistaja + ", Tuntematon malli"
        
        else:
            return str(self.valmistaja) + ", " + str(self.malli) + " (" + self.juttu.juttunumero +")"

    def save(self, *args, **kwargs):
        super().save() #need to save so that we get a new object, hence an obj.id
        #Automatically creates a muistiinpano instance for the newly created laite
        try:
            obj = LaiteMuistiinpano.objects.get(laite_id=self.pk)
        except LaiteMuistiinpano.DoesNotExist:
            obj = LaiteMuistiinpano(laite_id=self.pk)
            obj.save()
        super().save(*args, **kwargs)


    #Where to redirect after submitting form
    def get_absolute_url(self):
        laiteid = self.pk
        field_value = Laite.objects.get(id=laiteid).juttu_id #last specifies what field's value we want to capture

        return reverse_lazy("juttu:jutun_laitteet", kwargs={'pk': field_value})

        #return reverse("laite:single_laite", kwargs={"pk":self.pk}) #  <-- this redirect to the detailview of the device we just made
        #return reverse("laite:single_laite", kwargs={"slug":self.slug}) #  <-- this redirect to the detailview of the device we just made
    

class OheisLaite(models.Model):

    laite = models.ForeignKey(Laite, related_name="varsinainen_laite", on_delete=models.CASCADE)
    valmistaja = models.CharField(max_length=512, default="")
    malli = models.CharField(max_length=512, null=True, blank=True,  default="")
    #oheislaite_tyyppi = models.CharField(max_length=512, choices=OHEISLAITE_TYYPPI, default='', verbose_name= _('Laitetyyppi'))
    oheislaite_tyyppi = models.ForeignKey("OheislaiteTyyppi", related_name="oheislaite_ohtyyppi", null=True, on_delete=models.SET_NULL, limit_choices_to={'on_aktiivinen':True})
    #oheislaite_status = models.CharField(max_length=512, choices=LAITE_STATUS, default='', verbose_name= _('Status'))
    oheislaite_status = models.ForeignKey("LaiteStatus", null=True, on_delete=models.SET_NULL, default="Otettu vastaan", limit_choices_to={'on_aktiivinen':True})
    #oheislaite_sijainti = models.CharField(max_length=512, choices=OHEISLAITTEEN_SIJAINTI, default='', verbose_name= _('Sijainti'))
    oheislaite_sijainti = models.ForeignKey("OheislaiteSijainti", null=True, on_delete=models.SET_NULL, limit_choices_to={'on_aktiivinen':True})
    sarjanumero = models.CharField(max_length=512, null=True, blank=True, default="")
    oheislaite_suojakoodi = models.CharField(max_length=512, null=True, blank=True, default="")
    ICCID = models.CharField(max_length=512, null=True, blank=True, default="")
    IMSI = models.CharField(max_length=512, null=True, blank=True, default="")
    kapasiteetti = models.IntegerField(default=0, verbose_name= _('Koko (GB)'))
    kirjauspvm = models.DateField(widgets.SelectDateWidget, default=timezone.now)
    lisatietoja = models.CharField(max_length=512, null=True, blank=True, default="", verbose_name= _('Lisätietoja'))
    raporttiin = models.BooleanField(default=True)


    def __str__(self):
        if self.oheislaite_tyyppi == "":
            return self.valmistaja
        return str(self.oheislaite_tyyppi) + ": " + self.valmistaja


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


     #Where to redirect after submitting form
     # This implementations redirects back to the juttu laite view
    def get_absolute_url(self):
        #Grab this views id (=oheislaite pk)
        oheislaite_id = self.pk
        #Grab the laite id associated with the oheislaite
        laite_value = OheisLaite.objects.get(id=oheislaite_id).laite_id
        #Grab the juttu id associated with the laite
        return_value_pk = Laite.objects.get(id=laite_value).juttu_id 

        #Use this id to then reverse back  to the correct juttu
        return reverse_lazy("juttu:jutun_laitteet", kwargs={'pk': return_value_pk})

    

class LaiteMuistiinpano(models.Model):
    laite = models.ForeignKey(Laite, related_name='laite_note', on_delete=models.CASCADE)
    laite_muistiinpano = models.TextField(blank=True)
    kirjauspvm = models.DateField(widgets.SelectDateWidget, default=timezone.now)
    raporttiin = models.BooleanField(default=True)
    parsitut_sovellukset = models.CharField(max_length=512, blank=True,  default="")
    parsimatta_jaaneet_sovellukset = models.CharField(max_length=512, blank=True,  default="")
    physical = models.BooleanField(default=False)
    fullfilesystem = models.BooleanField(default=False)
    filesystem = models.BooleanField(default=False)
    apk_downgrade = models.BooleanField(default=False)
    logical = models.BooleanField(default=False)
    live = models.BooleanField(default=False)
    #physical_menetelma = models.CharField(max_length=512, blank=True,  default="")
    #TODO: physical_menetelma kenttä "pop-upina" laite listaan

    def __str__(self):
        return self.laite_muistiinpano

    def save(self, *args, **kwargs):
        super().save() #first save, so that we get an primary key to refer to in our slugify
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        #Grab this views id (=oheislaite pk)
        muistiinpano_id = self.pk
        #Grab the laite id associated with the oheislaite
        laite_value = LaiteMuistiinpano.objects.get(id=muistiinpano_id).laite_id
        #Grab the juttu id associated with the laite
        return_value_pk = Laite.objects.get(id=laite_value).juttu_id 
        return reverse("juttu:jutun_laitteet",  kwargs={'pk': return_value_pk})



class LaiteStatus(models.Model):
    laite_status = models.CharField(max_length=512, blank=True)
    on_aktiivinen = models.BooleanField(default=True)

    def __str__(self):
        return self.laite_status


class LaiteTyyppi(models.Model):
    laitetyyppi = models.CharField(max_length=512, blank=True)
    on_aktiivinen = models.BooleanField(default=True)

    def __str__(self):
        return self.laitetyyppi


class LaiteSijainti(models.Model):
    laitesijainti = models.CharField(max_length=512, blank=True)
    on_aktiivinen = models.BooleanField(default=True)

    def __str__(self):
        return self.laitesijainti

class LaiteDataStatus(models.Model):
    laite_data_status = models.CharField(max_length=512, blank=True)
    on_aktiivinen = models.BooleanField(default=True)
    datatyyppi_sailytyksessa = models.BooleanField(default=False)

    def __str__(self):
        return self.laite_data_status


class Oheislaitetyyppi(models.Model):
    oheislaitetyyppi = models.CharField(max_length=512, blank=True)
    on_aktiivinen = models.BooleanField(default=True)

    def __str__(self):
        return self.oheislaitetyyppi


class OheislaiteSijainti(models.Model):
    oheislaitesijainti = models.CharField(max_length=512, blank=True)
    on_aktiivinen = models.BooleanField(default=True)

    def __str__(self):
        return self.oheislaitesijainti