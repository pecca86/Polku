import itertools
from django.http import request
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from juttu.models import Juttu, TutkintaRyhma, Salasanat
from laite.models import Laite, OheisLaite
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count, F
from itertools import chain
from django.db.models import Q
from django.utils.html import format_html_join
from django.template.defaulttags import register
import datetime
from django.db.models.functions import TruncMonth

class TestPage(TemplateView):
    template_name = 'test.html'


class AloitusPage(TemplateView):
    template_name = 'aloitus.html'


class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("test"))
        return super().get(request, *args, **kwargs)


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        year = self.request.GET.get('year')
        if year is None:
            year = self.kwargs['year']

        context = super().get_context_data(**kwargs)

        # RYHMÄN JUTTU LKM / VUOSI
        context['ryhma_juttuja_vuosi'] = Juttu.objects.values('ryhma_id__tutkintaryhma').filter(kirjauspvm__year=year).annotate(ryhma_juttu_lkm=Count('ryhma_id')) #juttuja per tutk.ryhm. / vuosi

        #RYHMÄN JUTTU LKM / KK / VUOSI
        context['ryhma_juttu_kk_vuosi'] = Juttu.objects.values('id').filter(kirjauspvm__year=year).annotate(month=TruncMonth('kirjauspvm')).values('month').annotate(total=Count('ryhma_id'))

        #RYHMÄN LAITEMÄÄRÄ / VUOSI
        context['ryhma_laitemaara_vuosi'] = Laite.objects.values('juttu_id__ryhma_id__tutkintaryhma').filter(kirjauspvm__year=year).annotate(ryhma_laite_lkm=Count('juttu_id'))


        #JUTTUMÄÄRÄ / KK / VUOSI
        context['juttumaara_kk'] = Juttu.objects.values('ryhma_id__tutkintaryhma').filter(kirjauspvm__year=year).annotate(month=TruncMonth('kirjauspvm')).values('month').annotate(total=Count('ryhma_id'))
       
        #KAIKKI JUTUT LKM / VUOSI
        context['kaikki_jutut_lkm_vuosi'] = Juttu.objects.filter(kirjauspvm__year=year).count

        #IT-TUTKIJAN JUTTU LKM / VUOSI
        context['it_tutk_jutut_lkm_vuosi'] = Juttu.objects.values('user_id__username').filter(kirjauspvm__year=year).annotate(it_tutk_juttu_lkm=Count('user_id')) 
        #IT-TUTKIJAN LAITE LKM / VUOSI
        context['it_tutk_laitemaara_vuosi'] = Laite.objects.values('juttu_id__user_id__username').filter(kirjauspvm__year=year).annotate(tutk_laite_lkm=Count('juttu_id'))
        context['it_tutk_oheislaitemaara_vuosi'] = OheisLaite.objects.values('laite_id__juttu_id__user_id__username').filter(kirjauspvm__year=year).annotate(tutk_laite_lkm=Count('laite_id'))


        #LAITTEET LKM & GB / VUOSI
        context['laite_lkm_vuosi'] = Laite.objects.filter(kirjauspvm__year=year).count
        context['laite_gb_lkm_vuosi'] = Laite.objects.values('kapasiteetti').filter(kirjauspvm__year=year).aggregate(summa=Sum('kapasiteetti'))
       
        #OHEISLAITTEET LKM & GB/ VUOSI
        context['oheislaite_lkm_vuosi'] = OheisLaite.objects.filter(kirjauspvm__year=year).count
        context['oheislaite_gb_lkm_vuosi'] = OheisLaite.objects.values('kapasiteetti').filter(kirjauspvm__year=year).aggregate(summa=Sum('kapasiteetti'))

        #LAITEMÄÄRÄ / KK / VUOSI
        context['laitemaara_kk'] = Laite.objects.filter(kirjauspvm__year=year).annotate(month=TruncMonth('kirjauspvm')).values('month').annotate(total=Count('id'))
        context['oheislaitemaara_kk'] = OheisLaite.objects.filter(kirjauspvm__year=year).annotate(month=TruncMonth('kirjauspvm')).values('month').annotate(total=Count('id'))

        #KAIKKI LAITTEET LKM / KK / VUOSI
        

        #GB / KK / VUOSI
        context['laite_gb_kk'] = Laite.objects.filter(kirjauspvm__year=year).annotate(month=TruncMonth('kirjauspvm')).values('month').annotate(total=Sum('kapasiteetti'))
        context['oheislaite_gb_kk'] = OheisLaite.objects.filter(kirjauspvm__year=year).annotate(month=TruncMonth('kirjauspvm')).values('month').annotate(total=Sum('kapasiteetti'))
        
        context['vuosi'] = year
        return context


