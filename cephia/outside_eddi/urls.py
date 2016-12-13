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
    url(r'^register/info/$', views.outside_eddi_user_registration_info, name='registration_info'),
    url(r'^login/$', views.outside_eddi_login, name='login'),
    url(r'^logout/$', views.outside_eddi_logout, name='logout'),
    
    url(r'^data_files/$', views.data_files, name='data_files'),
    url(r'^help/$', views.help_page, name='help_page'),
    
    url(r'^tests/$', views.tests, name='tests'),
    url(r'^tests/(?P<test_id>\d+)/edit/$', views.edit_test, name='edit_test'),
    url(r'^tests/create/$', views.create_test, name='create_test'),
    
    url(r'^test_mapping/$', views.test_mapping, name='test_mapping'),
    url(r'^test_mapping/create/$', views.create_test_mapping, name='create_test_mapping'),
    url(r'^test_mapping/create/(?P<test_id>\d+)/$', views.create_test_mapping, name='create_test_mapping'),
    url(r'^test_mapping/create/(?P<test_id>\d+)/$', views.create_test_mapping, name='create_test_mapping_properties'),
    url(r'^test_mapping/create/([?P<map_code>\w ]+)/(?P<test_id>\d+)/$', views.create_test_mapping, name='create_test_mapping_properties'),
    
    url(r'^test_mapping/(?P<map_id>\d+)/edit/$', views.edit_test_mapping, {'is_file': False}, name='edit_test_mapping'),
    url(r'^test_mapping/(?P<map_id>\d+)/edit/file/$', views.edit_test_mapping, {'is_file': True}, name='edit_test_mapping_file'),
    
    url(r'^test_mapping/(?P<map_id>\d+)/(?P<test_id>\d+)/edit/$', views.edit_test_mapping, {'is_file': False}, name='edit_test_mapping'),
    url(r'^test_mapping/(?P<map_id>\d+)/(?P<test_id>\d+)/edit/file/$', views.edit_test_mapping, {'is_file': True}, name='edit_test_mapping_file'),
    
    url(r'^test_mapping/(?P<map_id>\d+)/(?P<test_id>\d+)/edit/file/properties/$', views.edit_test_mapping_file_properties, {'is_file': False}, name='edit_test_mapping_properties'),
    url(r'^test_mapping/(?P<map_id>\d+)/(?P<test_id>\d+)/edit/properties/$', views.edit_test_mapping_properties, {'is_file': True}, name='edit_test_mapping_file_properties'),
    
    
    url(r'^test_mapping/(?P<file_id>\d+)/$', views.test_mapping, name='test_mapping'),
    
    url(r'^create_study/$', views.edit_study, name='create_study'),
    url(r'^edit_study/(?P<study_id>\d+)/$', views.edit_study, name='edit_study'),
    
    url('^data_files/(?P<file_id>\d+)/delete', views.delete_data_file, name='delete_data_file'),
    url('^data_files/(?P<file_id>\d+)/process_data', views.process_data_file, name='process_data_file'),
    
    url('^validate_mapping/(?P<file_id>\d+)/', views.validate_mapping_from_page, name='validate_mapping_from_page'),

    url(r'^results/(?P<file_id>\d+)/$', views.results, name='results'),
    url(r'^results/(?P<file_id>\d+)/download/$', views.download_results, name='download_results'),

    url(r'^user_registration/finalise/(?P<token>.*)/$', views.finalise_user_account, name='finalise_user_account'),

]
urlpatterns += staticfiles_urlpatterns()
