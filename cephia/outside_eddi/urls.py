from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.outside_eddi_user_registration, name='registration'),
    url(r'^login/$', views.outside_eddi_login, name='login'),
    url(r'^logout/$', views.outside_eddi_logout, name='logout'),
    url(r'^diagnostic_tests/$', views.diagnostic_tests, name='diagnostic_tests'),
)
