from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^tms/$', views.table_management, name='table_management'),
    
    url(r'^countries/$', views.countries, name='countries'),
    url(r'^ethnicities/$', views.ethnicities, name='ethnicities'),
    url(r'^specimen_type/$', views.specimen_type, name='specimen_type'),
    url(r'^studies/$', views.studies, name='studies'),
    url(r'^sites/$', views.sites, name='sites'),
    url(r'^subjects/$', views.subjects, name='subjects'),
    url(r'^visits/$', views.visits, name='visits'),
    url(r'^specimen/$', views.specimen, name='specimen'),
    url(r'^file_info/$', views.file_info, name='file_info'),
    url(r'^row_info/(?P<file_id>\d+)/$', views.row_info, name='row_info'),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^download_file/(?P<file_id>\d+)/$', views.download_file, name='download_file'),
    url(r'^process_file/(?P<file_id>\d+)/$', views.process_file, name='process_file'),
    url(r'^parse_file/(?P<file_id>\d+)/$', views.parse_file, name='parse_file'),
    url(r'^validate_rows/(?P<file_id>\d+)/$', views.validate_rows, name='validate_rows'),
    url(r'^delete_file/(?P<file_id>\d+)/$', views.delete_file, name='delete_file'),
    url(r'^export_as_csv/(?P<file_id>\d+)/$', views.export_as_csv, name='export_as_csv'),
    url(r'^download_subjects_no_visits/$', views.download_subjects_no_visits, name='download_subjects_no_visits'),
    url(r'^download_visits_no_subjects/$', views.download_visits_no_subjects, name='download_visits_no_subjects'),
    url(r'^associate_specimen/$', views.associate_specimen, name='associate_specimen'),
    url(r'^comment_on_row/$', views.comment_on_row, name='comment_on_row'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/cephia_login.html'}, name='auth_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='auth_logout'),
    url(r'^accounts/password-change/$', 'django.contrib.auth.views.password_change', name='change_password'),
    url(r'^accounts/password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^accounts/password-reset/$', 'django.contrib.auth.views.password_reset', name='reset_password'),
    url(r'^accounts/password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
