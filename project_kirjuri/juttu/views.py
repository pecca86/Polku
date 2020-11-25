from __future__ import unicode_literals
from django.forms import fields
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.utils.http import is_safe_url
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from braces.views import SelectRelatedMixin
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.views.generic.list import ListView, MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from django.views.generic import FormView, View
from django.conf import settings
from django.db.models import Q #for robust searches
import itertools
from itertools import chain
from django.forms import formset_factory
from django.http import JsonResponse


from .models import Juttu, Muistiinpanot, Poikkeamat, Salasanat
from laite.models import Laite, LaiteSijainti, LaiteStatus, OheisLaite, LaiteMuistiinpano, OheislaiteSijainti, LaiteDataStatus
from . import models

from .forms import JuttuForm, MuistiinpanotForm, PoikkeamatForm, SalasanaForm
from laite.forms import LaiteForm, LaiteMuistiinpanoForm, OheisLaiteForm
from laite.views import LaiteDetailView
from django.contrib import messages

# Create your views here.



## JUTUT ##

class CreateJuttu(generic.CreateView):
    ''' Here we create juttus'''
    model = Juttu
    form_class = JuttuForm

    
    #must be in the form of a tuple!
"""     fields = (
        'juttunumero', 'nimike', 
        'tutkinnanjohtaja', 'kohdehenkilo', 
        'tutkija', 'ryhma',
        'toimenpidepyynto', 'salasana',
        'kiireellisyys',
        ) 
         """


#List of all juttus
class ListJuttu(LoginRequiredMixin, generic.ListView):
    """ 
    Displays a list of all juttus.
    """
    #TODO: Implement MultipleObjectMixin if list grows too big
    paginate_by = 500
    model = Juttu
    

    def get_context_data(self, **kwargs):
        '''
        Enables us to get to the juttu using the pk
        '''
        context = super(ListJuttu, self).get_context_data(**kwargs)
        context['laites'] = Laite.objects.all
        context['search_term'] = self.request.GET.get('q')
        #context['laite_status'] = Laite.objects.filter(laite_status__startswith='OD') #we can present the value inside our template by calling just 'laite_status'
        return context


    def get_queryset(self):
        query = self.request.GET.get('q') #q is the input name for our search bar form 
        query2 = ""
        tarkenne = self.request.GET.get('tarkenne')
        #user_zero = Juttu.objects.get(user_id=None)[0:1]
        #if query == None and query2 == "":
        if query == None or query == "":
            #return Juttu.objects.all()
            return Juttu.objects.order_by('-juttu_status_id__aloittamatta_status','-juttu_status_id__aloitettu_status', '-juttu_status_id__odottaa_status', '-kirjauspvm') #-high -> low

        #juttunumeroon perustuva haku
        if tarkenne == "juttunumero":
            object_list = Juttu.objects.filter(
                Q(juttunumero__icontains=query) |
                Q(case_nimi__icontains=query)
            ).order_by('-kirjauspvm') 

            return object_list
        
        if tarkenne == "etu_and_suku":
            query2 = ""

            if len(query.split(" ")) > 1:
                split_query = query.split(" ")
                query = split_query[0]
                query2 = split_query[1]

            object_list = Juttu.objects.filter(
                Q(etunimi__iexact=query) & Q(sukunimi__iexact=query2)
            ).order_by('-kirjauspvm')

            return object_list
        
        if tarkenne == "etu_or_suku":
            query2 = ""

            if len(query.split(" ")) > 1:
                split_query = query.split(" ")
                query = split_query[0]
                query2 = split_query[1]

            object_list = Juttu.objects.filter(
                Q(etunimi__icontains=query) & Q(sukunimi__icontains=query2) |
                Q(etunimi__icontains=query2) & Q(sukunimi__icontains=query)
            ).order_by('-kirjauspvm')

            return object_list
        
        if tarkenne == "it_tutkija":
            query2 = ""

            if len(query.split(" ")) > 1:
                split_query = query.split(" ")
                query = split_query[0]
                query2 = split_query[1] #in case we implement a two word username

            object_list = Juttu.objects.filter(
                Q(user__username__icontains=query)
            ).order_by('-kirjauspvm')

            return object_list

        #iexact is case insensitive, icontains = case-insensitive, unnaccent removes special signs
        if tarkenne == "wildcard":

            if len(query.split(" ")) > 1:
                split_query = query.split(" ")
                query = split_query[0]
                query2 = split_query[1]

            object_list = Juttu.objects.filter( 
                    Q(juttunumero__icontains=query) | 
                    Q(etunimi__icontains=query) | 
                    Q(sukunimi__icontains=query) |
                    Q(etunimi__icontains=query) & Q(sukunimi__icontains=query2) |
                    Q(user__username__icontains=query) & Q(user__username__icontains=query2) |
                    Q(case_nimi__icontains=query)
    
                    #TODO: Filter year by this method?
                ).order_by('-kirjauspvm')
        else:
            object_list = Juttu.objects.order_by('juttu_status_id', '-kirjauspvm') 

        return object_list

