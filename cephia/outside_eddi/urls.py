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
    url(r'^diagnostic_tests/$', views.diagnostic_tests, name='diagnostic_tests'),
    url(r'^manage_studies/$', views.manage_studies, name='manage_studies'),
]
urlpatterns += staticfiles_urlpatterns()
