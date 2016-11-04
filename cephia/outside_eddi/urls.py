from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.outside_eddi_user_registration, name='registration'),
    url(r'^login/$', views.outside_eddi_login, name='login'),
    url(r'^logout/$', views.outside_eddi_logout, name='logout'),
    url(r'^data_files/$', views.data_files, name='data_files'),
    url(r'^tests/$', views.tests, name='tests'),
    
    url(r'^test_mapping/$', views.test_mapping, name='test_mapping'),
    url(r'^test_mapping/create/$', views.create_test_mapping, name='create_test_mapping'),
    url(r'^test_mapping/(?P<map_id>\d+)/edit/$', views.edit_test_mapping, name='edit_test_mapping'),
    url(r'^test_mapping/(?P<map_id>\d+)/(?P<test_id>\d+)/edit/$', views.edit_test_mapping, name='edit_test_mapping'),
    url(r'^test_mapping/(?P<file_id>\d+)/$', views.test_mapping, name='test_mapping'),

    url(r'^test_properties/(?P<test_id>\d+)/test/$', views.test_properties, name='test_properties_test'),
    url(r'^test_properties/(?P<map_id>\d+)/(?P<file_id>\d+)/mapping/$', views.test_properties, name='test_properties_mapping'),
    url(r'^test_properties/(?P<map_id>\d+)/mapping/$', views.test_properties, name='test_properties_mapping'),
    
    url(r'^create_study/$', views.edit_study, name='create_study'),
    url(r'^edit_study/(?P<study_id>\d+)/$', views.edit_study, name='edit_study'),
    
    url('^data_files/(?P<file_id>\d+)/delete', views.delete_data_file, name='delete_data_file'),
    url('^data_files/(?P<file_id>\d+)/save_data', views.save_data_file, name='save_data_file'),
    url('^data_files/(?P<file_id>\d+)/process_data', views.process_data_file, name='process_data_file'),

    url(r'^results/(?P<file_id>\d+)/$', views.results, name='results'),

]
urlpatterns += staticfiles_urlpatterns()
