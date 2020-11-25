from django import forms
from . import models
from .models import Laite, Juttu, OheisLaite, LaiteMuistiinpano
from django.utils.translation import gettext_lazy as _
from django.forms import formset_factory


class LaiteMuistiinpanoForm(forms.ModelForm):

    class Meta():
        model = LaiteMuistiinpano
        fields = (
            'laite_muistiinpano',
            'kirjauspvm',
            'parsitut_sovellukset',
            'parsimatta_jaaneet_sovellukset',
            'physical',
            'fullfilesystem',
            'filesystem',
            'apk_downgrade',
            'logical',
            'live',
            'raporttiin',
        )


        labels = {
            "laite_muistiinpano": _("Laitteen muistiinpanot"),
            "parsitut_sovellukset": _("Parsitut sovellukset"),
            "parsimatta_jaaneet_sovellukset": _("Parsimatta jääneet sovellukset"),
            "kapasiteetti": _("Koko (GB)"),
            "physical": _("Physical"),
            "fullfilesystem": _("Full Filesystem"),
            "filesystem": _("Filesystem"),
            "apk_downgrade": _("APK Downgrade"),
            "logical": _("Logical"),
            "raporttiin": _("Lisää muistiinpano raporttiin"),
            "kirjauspvm": _("Kirjaus pvm"),
        }

        widgets = {
            'kirjauspvm': forms.DateInput(attrs={'type': 'date'}),
        }


class LaiteForm(forms.ModelForm):


    class Meta():
        model = Laite

        kapasiteetti = forms.CharField(label='Koko (GB)')

        fields = (
            "juttu", 
            "laite_status",
            "sijainti",
            "valmistaja",
            "malli",
            "laite_tyyppi",
            "kapasiteetti",
            "IMEI",
            "IMEI2",
            "IMEI3",
            "sarjanumero",
            "kayttojarjestelma",
            "chipset",
            "laite_suojakoodi",
            "pakkokeinonro",
            "esinenro",
            "sinettipussi_id",
            "lisatietoja",
            "kirjauspvm",
            "raporttiin",
            'laite_data_status',
            )

        labels = {
            "valmistaja": _("Valmistaja"),
            "malli": _("Malli"),
            "laite_tyyppi": _("Laitetyyppi"),
            "kapasiteetti": _("Koko (GB)"),
            "IMEI": _("IMEI"),
            "IMEI2": _("IMEI 2"),
            "IMEI3": _("eSIM IMEI"),
            "sarjanumero": _("Sarjanumero"),
            "kayttojarjestelma": _("Käyttöjärjestelmä"),
            "chipset": _("Chipset"),
            "laite_suojakoodi": _("Suojakoodi / salasana"),
            "pakkokeinonro": _("Pakkokeino nro"),
            "esinenro": _("Esine nro"),
            "sinettipussi_id": _("Sinettipussin ID"),
            "lisatietoja": _("Lisätietoja"),
            "laite_status": _("Status"),
            "sijainti": _('Laitteen sijainti'),
            "kirjauspvm": _("Kirjaus pvm"),
            "raporttiin": _("Raporttiin"),
            "laite_data_status": _("Datan status"),
        }

        widgets = {
            'kirjauspvm': forms.DateInput(attrs={'type': 'date'}),
        }




class OheisLaiteForm(forms.ModelForm):

    class Meta():
        model = OheisLaite
        fields = (
            "laite",
            "oheislaite_status",
            "valmistaja",
            "malli",
            "oheislaite_tyyppi",
            "oheislaite_sijainti",
            "sarjanumero",
            "oheislaite_suojakoodi",
            "ICCID",
            "IMSI",
            "kapasiteetti",
            "kirjauspvm",
            "lisatietoja",
            "raporttiin",
            )

        labels = {
            "laite": _("Laite"),
            "valmistaja": _("Valmistaja"),
            "malli": _("Malli"),
            "oheislaite_tyyppi": _("Laitetyyppi"),
            "kapasiteetti": _("Koko (GB)"),
            "IMSI": _("IMSI"),
            "ICCID": _("ICCID"),
            "sarjanumero": _("Sarjanumero"),
            "oheislaite_suojakoodi": _("Suojakoodi / salasana"),
            "lisatietoja": _("Lisätietoja"),
            "oheislaite_status": _("Status"),
            "oheislaite_sijainti": _('Laitteen sijainti'),
            "kirjauspvm": _("Kirjaus pvm"),
            "raporttiin": _("Raporttiin"),
        }

        help_texts = {
            'laite': _('Oletuksena liitetään laitteeseen mistä käyttäjä tuli')
        }