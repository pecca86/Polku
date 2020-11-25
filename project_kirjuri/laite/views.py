'''LAITE VIEW'''

from django.conf import settings
from django.db.models import fields
from django.forms.forms import Form
from django.utils.http import is_safe_url
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from .models import Laite, OheisLaite, LaiteMuistiinpano
from .models import Juttu, LaiteDataStatus
from .forms import LaiteForm, OheisLaiteForm, LaiteMuistiinpanoForm
from django.contrib import messages
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth import get_user_model #gets current logged in user
User = get_user_model()
from django.db.models import Q #for robust searches
from django.http import JsonResponse
from datetime import datetime, timedelta

# Create your views here.

## LAITE ##

class LaiteListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 500
    model = models.Laite
    #template_name = 
    select_related = ('juttu', 'laite_note',)

    def get_context_data(self, **kwargs):
        '''
        Enables us to get to the juttu using the pk
        '''
        context = super(LaiteListView, self).get_context_data(**kwargs)
        context['laite_muistiinpanot'] = LaiteMuistiinpano.objects.all()
        context['search_term'] = self.request.GET.get('ql')
        return context

    def get_queryset(self):
        query = self.request.GET.get('ql') #q is the input name for our search bar form 
        query2 = ""
        query3 = ""
        laite_data = self.request.GET.get('laite_data')

        if laite_data:
            nelja_kk = datetime.today() - timedelta(days=120)
            return Laite.objects.filter(laite_data_status_id__datatyyppi_sailytyksessa=True).order_by('-kirjauspvm')

        if query == None:
            return Laite.objects.all().order_by('-kirjauspvm')
        if len(query.split(" ")) > 1:
            split_query = query.split(" ")
            query = split_query[0]
            query2 = split_query[1]


        #iexact is case insensitive, icontains = case-insensitive, unnaccent removes special signs
        laite_list = Laite.objects.filter( 
                Q(juttu__juttunumero__icontains=query) | 
                Q(IMEI__icontains=query) | 
                Q(sinettipussi_id__icontains=query) |
                Q(kayttojarjestelma__iexact=query) |
                Q(chipset__icontains=query) |
                Q(juttu__etunimi__iexact=query) & Q(juttu__sukunimi__iexact=query2) |
                Q(juttu__etunimi__iexact=query2) & Q(juttu__sukunimi__iexact=query) |
                Q(kayttojarjestelma__icontains=query) & Q(kayttojarjestelma__icontains=query2) |
                (Q(valmistaja__icontains=query) & Q(malli__icontains=query2)) |
                Q(malli__icontains=query) & Q(malli__icontains=query2) 
                #TODO: Implement search term 'physical + nokia lumia 900' etc
                
   
                #TODO: Filter year by this method?
            ).order_by('-kirjauspvm')
        return laite_list

        

class LaiteDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Laite
    select_related = ('juttu',)

    
    def get_context_data(self, **kwargs):
        context = super(LaiteDetailView, self).get_context_data(**kwargs)
        context['muistiinpanot'] = LaiteMuistiinpano.objects.filter(laite_id=self.object.pk)
        context['oheislaitteet'] = OheisLaite.objects.filter(laite_id=self.object.pk)
        context['laite_data_status'] = LaiteDataStatus.objects.all()
        return context
    


#This view automatically assigns the device to the case we came from
class CreateLaiteView_with_pk(LoginRequiredMixin, generic.CreateView):
    #editable fields
    fields = [
        'valmistaja',
        'malli',
        'laite_tyyppi',
        'kapasiteetti',
        'IMEI',
        'IMEI2',
        'IMEI3',
        'sarjanumero',
        'kayttojarjestelma',
        'chipset',
        'laite_suojakoodi',
        'pakkokeinonro',
        'esinenro',
        'sinettipussi_id',
        'lisatietoja',
        'laite_status',
        'sijainti',
        'raporttiin',
        'laite_data_status',
        ]
    #form_class = LaiteForm
    model = models.Laite

    def form_valid(self, form):
        #Testing updating status from laite listview
        if self.request.POST.get('status'):
            form.instance.laite_status = self.request.POST.get('status')

        form.instance.juttu_id = self.kwargs.get('pk') #sets the foreign key juttu_id to the pk of the case we came from
        return super().form_valid(form)


class DeleteLaiteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Laite
    select_related = ('juttu')
    #success_url = reverse_lazy('juttu:juttu_list') #TODO: Reverse to a better view
    #success_url = reverse_lazy('laite:laite_list') #TODO: Reverse to a better view

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Laite poistettu!")
        return super().delete(*args, **kwargs)

    def get_success_url(self):
      # if you are passing 'pk' from 'urls' to 'DeleteView' for company
      # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
      mymodel = Laite
      laiteid=self.kwargs['pk'] #gets the id of the laite
      field_value = mymodel.objects.get(id=laiteid).juttu_id #last specifies what field's value we want to capture

      return reverse_lazy("juttu:jutun_laitteet", kwargs={'pk': field_value})


class UpdateLaiteView(LoginRequiredMixin, generic.UpdateView):
    #form_class = LaiteForm
    fields = [
        'juttu',
        'valmistaja',
        'malli',
        'laite_tyyppi',
        'kapasiteetti',
        'IMEI',
        'IMEI2',
        'IMEI3',
        'sarjanumero',
        'kayttojarjestelma',
        'chipset',
        'laite_suojakoodi',
        'pakkokeinonro',
        'esinenro',
        'sinettipussi_id',
        'lisatietoja',
        'laite_status',
        'sijainti',
        'raporttiin',
        'laite_data_status',
        ]
    model = models.Laite
    #success_url = reverse_lazy("laite:single_j", kwargs={"pk":"11"})

    #in case we want case we want to alter the succes url
    #def get_success_url(self):
      # if you are passing 'pk' from 'urls' to 'DeleteView' for company
      # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
      #mymodel = Laite
      #laiteid=self.kwargs['pk'] #gets the id of the laite
      #field_value = mymodel.objects.get(id=laiteid).juttu_id #last specifies what field's value we want to capture

      #return reverse_lazy("laite:single_j", kwargs={'pk': field_value})


#FUNCTIONAL AJAX VIEW FOR LAITESTATUS IN JUTTU LAITE LISTs
def validate_laitestatus(request):
    laite_status = request.GET.get('laite_status', None)
    laite_id = request.GET.get('laite_id', None)
    laite = Laite.objects.get(id=laite_id)
    laite.laite_status_id = laite_status
    laite.save()
    data = {
        'is_valid': True,
        'new_status_id': "PILLU",
        'laite_id': laite_id,
    }
    return JsonResponse(data)


#FUNCTIONAL AJAX VIEW FOR LAITESIJAINTI IN JUTTU LAITE LISTs
def validate_laitesijainti(request):
    print(request.GET.get('laite_sijainti', None))
    laite_sijainti = request.GET.get('laite_sijainti', None)
    laite_id = request.GET.get('laite_id', None)
    laite = Laite.objects.get(id=laite_id)
    laite.sijainti_id = laite_sijainti
    laite.save()
    data = {
        'is_valid': True,
        'new_sijainti_id': laite_sijainti,
        'laite_id': laite_id,
    }
    return JsonResponse(data)


#FUNCTIONAL AJAX VIEW FOR LAITE RAPORTTIIN IN JUTTU LAITE LISTs
def validate_laiteraporttiin(request):
    laite_raporttiin = request.GET.get('raportti_status', None)
    print(laite_raporttiin)
    laite_id = request.GET.get('laite_id', None)
    laite = Laite.objects.get(id=laite_id)
    if laite.raporttiin:
        laite.raporttiin = 0
        laite_raporttiin = 0
    else:
        laite.raporttiin = 1
        laite_raporttiin = 1
        
    laite.save()
    data = {
        'is_valid': True,
        'new_raporttiin_id': laite_raporttiin,
        'laite_id': laite_id,
    }
    return JsonResponse(data)


#FUNCTIONAL AJAX VIEW FOR LAITE HÄVITETTY IN JUTTU LAITE LISTs
def validate_laite_data_status(request):
    laite_data_status = int(request.GET.get('laite_data_status', None))
    laite_id = request.GET.get('laite_id', None)
    laite = Laite.objects.get(id=laite_id)
    laite.laite_data_status_id = laite_data_status
    laite.save()
    data = {
        'is_valid': True,
        'new_laite_data_status_id': laite_data_status,
        'laite_id': laite_id,
    }
    return JsonResponse(data)


