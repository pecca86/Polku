''' JUTTU FORMS '''
from django import forms
from django.forms import fields
from django.http import request
from . import models
from .models import Juttu, Muistiinpanot, Poikkeamat, Salasanat
from laite.models import Laite
from laite.forms import LaiteForm
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import formset_factory


class SalasanaForm(forms.ModelForm):
    class Meta:
        model = Salasanat

        fields = (
            #'juttu',
            'juttu_salasana',
        )

        labels = {
            'juttu_salasana': _('Salasana'),
        }


class PoikkeamatForm(forms.ModelForm):
    class Meta:
        model = Poikkeamat

        fields = (
            #'juttu',
            'poikkeama',
            #'kirjauspvm',
            #'laite',
            'it_tutkija',
            'raporttiin',
        )

        labels = {
            'poikkeama': _('Lisää uusi poikkeustapaus'),
            'kirjauspvm': _('Kirjauspvm'),
            'raporttiin': _('Raporttiin'),
            'it_tutkija': _('IT-tutkija'),
        }

        widgets = {
            'kirjauspvm': forms.DateInput(attrs={'type': 'date'}),
        }

    #not working
    def __init__(self, *args, **kwargs):
        super(PoikkeamatForm, self).__init__(*args, **kwargs)
        #self.fields['laite'].queryset = Laite.objects.filter(juttu_id=self.instance.get_pk())



class MuistiinpanotForm(forms.ModelForm):

    model = Muistiinpanot

    class Meta:

        model = Muistiinpanot

        fields = (
            #'juttu',
            'muistiinpano',
            'kirjauspvm',
            'it_tutkija',
            'raporttiin',
        )

        labels = {
            'muistiinpano': _('Lisää uusi muistiinpano'),
            'kirjauspvm': _('Kirjauspvm'),
            'raporttiin': _('Raporttiin'),
            'it_tutkija': _('IT-tutkija'),
        }

        widgets = {
            'kirjauspvm': forms.DateInput(attrs={'type': 'date'}),
        }


class JuttuForm(forms.ModelForm):

    model = Juttu

    #Enables editing of existing forms
    class Meta:
        #model = Juttu #connects the form to the model
        model = Juttu

        #set editable fields
        fields = (
            'juttunumero',
            'case_nimi',
            'nimike',
            'etunimi',
            'sukunimi',
            'asianosaisuus',
            #'kohdehenkilo',
            'paattaja',
            #'tutkinnanjohtaja',
            'paatos_pvm',
            'tutkija',
            'ryhma',
            'teon_kuvaus',
            'toimenpidepyynto',
            'salasana',
            'pin_koodi',
            'kiireellisyys',
            #'user',
            #'juttu_status',
            #'kirjauspvm',
        )

        labels = {
            'juttu_status': _('Jutun status'),
            'case_nimi': _('Case nimi'),
            'etunimi': _('Kohdehenkilön etunimi'),
            'sukunimi': _('Kohdehenkilön sukunimi'),
            'paattaja': _('Laite-etsinnän päätöksen tekijä'),
            'paatos_pvm': _('Päätöksen pvm'),
            'ryhma': _('Ryhmä'),
            'salasana': _('Salasanat / Lukituskoodit / Piirtokoodit'),
            'pin_koodi': _('Puhelimen SIM-kortin PIN'),
            'toimenpidepyynto': _('Toimenpidepyyntö'),
            'asianosaisuus': _('Asema'),
            'teon_kuvaus': _('Jutun kuvaus'),
            'user': _('IT-tutkija'),
            } 

        help_texts = {
            'juttunumero': _('* pakollinen'),
            'case_nimi': _("jos liittyy caseen"),
            'nimike': _('* pakollinen'),
            'tutkija': _('* pakollinen'),
            'paattaja': _('* pakollinen'),
            'ryhma': _('* pakollinen'),
            'kohdehenkilo': _('SUKUNIMI, Etunimi'),
            'teon_kuvaus': _('Lyhyt selostus tutkittavasta jutusta'),
            'toimenpidepyynto': _('esim. kiinnostavat sovellukset, videot, kuvat jne.'),
            'salasana': _('esim. Laite: abc123 (=salasana), 1234 (=suojakoodi), 1-2-3-4 (=piirtokoodi)'),
        } 

        widgets = {
            'paatos_pvm': forms.DateInput(attrs={'type': 'date'}),
        }

