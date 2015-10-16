from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    
    url(r'^visit_report/', views.visit_report, name='visit_report'),
    
    ]

    