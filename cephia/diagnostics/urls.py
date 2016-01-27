from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    url(r'^eddi_report/', views.eddi_report, name='eddi_report'),
    url(r'^eddi_report_detail/(?P<subject_id>\d+)/$', views.eddi_report_detail, name='eddi_report_detail'),
]