#A specific juttu
class SingleJuttu(LoginRequiredMixin, generic.DetailView, ModelFormMixin):
    #model = Juttu #Use this if no queryset is implemented
    #form_class = JuttuForm #this cannot be used with modelformmixin
    fields = ['juttu_status', 'user'] #what fields from the form we want to incorperate inside the view
    #success_url = reverse_lazy('juttu:single_juttu', kwargs={'pk':model.pk})
    #success_url = reverse_lazy('juttu:single_juttu', kwargs={'pk':object}) #unnecessary of method get_success_url is specified
    #queryset = Juttu.objects.all() #not needed if get_queryset method is specified

    #Need to implement this method if we want to performe updates to the db from this view
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'juttu_status' in request.POST:
            form = self.get_form()
        else:
            form = JuttuForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            return self.form_valid(form)
        else:
            raise ValueError(f"INVALID FORM: {type(form)} {form}")


    """ https://stackoverflow.com/questions/35028557/how-to-add-listview-to-generic-detailview-django/35031544 """
    """ https://stackoverflow.com/questions/21758731/how-can-i-get-pk-or-id-in-get-context-data-from-cvb """
    def get_context_data(self, **kwargs):
        '''
        Enables us to get to the juttu using the pk
        '''
        context = super(SingleJuttu, self).get_context_data(**kwargs)
        context['laites'] = Laite.objects.filter(juttu_id=self.object.pk)
        context['mustiinpanot_list'] = Muistiinpanot.objects.filter(juttu_id=self.object.pk)
        context['poikkeamat_list'] = Poikkeamat.objects.filter(juttu_id=self.object.pk)
        return context


    def get_queryset(self):
        """ 
        If model is not specified when using ModelMixin, we need to provide
        the Model using the queryset 
        """
        #laite_data = Laite.objects.get_queryset()
        #juttu_data = Juttu.objects.get_queryset()
        juttu_data = Juttu.objects.all()

        return juttu_data

#FUNCTIONAL AJAX VIEW FOR JUTTU DETAIL
def validate_status(request):
    juttu_status = request.GET.get('juttu_status', None)
    get_juttu_id = request.GET.get('juttu_id', None)
    juttu = Juttu.objects.get(id=get_juttu_id)
    juttu.juttu_status_id = juttu_status
    juttu.save()
    juttu_status_valmis = juttu.juttu_status.valmis_status

    #Check if all laittees has data_value filled:
    check_if_data = True
    laitteet = Laite.objects.filter(juttu_id=get_juttu_id)
    for laite in laitteet:
        if laite.laite_data_status_id is None:
            check_if_data = False

    data = {
        'is_valid': True,
        'new_status_id': juttu_status,
        'juttu_id': get_juttu_id,
        'check_if_data': check_if_data,
        'juttu_status_valmis_status': juttu_status_valmis,
    }
    return JsonResponse(data)


#FUNCTIONAL AJAX VIEW FOR JUTTU DETAIL
def validate_tutkija(request):
    tutkija_id = request.GET.get('user', None)
    juttu_id = request.GET.get('juttu_id', None)
    juttu = Juttu.objects.get(id=juttu_id)
    juttu.user_id = tutkija_id
    juttu.save()

    data = {
        'is_valid': True,
        'msg': tutkija_id,
    }
    return JsonResponse(data)



#Delete a view
class DeleteJuttu(LoginRequiredMixin, generic.DeleteView):
    model = models.Juttu
    #select_related = ('juttunumero', 'juttu')
    success_url = reverse_lazy('juttu:juttu_list')

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Juttu poistettu!")
        return super().delete(*args, **kwargs)


