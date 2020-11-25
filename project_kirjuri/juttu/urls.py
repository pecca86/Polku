''' JUTTU URLS.PY '''
from __future__ import unicode_literals
from django.urls import path
from . import views

app_name = 'juttu'

urlpatterns = [
    path('', views.ListJuttu.as_view(), name="juttu_list"), #JuttuList
    path('uusi_juttu/', views.CreateJuttu.as_view(), name="uusi_juttu"), 
    path('juttu/<int:pk>/', views.SingleJuttu.as_view(), name="single_juttu"), #SingleJuttu
    path('delete/<int:pk>/', views.DeleteJuttu.as_view(), name="delete"), #RemoveJuttu
    path('juttu/<int:pk>/muokkaa', views.UpdateJuttu.as_view(), name="muokkaa_juttu"), #EditJuttu
    path('juttu/<int:pk>/jutun_laitteet', views.JuttuLaiteList.as_view(), name="jutun_laitteet"),
    #path('juttu/<int:pk>/muistiinpanot', views.Muistiinpanot.as_view(), name="jutun_muistiinpanot"),
    path('juttu/muistiinpano/<int:pk>/', views.CreateMuistiinpano.as_view(), name="juttu_muistiinpano"),
    path('juttu/muistiinpano_update/<int:pk>/', views.UpdateMuistiinpano.as_view(), name="juttu_muistiinpano_update"),
    path('juttu/muistiinpano_delete/<int:pk>/' ,views.DeleteMuistiinpano.as_view(), name="juttu_muistiinpano_delete"),
    #path('juttu/function_pano/<int:pk>/', views.muistiinpano_function, name="pano_func"),
    path('juttu/poikkeamat/<int:pk>/', views.CreatePoikkeama.as_view(), name="juttu_poikkeamat"),
    path('juttu/poikkeamat_update/<int:pk>/', views.UpdatePoikkeama.as_view(), name="juttu_poikkeamat_update"),
    path('juttu/poikkeamat_delete/<int:pk>/', views.DeletePoikkeama.as_view(), name="juttu_poikkeamat_delete"),
    path('poikkeamat/kaikki/', views.PoikkeamatList.as_view(), name="poikkeamat_list"),
    path('juttu/yhteenveto/<int:pk>/', views.YhteenvetoView.as_view(), name="jutun_yhteenveto"),
    path('juttu/yhteenveto_print/<int:pk>', views.YhteenvetoPrintView.as_view(), name="yhteenveto_print"),
    path('juttu/jutun_salasanat/<int:pk>/', views.CreateSalasana.as_view(), name="jutun_salasanat"),
    path('juttu/salasana_delete/<int:pk>/', views.DeleteSalasana.as_view(), name="delete_salasana"),
    path('juttu/salasana_print/<int:pk>/', views.SalasanaPrint.as_view(), name="salasanat_print"),

    path('juttu/validate_status/', views.validate_status, name="validate_status"),
    path('juttu/validate_tutkija/', views.validate_tutkija, name="validate_tutkija"),
]