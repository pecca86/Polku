from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Laite)
admin.site.register(models.OheisLaite)
admin.site.register(models.LaiteStatus)
admin.site.register(models.LaiteTyyppi)
admin.site.register(models.LaiteDataStatus)
admin.site.register(models.LaiteSijainti)
admin.site.register(models.Oheislaitetyyppi)
admin.site.register(models.OheislaiteSijainti)
