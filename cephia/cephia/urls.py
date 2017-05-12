from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
import views
import reporting
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from infection_dating_tool import views as idt_views

urlpatterns = [
    url(r'^$', idt_views.home, name='home'),
    url(r'^idt/$', idt_views.home),
    
    url(r'^register/$', idt_views.idt_user_registration, name='registration'),
    url(r'^idt/register/$', idt_views.idt_user_registration),
    
    url(r'^register/info/$', idt_views.idt_user_registration_info, name='registration_info'),
    url(r'^idt/register/info/$', idt_views.idt_user_registration_info),
    
    url(r'^login/$', idt_views.idt_login, name='login'),
    url(r'^idt/login/$', idt_views.idt_login),
    
    url(r'^logout/$', idt_views.idt_logout, name='logout'),
    url(r'^idt/logout/$', idt_views.idt_logout),
    
    url(r'^data_files/$', idt_views.data_files, name='data_files'),
    url(r'^idt/data_files/$', idt_views.data_files),
    
    url(r'^help/$', idt_views.help_page, name='help_page'),
    url(r'^idt/help/$', idt_views.help_page),
    
    url(r'^tests/$', idt_views.tests, name='tests'),
    url(r'^idt/tests/$', idt_views.tests),
    
    url(r'^tests/(?P<test_id>\d+)/edit/$', idt_views.edit_test, name='edit_test'),
    url(r'^idt/tests/(?P<test_id>\d+)/edit/$', idt_views.edit_test),
    
    url(r'^tests/create/$', idt_views.create_test, name='create_test'),
    url(r'^idt/tests/create/$', idt_views.create_test),
    
    url(r'^test_mapping/$', idt_views.test_mapping, name='test_mapping'),
    url(r'^idt/test_mapping/$', idt_views.test_mapping),
    
    url(r'^test_mapping/(?P<file_id>\d+)/$', idt_views.test_mapping, name='test_mapping'),
    url(r'^idt/test_mapping/(?P<file_id>\d+)/$', idt_views.test_mapping),
    
    url(r'^test_mapping/create/$', idt_views.create_test_mapping, name='create_test_mapping'),
    url(r'^idt/test_mapping/create/$', idt_views.create_test_mapping),
    
    url(r'^test_mapping/edit/$', idt_views.edit_test_mapping, name='edit_test_mapping'),
    url(r'^idt/test_mapping/edit/$', idt_views.edit_test_mapping),
    
    url(r'^test_mapping/edit/(?P<save_map_id>\d+)/$', idt_views.edit_test_mapping, name='edit_test_mapping_save'),
    url(r'^idt/test_mapping/edit/(?P<save_map_id>\d+)/$', idt_views.edit_test_mapping),
    
    url(r'^data_files/(?P<file_id>\d+)/delete', idt_views.delete_data_file, name='delete_data_file'),
    url(r'^idt/data_files/(?P<file_id>\d+)/delete', idt_views.delete_data_file),
    
    url(r'^data_files/(?P<file_id>\d+)/process_data', idt_views.process_data_file, name='process_data_file'),
    url(r'^idt/data_files/(?P<file_id>\d+)/process_data', idt_views.process_data_file),
    
    url(r'^validate_mapping/(?P<file_id>\d+)/', idt_views.validate_mapping_from_page, name='validate_mapping_from_page'),
    url(r'^idt/validate_mapping/(?P<file_id>\d+)/', idt_views.validate_mapping_from_page),

    url(r'^results/(?P<file_id>\d+)/$', idt_views.results, name='results'),
    url(r'^idt/results/(?P<file_id>\d+)/$', idt_views.results),
    
    url(r'^results/(?P<file_id>\d+)/download/$', idt_views.download_results, name='download_results'),
    url(r'^idt/results/(?P<file_id>\d+)/download/$', idt_views.download_results),
    
    url(r'^user_registration/finalise/(?P<token>.*)/$', idt_views.finalise_user_account, name='finalise_user_account'),
    url(r'^idt/user_registration/finalise/(?P<token>.*)/$', idt_views.finalise_user_account),

    url(r'^tests/set_selected_category/$', idt_views.set_selected_category, name='set_selected_category'),
    url(r'^idt/tests/set_selected_category/$', idt_views.set_selected_category),

    # url(r'^mapping/set_selected_test/$', idt_views.set_selected_category, name='set_selected_test'),
    # url(r'^idt/mapping/set_selected_test/$', idt_views.set_selected_test),
    
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
