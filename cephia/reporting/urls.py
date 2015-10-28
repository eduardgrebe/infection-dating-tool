from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    url(r'^report_landing_page/', views.report_landing_page, name='report_landing_page'),

    url(r'^all_subject_material/', views.all_subject_material, name='all_subject_material'), # under construction
    
    url(r'^generic_report/', views.generic_report, name='generic_report'),
    
    url(r'^visit_material/', views.visit_material, name='visit_material'), # main report page for view and csv
    url(r'^visit_specimen_report/', views.visit_specimen_report, name='visit_specimen_report'), #popup
    url(r'^visit_specimen_detail_download/', views.visit_specimen_detail_download, name='visit_specimen_detail_download'), # popup download

    # Sample of a custom query
    url(r'^fixed_query_template/', views.fixed_query_template, name='fixed_query_template'),
    
    
]
