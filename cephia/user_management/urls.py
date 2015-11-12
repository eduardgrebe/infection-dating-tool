from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns(
    '',
    #url(r'^is_logged_in/$', views.is_logged_in, name='is_logged_in'),
    url(r'^login/$', views.login, {'template_name': 'admin/cephia_login.html'}, name='auth_login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='change_password'),
    #url(r'^check_activation_key/$', views.check_activation_key, name='check_activation_key'),
    #url(r'^activate/$', views.activate_user, name='activate_user'),
    #url(r'^generate_activation_key/$', views.generate_activation_key, name='generate_activation_key'),
    #url(r'^send_activation_email/$', views.send_activation_email, name='send_activation_email'),
    url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='reset_password'),
    url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

    #url(r'^users/$', views.user_list, name='user_list'),
    #url(r'^unactivated_users/$', views.unactivated_users, name='unactivated_users'),
    url(r'^user_edit/$', views.user_edit, name='user_edit'),
    url(r'^user_add/$', views.user_add, name='user_add'),
    #url(r'^profile/$', views.user_profile, name='user_profile'),

    # url(r'^groups/$', views.group_list, name='group_list'),
    # url(r'^group_edit/$', views.group_edit, name='group_edit'),
    # url(r'^group_add/$', views.group_add, name='group_add'),

)

