from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='outside_eddi/home'),
    url(r'^register/$', views.outside_eddi_user_registration, name='outside_eddi/user_registration'),
    url(r'^login/$', views.outside_eddi_login, name='outside_eddi/login'),
    url(r'^logout/$', views.outside_eddi_logout, name='outside_eddi/logout'),
)