## FUNCTION BASED VIEW ##

def home(request, year):

    context = {
        'year': year,
        }

    return render(request, 'home.html', context)


def population_chart(request, year):
    labels = []
    data = []

    queryset = Juttu.objects.values('ryhma_id__tutkintaryhma').filter(kirjauspvm__year=year).annotate(ryhma_juttu_lkm=Count('ryhma_id'))
    for entry in queryset:
        labels.append(entry['ryhma_id__tutkintaryhma'])
        data.append(entry['ryhma_juttu_lkm'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })    

## SALASANAT SEARCH VIEW ##

def search_view(request):

    query = request.GET.get('qs')
    query2 = ""

    if query is None:
        query = ""

    if len(query.split(" ")) > 1:
            split_query = query.split(" ")
            query = split_query[0]
            query2 = split_query[1]

    laite_salasanat = Laite.objects.filter(
        Q(juttu__juttunumero__icontains=query) |
        Q(juttu__etunimi__iexact=query) & Q(juttu__sukunimi__iexact=query2) |
        Q(juttu__etunimi__iexact=query2) & Q(juttu__sukunimi__iexact=query)
    )

    juttu_salasanat = Salasanat.objects.filter(
        Q(juttu__juttunumero__icontains=query) |
        Q(juttu__etunimi__iexact=query) & Q(juttu__sukunimi__iexact=query2) |
        Q(juttu__etunimi__iexact=query2) & Q(juttu__sukunimi__iexact=query)
    )
        
    oheislaite_salasanat = OheisLaite.objects.filter(
        Q(laite__juttu__juttunumero__icontains=query) |
        Q(laite__juttu__etunimi__iexact=query) & Q(laite__juttu__sukunimi__iexact=query2) |
        Q(laite__juttu__etunimi__iexact=query2) & Q(laite__juttu__sukunimi__iexact=query)
    ) 
    
    combined = itertools.chain(laite_salasanat, juttu_salasanat, oheislaite_salasanat)

    return render(request, 'results.html', {'object_list': combined})



class SalasanatAll(LoginRequiredMixin, ListView):
    #paginate_by = 500 #apparently not functional when using itertools
    model = Salasanat
    template_name = "salasanat_list.html"

    def get_context_data(self, **kwargs):
        '''
        Enables us to get to the juttu using the pk
        '''
        context = super(SalasanatAll, self).get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('qs')

        return context


    def get_queryset(self):
        query = self.request.GET.get('qs') #q is the input name for our search bar form 
        query2 = ""
        if query == None:
            query = ""
        if len(query.split(" ")) > 1:
            split_query = query.split(" ")
            query = split_query[0]
            query2 = split_query[1]

        #iexact is case insensitive, icontains = case-insensitive, unnaccent removes special signs
        juttu_salasanat = Salasanat.objects.filter( 
                Q(juttu__juttunumero__icontains=query) |
                Q(juttu__etunimi__iexact=query) & Q(juttu__sukunimi__iexact=query2) |
                Q(juttu__etunimi__iexact=query2) & Q(juttu__sukunimi__iexact=query)
   
            )

        laite_salasanat = Laite.objects.filter(
            Q(juttu__juttunumero__icontains=query) |
            Q(juttu__etunimi__iexact=query) & Q(juttu__sukunimi__iexact=query2) |
            Q(juttu__etunimi__iexact=query2) & Q(juttu__sukunimi__iexact=query)
        )

        oheislaite_salasanat = OheisLaite.objects.filter(
            Q(laite__juttu__juttunumero__icontains=query) |
            Q(laite__juttu__etunimi__iexact=query) & Q(laite__juttu__sukunimi__iexact=query2) |
            Q(laite__juttu__etunimi__iexact=query2) & Q(laite__juttu__sukunimi__iexact=query)
        ) 

        
        combined = itertools.chain(laite_salasanat, juttu_salasanat, oheislaite_salasanat)
        
        return combined
    