#Update a view, needs proper meta class in forms.py
class UpdateJuttu(LoginRequiredMixin, generic.UpdateView):
    form_class = JuttuForm #binds the update form to an existing form
    #success_url = reverse_lazy('juttu:single_juttu', kwargs={'pk': self.object.id})
    model = Juttu

    def get_success_url(self):
        return reverse('juttu:single_juttu', kwargs={'pk': self.object.id})



## TEST LIST VIEW ##



## END TEST LIST VIEW ##


class JuttuLaiteList(LoginRequiredMixin, generic.CreateView, ModelFormMixin):
    template_name = 'juttu/juttu_laite_list.html'

    model = Laite
    fields = ['laite_status', 'sijainti', 'raporttiin']
    #form_class = LaiteForm
    
    def get_context_data(self, **kwargs):
        context = super(JuttuLaiteList, self).get_context_data(**kwargs)
        juttu_pk = self.kwargs['pk']
        context['laites'] = Laite.objects.filter(juttu_id=juttu_pk)
        context['laite_status'] = LaiteStatus.objects.all()
        context['laite_sijainti'] = LaiteSijainti.objects.all()
        context['laite_data_status'] = LaiteDataStatus.objects.all()
        context['oheislaite_sijainti'] = OheislaiteSijainti.objects.all()
        context['oheislaite_status'] = LaiteStatus.objects.all()
        context['juttu'] = Juttu.objects.filter(id=juttu_pk)[0] #in order for side nav to be rendered correctly
        context['mustiinpanot_list'] = Muistiinpanot.objects.filter(juttu_id=juttu_pk)
        context['laite_muistiinpanot'] = LaiteMuistiinpano.objects.all()
        context['poikkeamat_list'] = Poikkeamat.objects.filter(juttu_id=juttu_pk)
        context['oheislaitteet'] = OheisLaite.objects.all()
        return context
        


    def post(self, request, *args, **kwargs):

        if self.request.POST.get('oheislaite_id'):
            oheislaite_id = self.request.POST.get('oheislaite_id')
            status_id = self.request.POST.get('oheislaite_status')
            sijainti_id = self.request.POST.get('oheislaite_sijainti')
            obj = OheisLaite.objects.get(id=oheislaite_id)
            obj.oheislaite_status = LaiteStatus.objects.get(id=status_id)
            obj.oheislaite_sijainti = OheislaiteSijainti.objects.get(id=sijainti_id)
            obj.save()
            return redirect(request.get_full_path())


        laite_id = self.request.POST.get('laite_id')
        self.object = Laite.objects.get(id=laite_id)
        if 'laite_status' in request.POST:
            form = self.get_form()
        elif 'laite_sijainti' in request.POST:
            form = self.get_form()
        else:
            form = LaiteForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            return self.form_valid(form)
        else:
            raise ValueError(f"INVALID FORM: {type(form)} {form}")

    def form_valid(self, form):
        form.instance.laite_id = self.request.POST.get('laite_id')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path



## MUISTIINPANOT ##

class CreateMuistiinpano(LoginRequiredMixin, generic.CreateView, ModelFormMixin):
    #template_name = 'juttu/juttu_muistiinpanot.html'
    model = Muistiinpanot
    fields = ['muistiinpano', 'it_tutkija', 'raporttiin',]
    #form_class = MuistiinpanotForm

    #No actual need for this function anymore, look at 
    def get_pk_from_url(self):
        '''
        Grabs the pk value from the url field IN THIS INSTANCE of the app
        '''
        url = self.request.path
        url_items_list = url.split('/')
        url_pk = url_items_list[-2]
        url_pk = int(url_pk)
        return url_pk


    def form_valid(self, form):
        form.instance.juttu_id = self.kwargs.get('pk')
        # If no tutkija is chosen, default to logged in tutkija
        if form.instance.it_tutkija_id == None:
            form.instance.it_tutkija_id = self.request.user.id
        #form.instance.it_tutkija_id = self.get('user')
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(Muistiinpanot, username=self.kwargs['it_tutkija'])


    def get_context_data(self, **kwargs):
        '''
        Enables us to get to the juttu using the pk
        '''
        juttu_pk = self.kwargs['pk'] #gets the url pk from the argument list
        context = super(CreateMuistiinpano, self).get_context_data(**kwargs)
        context['laites'] = Laite.objects.filter(juttu_id=juttu_pk)
        context['muistiinpanon_juttu'] = Juttu.objects.filter(pk=juttu_pk)
        context['jutun_muistiinpanot'] = Muistiinpanot.objects.filter(juttu_id=juttu_pk)
        context['mp_poikkeamat'] = Poikkeamat.objects.filter(juttu_id=juttu_pk)
        context['juttu'] = Juttu.objects.filter(id=juttu_pk)[0] #in order for side nav to be rendered correctly
        context['mustiinpanot_list'] = Muistiinpanot.objects.filter(juttu_id=juttu_pk)
        context['poikkeamat_list'] = Poikkeamat.objects.filter(juttu_id=juttu_pk)

        return context

    
