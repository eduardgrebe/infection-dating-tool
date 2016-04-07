from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    url(r'^eddi_report/', views.eddi_report, name='eddi_report'),
    url(r'^recalculate_eddi/', views.recalculate_eddi, name='recalculate_eddi'),
    url(r'^subject_test_timeline/(?P<subject_id>\d+)/$', views.subject_test_timeline, name='subject_test_timeline'),
    url(r'^subject_timeline_data/(?P<subject_id>\d+)/$', views.subject_timeline_data, name='subject_timeline_data'),
    url(r'^eddi_report_detail/(?P<subject_id>\d+)/$', views.eddi_report_detail, name='eddi_report_detail'),
]
