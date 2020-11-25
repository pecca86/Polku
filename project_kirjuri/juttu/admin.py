from django.contrib import admin
from . import models


# Register your models here.

class JuttuInline(admin.TabularInline):
    model = models.Juttu

class MuistiinpanoInline(admin.TabularInline):
    model = models.Muistiinpanot


class TutkintaRymhat():
    model = models.TutkintaRyhma


class Salasanat():
    model = models.Salasanat

class JuttuStatus():
    model = models.JuttuStatus

admin.site.register(models.Juttu)
admin.site.register(models.Salasanat)
admin.site.register(models.TutkintaRyhma)
admin.site.register(models.JuttuStatus)