class UpdateMuistiinpano(LoginRequiredMixin, generic.UpdateView):
    template_name = 'juttu/muistiinpanot_update.html'
    form_class = MuistiinpanotForm
    model = Muistiinpanot


class DeleteMuistiinpano(LoginRequiredMixin, generic.DeleteView):
    model = Muistiinpanot

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Muistiinpano poistettu!")
        return super().delete(*args, **kwargs)

    def get_success_url(self):
        return reverse('juttu:juttu_muistiinpano', kwargs={'pk': self.object.juttu_id})


## POIKKEAMAT ##

class CreatePoikkeama(LoginRequiredMixin, generic.CreateView, ModelFormMixin):
    model = Poikkeamat
    #fields = ['poikkeama', 'laite', 'it_tutkija', 'raporttiin']
    form_class = PoikkeamatForm

    def form_valid(self, form):
        form.instance.juttu_id = self.kwargs.get('pk') #this puts the views juttu pk into the poikkeama table juttu_id
        form.instance.laite_id = self.request.POST.get('laite_id')
        # If IT-tutkija not chosen from list, default to logged in tutkija
        if form.instance.it_tutkija_id == None:
            form.instance.it_tutkija_id = self.request.user.id
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        '''
        Enables us to get to the juttu using the pk
        '''
        juttu_pk = self.kwargs['pk']
        context = super(CreatePoikkeama, self).get_context_data(**kwargs)
        context['laites'] = Laite.objects.filter(juttu_id=juttu_pk)
        context['poikkeaman_juttu'] = Juttu.objects.filter(pk=juttu_pk)
        context['jutun_poikkeamat'] = Poikkeamat.objects.filter(juttu_id=juttu_pk)
        context['mp_in_poikkeama'] = Muistiinpanot.objects.filter(juttu_id=juttu_pk)
        context['juttu'] = Juttu.objects.filter(id=juttu_pk)[0] #in order for side nav to be rendered correctly
        context['mustiinpanot_list'] = Muistiinpanot.objects.filter(juttu_id=juttu_pk)
        context['poikkeamat_list'] = Poikkeamat.objects.filter(juttu_id=juttu_pk)

        return context


class UpdatePoikkeama(LoginRequiredMixin, generic.UpdateView):
    template_name = 'juttu/poikkeamat_update.html'
    fields = ['poikkeama', 'laite', 'it_tutkija', 'raporttiin']
    #form_class = PoikkeamatForm
    model = Poikkeamat


class DeletePoikkeama(LoginRequiredMixin, generic.DeleteView):
    model = Poikkeamat

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Poikkeama poistettu!")
        return super().delete(*args, **kwargs)

    def get_success_url(self):
        return reverse('juttu:juttu_poikkeamat', kwargs={'pk': self.object.juttu_id})


class PoikkeamatList(ListView):
    paginate_by = 500
    model = Poikkeamat


    def get_context_data(self, **kwargs):
        '''
        Enables us to get to the juttu using the pk
        '''
        context = super(PoikkeamatList, self).get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('qp')

        return context

    def get_queryset(self):
        query = self.request.GET.get('qp') #q is the input name for our search bar form 
        query2 = ""
        if query == None:
            return Poikkeamat.objects.all().order_by('-kirjauspvm') # '-' = descending
        if len(query.split(" ")) > 1:
            split_query = query.split(" ")
            query = split_query[0]
            query2 = split_query[1]

        #iexact is case insensitive, icontains = case-insensitive, unnaccent removes special signs
        poikkeamat = Poikkeamat.objects.filter( 
                Q(juttu__juttunumero__icontains=query) |
                Q(it_tutkija__username__icontains=query) & Q(it_tutkija__username__icontains=query2)
   
            ).order_by('-kirjauspvm')
        return poikkeamat



