from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^outside_eddi/home/$', views.home, name='outside_eddi/home'),
    # url(r'^outside_eddi/user_registration/$', views.user_registration, name='outside_eddi/user_registration'),
)