## OHEISLAITE ##

#For creating an Oheislaite to the laite
class CreateOheisLaiteWithPk(LoginRequiredMixin, generic.CreateView):

    model = models.OheisLaite

    fields = [
        "valmistaja",
        "malli",
        "oheislaite_tyyppi",
        "oheislaite_status",
        "oheislaite_sijainti",
        "sarjanumero",
        "oheislaite_suojakoodi",
        "ICCID",
        "IMSI",
        "kapasiteetti",
        "raporttiin",
    ]
    

    def form_valid(self,form):
        form.instance.laite_id = self.kwargs.get('pk')
        return super().form_valid(form)



class DeleteOheislaiteView(LoginRequiredMixin, generic.DeleteView):
    model = OheisLaite
    select_related = ('laite')

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Oheislaite poistettu")
        return super().delete(*args, **kwargs)

    def get_success_url(self):
        oheislaite_id = self.kwargs['pk']
        laite_value = OheisLaite.objects.get(id=oheislaite_id).laite_id
        return_value_pk = Laite.objects.get(id=laite_value).juttu_id 
        return reverse_lazy("juttu:jutun_laitteet", kwargs={'pk': return_value_pk})


class UpdateOheisLaiteView(LoginRequiredMixin, generic.UpdateView):
    form_class = OheisLaiteForm
    model = OheisLaite


#FUNCTIONAL AJAX VIEW FOR OHEISLAITE IN JUTTU LAITE LISTs
def validate_oheislaitestatus(request):
    oheislaite_status = request.GET.get('oheislaite_status', None)
    oheislaite_id = request.GET.get('oheislaite_id', None)
    oheislaite = OheisLaite.objects.get(id=oheislaite_id)
    oheislaite.oheislaite_status_id = oheislaite_status
    oheislaite.save()
    data = {
        'is_valid': True,
        'new_status_id': oheislaite_status,
        'oheislaite_id': oheislaite_id,
    }
    return JsonResponse(data)


#FUNCTIONAL AJAX VIEW FOR OHEISLAITE IN JUTTU LAITE LISTs
def validate_oheislaitesijainti(request):
    oheislaite_sijainti = request.GET.get('oheislaite_sijainti', None)
    oheislaite_id = request.GET.get('oheislaite_id', None)
    oheislaite = OheisLaite.objects.get(id=oheislaite_id)
    oheislaite.oheislaite_sijainti_id = oheislaite_sijainti
    oheislaite.save()
    data = {
        'is_valid': True,
    }
    return JsonResponse(data)


#FUNCTIONAL AJAX VIEW FOR OHEISLAITE RAPORTTIIN IN JUTTU LAITE LISTs
def validate_oheislaiteraporttiin(request):
    print("Rap.stat.: " + request.GET.get('raportti_status', None))
    print(type(request.GET.get('raportti_status', None)))
    oheislaite_raporttiin = int(request.GET.get('raportti_status', None))
    oheislaite_id = request.GET.get('oheislaite_id', None)
    oheislaite = OheisLaite.objects.get(id=oheislaite_id)
    if oheislaite.raporttiin:
        oheislaite.raporttiin = 0
    else:
        oheislaite.raporttiin = 1
    oheislaite.save()
    data = {
        'is_valid': True,
        'new_oh_raporttiin_id': oheislaite_raporttiin,
        'oheislaite_id': oheislaite_id,
    }
    return JsonResponse(data)


## LAITE MUISTIINPANOT ##

class CreateLaiteMuistiinpano(LoginRequiredMixin, generic.CreateView):
    model = LaiteMuistiinpano
    form_class = LaiteMuistiinpanoForm

    def form_valid(self,form):
        form.instance.laite_id = self.kwargs.get('pk')
        return super().form_valid(form)


class UpdateLaiteMuistiinpano(LoginRequiredMixin, generic.UpdateView):
    form_class = LaiteMuistiinpanoForm
    model = LaiteMuistiinpano

    def get_context_data(self, **kwargs):
        '''
        Enables us to get to the juttu using the pk
        '''
        context = super(UpdateLaiteMuistiinpano, self).get_context_data(**kwargs)
        context['laites'] = Laite.objects.filter(id=self.object.laite_id)
        return context