## YHTEENVETO / RAPORTTI ##

class YhteenvetoView(generic.DetailView):
    model = Juttu
    template_name = 'juttu/yhteenveto.html'

    def get_context_data(self, **kwargs):
        context = super(YhteenvetoView, self).get_context_data(**kwargs)
        context['laites'] = Laite.objects.filter(juttu_id=self.object.pk)
        context['mustiinpanot_list'] = Muistiinpanot.objects.filter(juttu_id=self.object.pk)
        context['poikkeamat_list'] = Poikkeamat.objects.filter(juttu_id=self.object.pk)
        context['laite_muistiinpano'] = LaiteMuistiinpano.objects.all()
        context['oheislaitteet'] = OheisLaite.objects.all()
        return context


class YhteenvetoPrintView(generic.DetailView):
    model = Juttu
    template_name = 'juttu/yhteenveto_print.html'

    def get_context_data(self, **kwargs):
        context = super(YhteenvetoPrintView, self).get_context_data(**kwargs)
        context['laites'] = Laite.objects.filter(juttu_id=self.object.pk)
        context['mustiinpanot_list'] = Muistiinpanot.objects.filter(juttu_id=self.object.pk)
        context['poikkeamat_list'] = Poikkeamat.objects.filter(juttu_id=self.object.pk)
        context['laite_muistiinpano'] = LaiteMuistiinpano.objects.all()
        context['oheislaitteet'] = OheisLaite.objects.all()
        return context


## SALASANAT ##


class CreateSalasana(LoginRequiredMixin, generic.CreateView, ModelFormMixin):
    model = Salasanat
    #fields = ['poikkeama', 'laite', 'it_tutkija', 'raporttiin']
    form_class = SalasanaForm

    def form_valid(self, form):
        form.instance.juttu_id = self.kwargs.get('pk')  #this puts the views juttu pk into the poikkeama table juttu_id
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        '''
        Enables us to get to the juttu using the pk
        '''
        juttu_pk = self.kwargs['pk']
        context = super(CreateSalasana, self).get_context_data(**kwargs)
        context['laites'] = Laite.objects.filter(juttu_id=juttu_pk)
        context['poikkeaman_juttu'] = Juttu.objects.filter(pk=juttu_pk)
        context['mp_in_poikkeama'] = Muistiinpanot.objects.filter(juttu_id=juttu_pk)
        context['jutun_salasanat'] = Salasanat.objects.filter(juttu_id=juttu_pk)
        context["oheislaitteet"] = OheisLaite.objects.all()
        context['juttu'] = Juttu.objects.filter(id=juttu_pk)[0] #in order for side nav to be rendered correctly
        context['mustiinpanot_list'] = Muistiinpanot.objects.filter(juttu_id=juttu_pk)
        context['poikkeamat_list'] = Poikkeamat.objects.filter(juttu_id=juttu_pk)

        return context


class DeleteSalasana(LoginRequiredMixin, generic.DeleteView):
    model = Salasanat

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Salasana poistettu!")
        return super().delete(*args, **kwargs)

    def get_success_url(self):
        return reverse('juttu:jutun_salasanat', kwargs={'pk': self.object.juttu_id})
        

class SalasanaPrint(LoginRequiredMixin, generic.DetailView):
    template_name = 'juttu/salasanat_print.html'
    model = Juttu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["salasanat"] = Salasanat.objects.filter(juttu_id=self.kwargs['pk'])
        context["laitteet"] = Laite.objects.filter(juttu_id=self.kwargs['pk'])
        context["oheislaitteet"] = OheisLaite.objects.all()
        return context
    
        
## FUNCTION VIEWS ##

def test_page(request, pk):
    helpdict = {'help_insert':'HELP PAGE', 'pk':pk}
    
    return render(request,'juttu/yhteenveto.html',context=helpdict)


## TEST VIEWS ##

class ModalTemplate(generic.ListView):
    '''
    For modal testing only!
    '''
    model = Juttu
    template_name = "juttu/content.html"