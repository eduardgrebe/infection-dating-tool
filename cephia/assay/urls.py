from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns(
    '',
    url(r'^panels/$', views.panels, name='panels'),
    url(r'^assay_runs/$', views.assay_runs, name='assay_runs'),
    url(r'^preview_assay_runs/$', views.preview_assay_runs, name='preview_assay_runs'),
    url(r'^run_results/(?P<run_id>\d+)$', views.run_results, name='run_results'),
    url(r'^purge_run/(?P<run_id>\d+)$', views.purge_run, name='purge_run'),
    url(r'^specific_results/(?P<result_id>\d+)$', views.specific_results, name='specific_results'),
    url(r'^membership_file_upload/(?P<panel_id>\d+)/$', views.membership_file_upload, name='membership_file_upload'),
    url(r'^shipment_file_upload/(?P<panel_id>\d+)/$', views.shipment_file_upload, name='shipment_file_upload'),
    url(r'^result_file_upload/(?P<panel_id>\d+)/$', views.result_file_upload, name='result_file_upload'),
    url(r'^panel_memberships/(?P<panel_id>\d+)/$', views.panel_memberships, name='panel_memberships'),
    url(r'^panel_shipments/(?P<panel_id>\d+)/$', views.panel_shipments, name='panel_shipments'),
    url(r'^custom_assays/$', views.custom_assays, name='custom_assays'),
)
