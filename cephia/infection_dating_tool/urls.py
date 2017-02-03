from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

app_name = 'infection_dating_tool'
urlpatterns = [
    url(r'^idt/$', views.home, name='home'),
    url(r'^idt/register/$', views.idt_user_registration, name='registration'),
    url(r'^idt/register/info/$', views.idt_user_registration_info, name='registration_info'),
    url(r'^idt/login/$', views.idt_login, name='login'),
    url(r'^idt/logout/$', views.idt_logout, name='logout'),
    
    url(r'^idt/data_files/$', views.data_files, name='data_files'),
    url(r'^idt/help/$', views.help_page, name='help_page'),
    
    url(r'^idt/tests/$', views.tests, name='tests'),
    url(r'^idt/tests/(?P<test_id>\d+)/edit/$', views.edit_test, name='edit_test'),
    url(r'^idt/tests/create/$', views.create_test, name='create_test'),
    
    url(r'^idt/test_mapping/$', views.test_mapping, name='test_mapping'),
    url(r'^idt/test_mapping/create/$', views.create_test_mapping, name='create_test_mapping'),
    url(r'^idt/test_mapping/create/(?P<test_id>\d+)/$', views.create_test_mapping, name='create_test_mapping'),
    url(r'^idt/test_mapping/create/(?P<test_id>\d+)/$', views.create_test_mapping, name='create_test_mapping_properties'),
    url(r'^idt/test_mapping/create/([?P<map_code>\w ]+)/(?P<test_id>\d+)/$', views.create_test_mapping, name='create_test_mapping_properties'),
    
    url(r'^idt/test_mapping/(?P<map_id>\d+)/edit/$', views.edit_test_mapping, {'is_file': False}, name='edit_test_mapping'),
    url(r'^idt/test_mapping/(?P<map_id>\d+)/edit/file/$', views.edit_test_mapping, {'is_file': True}, name='edit_test_mapping_file'),
    
    url(r'^idt/test_mapping/(?P<map_id>\d+)/(?P<test_id>\d+)/edit/$', views.edit_test_mapping, {'is_file': False}, name='edit_test_mapping'),
    url(r'^idt/test_mapping/(?P<map_id>\d+)/(?P<test_id>\d+)/edit/file/$', views.edit_test_mapping, {'is_file': True}, name='edit_test_mapping_file'),
    
    url(r'^idt/test_mapping/(?P<map_id>\d+)/(?P<test_id>\d+)/edit/file/properties/$', views.edit_test_mapping_file_properties, {'is_file': False}, name='edit_test_mapping_properties'),
    url(r'^idt/test_mapping/(?P<map_id>\d+)/(?P<test_id>\d+)/edit/properties/$', views.edit_test_mapping_properties, {'is_file': True}, name='edit_test_mapping_file_properties'),
    
    
    url(r'^idt/test_mapping/(?P<file_id>\d+)/$', views.test_mapping, name='test_mapping'),
    
    url('^idt/data_files/(?P<file_id>\d+)/delete', views.delete_data_file, name='delete_data_file'),
    url('^idt/data_files/(?P<file_id>\d+)/process_data', views.process_data_file, name='process_data_file'),
    
    url('^idt/validate_mapping/(?P<file_id>\d+)/', views.validate_mapping_from_page, name='validate_mapping_from_page'),

    url(r'^idt/results/(?P<file_id>\d+)/$', views.results, name='results'),
    url(r'^idt/results/(?P<file_id>\d+)/download/$', views.download_results, name='download_results'),

    url(r'^idt/user_registration/finalise/(?P<token>.*)/$', views.finalise_user_account, name='finalise_user_account'),
    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),

]
urlpatterns += staticfiles_urlpatterns()
