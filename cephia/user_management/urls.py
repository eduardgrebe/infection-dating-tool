from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns(
    '',

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

)

