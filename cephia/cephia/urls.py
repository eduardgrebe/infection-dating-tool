"""cephia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.home, name='home'),

    url(r'^countries/$', views.countries, name='countries'),
    url(r'^ethnicity/$', views.ethnicity, name='ethnicity'),
    url(r'^subjects/$', views.subjects, name='subjects'),
    url(r'^file_info/$', views.file_info, name='file_info'),
    url(r'^row_info/(?P<file_id>\d+)/$', views.row_info, name='row_info'),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^download_file/(?P<file_id>\d+)/$', views.download_file, name='download_file'),
    url(r'^process_file/(?P<file_id>\d+)/$', views.process_file, name='process_file'),
    url(r'^parse_file/(?P<file_id>\d+)/$', views.parse_file, name='parse_file'),
    url(r'^delete_row/(?P<row_id>\d+)/$', views.delete_row, name='delete_row'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, name='auth_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='auth_logout'),
    url(r'^accounts/password-change/$', 'django.contrib.auth.views.password_change', name='change_password'),
    url(r'^accounts/password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^accounts/password-reset/$', 'django.contrib.auth.views.password_reset', name='reset_password'),
    url(r'^accounts/password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    
]
