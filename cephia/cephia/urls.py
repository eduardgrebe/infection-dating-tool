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
    # url(r'^robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    # url(r'^$', views.home, name='home'),
    # url(r'^tms/$', views.table_management, name='table_management'),

    # url(r'^reports/', include('reporting.urls', namespace='reporting')),
    # url(r'^accounts/', include('user_management.urls', namespace='users')),
    # url(r'^assay/', include('assay.urls', namespace='assay')),
    # url(r'^diagnostics/', include('diagnostics.urls', namespace='diagnostics')),
    
    # url(r'^countries/$', views.countries, name='countries'),
    # url(r'^ethnicities/$', views.ethnicities, name='ethnicities'),
    # url(r'^specimen_type/$', views.specimen_type, name='specimen_type'),
    # url(r'^studies/$', views.studies, name='studies'),
    # url(r'^labs/$', views.labs, name='labs'),
    # url(r'^subjects/$', views.subjects, name='subjects'),
    # url(r'^visits/(?P<visit_id>\d+)/$', views.visits, name='visits'),
    # url(r'^visits/$', views.visits, name='visits'),
    # url(r'^visits/export$', views.visit_export, name='visit_export'),
    # url(r'^specimen/$', views.specimen, name='specimen'),
    # url(r'^preview_specimen_download/$', views.preview_specimen_download, name='preview_specimen_download'),
    # url(r'^file_info/$', views.file_info, name='file_info'),
    # url(r'^row_info/(?P<file_id>\d+)/$', views.row_info, name='row_info'),
    # url(r'^upload_file/$', views.upload_file, name='upload_file'),
    # url(r'^upload_file_priority/$', views.upload_file, name='upload_file_priority'),
    # url(r'^download_file/(?P<file_id>\d+)/$', views.download_file, name='download_file'),
    # url(r'^process_file/(?P<file_id>\d+)/$', views.process_file, name='process_file'),
    # url(r'^parse_file/(?P<file_id>\d+)/$', views.parse_file, name='parse_file'),
    # url(r'^validate_rows/(?P<file_id>\d+)/$', views.validate_rows, name='validate_rows'),
    # url(r'^delete_file/(?P<file_id>\d+)/$', views.delete_file, name='delete_file'),
    # url(r'^export_as_csv/(?P<file_id>\d+)/$', views.export_as_csv, name='export_as_csv'),
    # url(r'^download_subjects_no_visits/$', views.download_subjects_no_visits, name='download_subjects_no_visits'),
    # url(r'^download_visits_no_subjects/$', views.download_visits_no_subjects, name='download_visits_no_subjects'),
    # url(r'^export_file_data/(?P<file_id>\d+)/(?P<state>\w+)/$', views.export_file_data, name='export_file_data'),
    # url(r'^associate_specimen/$', views.associate_specimen, name='associate_specimen'),
    # url(r'^associate_specimen/(?P<subject_id>\d+)$', views.associate_specimen, name='associate_specimen_subject'),
    # url(r'^row_comment/(?P<file_type>\w+)/(?P<file_id>\d+)/(?P<row_id>\d+)$', views.row_comment, name='row_comment'),
    # url(r'^row_comment/$', views.row_comment, name='row_comment'),
    # url(r'^release_notes/$', views.release_notes, name='release_notes'),
    # url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),

    # To be moved, keeping here for now to make url resolution easier.
    # url(r'^', include('infection_dating_tool.urls', namespace='idt')),

    url(r'^idt/$', idt_views.home, name='home'),
    url(r'^idt/register/$', idt_views.idt_user_registration, name='registration'),
    url(r'^idt/register/info/$', idt_views.idt_user_registration_info, name='registration_info'),
    url(r'^idt/login/$', idt_views.idt_login, name='login'),
    url(r'^idt/logout/$', idt_views.idt_logout, name='logout'),
    
    url(r'^idt/data_files/$', idt_views.data_files, name='data_files'),
    url(r'^idt/help/$', idt_views.help_page, name='help_page'),
    
    url(r'^idt/tests/$', idt_views.tests, name='tests'),
    url(r'^idt/tests/(?P<test_id>\d+)/edit/$', idt_views.edit_test, name='edit_test'),
    url(r'^idt/tests/create/$', idt_views.create_test, name='create_test'),
    
    url(r'^idt/test_mapping/$', idt_views.test_mapping, name='test_mapping'),
    url(r'^idt/test_mapping/(?P<file_id>\d+)/$', idt_views.test_mapping, name='test_mapping'),
    url(r'^idt/test_mapping/create/$', idt_views.create_test_mapping, name='create_test_mapping'),
    url(r'^idt/test_mapping/edit/$', idt_views.edit_test_mapping, name='edit_test_mapping'),
    url(r'^idt/test_mapping/edit/(?P<save_map_id>\d+)/$', idt_views.edit_test_mapping, name='edit_test_mapping_save'),
    
    url(r'^idt/data_files/(?P<file_id>\d+)/delete', idt_views.delete_data_file, name='delete_data_file'),
    url(r'^idt/data_files/(?P<file_id>\d+)/process_data', idt_views.process_data_file, name='process_data_file'),
    
    url(r'^idt/validate_mapping/(?P<file_id>\d+)/', idt_views.validate_mapping_from_page, name='validate_mapping_from_page'),

    url(r'^idt/results/(?P<file_id>\d+)/$', idt_views.results, name='results'),
    url(r'^idt/results/(?P<file_id>\d+)/download/$', idt_views.download_results, name='download_results'),

    url(r'^idt/user_registration/finalise/(?P<token>.*)/$', idt_views.finalise_user_account, name='finalise_user_account'),
    
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
