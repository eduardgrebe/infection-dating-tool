from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns(
    '',
    url(r'^panels/$', views.panels, name='panels'),
    url(r'^panel_file_upload/(?P<panel_id>\d+)/$', views.panel_file_upload, name='panel_file_upload'),
    url(r'^panel_file_upload/$', views.panel_file_upload, name='panel_file_upload'),
    url(r'^result_file_upload/(?P<panel_id>\d+)/$', views.result_file_upload, name='result_file_upload'),
)

