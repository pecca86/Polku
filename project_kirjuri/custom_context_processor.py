import datetime

def year_renderer(request):
    return {
       'this_year': datetime.datetime.today().year,
    }