''' LAITE URLS.PY '''
from django.urls import path
from . import views
from juttu import views as juttuview

app_name = 'laite'

#TODO: Muokkaa view
urlpatterns = [
    path('', views.LaiteListView.as_view(), name="laite_list" ),
    path('uusi_laite_with_pk/<int:pk>/', views.CreateLaiteView_with_pk.as_view(), name="uusi_laite_pk"), 
    path('laite/<int:pk>', views.LaiteDetailView.as_view(), name="single_laite"), 
    path('delete/<int:pk>', views.DeleteLaiteView.as_view(), name='delete'),
    path('delete_oheislaite/<int:pk>', views.DeleteOheislaiteView.as_view(), name="delete_oheislaite"),
    path('laite/<int:pk>/muokkaa', views.UpdateLaiteView.as_view(), name="muokkaa_laite"),
    path('laite/uusi_oheislaite/<int:pk>/', views.CreateOheisLaiteWithPk.as_view(), name="uusi_oheislaite"),
    path('oheislaite/<int:pk>/muokkaa/', views.UpdateOheisLaiteView.as_view(), name="muokkaa_oheislaite"),
    path('laite/uusi_muistiinpano/<int:pk>/', views.CreateLaiteMuistiinpano.as_view(), name='uusi_laite_mp'),
    path('laite/update_muistiinpano/<int:pk>', views.UpdateLaiteMuistiinpano.as_view(), name='update_muistiinpano'),

    path('laite/validate_oheislaite_status', views.validate_oheislaitestatus, name='validate_oheislaite_status'),
    path('laite/validate_oheislaite_sijainti', views.validate_oheislaitesijainti, name='validate_oheislaite_sijainti'),
    path('laite/validate_laite_status/', views.validate_laitestatus, name="validate_laitestatus"),
    path('laite/validate_laite_sijainti/', views.validate_laitesijainti, name="validate_laitesijainti"),
    path('laite/validate_laiteraporttiin/', views.validate_laiteraporttiin, name="validate_laiteraporttiin"),
    path('laite/validate_oheislaiteraporttiin', views.validate_oheislaiteraporttiin, name="validate_oheislaiteraporttiin"),
    path('laite/validate_laite_data_status/', views.validate_laite_data_status, name="validate_laite_data_status"),

]