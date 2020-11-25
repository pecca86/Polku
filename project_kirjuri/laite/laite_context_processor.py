from .models import Laite

def laite_renderer(request):
    return { 'all_laites': Laite.objects.all()}


def laite_juttu_pk(request):
    return { 'laite_juttu_pk' : request.GET }
    #return { 'laite_juttu_pk' : Laite.objects.filter(juttu_id=request.GET.get('pk'))}