from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from infection_dating_tool import views as idt_views

urlpatterns = [
    url(r'^$', idt_views.home, name='home'),
    url(r'^idt/$', idt_views.home),

    url(r'^register/$', idt_views.idt_user_registration, name='registration'),
    url(r'^idt/register/$', idt_views.idt_user_registration),

    url(r'^register/info/$', idt_views.idt_user_registration_info, name='registration_info'),
    url(r'^idt/register/info/$', idt_views.idt_user_registration_info),

    url(r'^login/$', idt_views.idt_login, name='login'),
    url(r'^idt/login/$', idt_views.idt_login),

    url(r'^logout/$', idt_views.idt_logout, name='logout'),
    url(r'^idt/logout/$', idt_views.idt_logout),

    url(r'^data_files/$', idt_views.data_files, name='data_files'),
    url(r'^idt/data_files/$', idt_views.data_files),

    url(r'^help/$', idt_views.help_page, name='help_page'),
    url(r'^idt/help/$', idt_views.help_page),

    url(r'^tests/$', idt_views.tests, name='tests'),
    url(r'^idt/tests/$', idt_views.tests),

    url(r'^tests/(?P<test_id>\d+)/edit/$', idt_views.edit_test, name='edit_test'),
    url(r'^idt/tests/(?P<test_id>\d+)/edit/$', idt_views.edit_test),

    url(r'^tests/create/$', idt_views.create_test, name='create_test'),
    url(r'^idt/tests/create/$', idt_views.create_test),

    url(r'^test_mapping/$', idt_views.test_mapping, name='test_mapping'),
    url(r'^idt/test_mapping/$', idt_views.test_mapping),

    url(r'^test_mapping/(?P<file_id>\d+)/$', idt_views.test_mapping, name='test_mapping'),
    url(r'^idt/test_mapping/(?P<file_id>\d+)/$', idt_views.test_mapping),

    url(r'^test_mapping/create/$', idt_views.create_test_mapping, name='create_test_mapping'),
    url(r'^idt/test_mapping/create/$', idt_views.create_test_mapping),

    url(r'^test_mapping/edit/$', idt_views.edit_test_mapping, name='edit_test_mapping'),
    url(r'^idt/test_mapping/edit/$', idt_views.edit_test_mapping),

    url(r'^test_mapping/edit/(?P<save_map_id>\d+)/$', idt_views.edit_test_mapping, name='edit_test_mapping_save'),
    url(r'^idt/test_mapping/edit/(?P<save_map_id>\d+)/$', idt_views.edit_test_mapping),

    url(r'^data_files/(?P<file_id>\d+)/delete', idt_views.delete_data_file, name='delete_data_file'),
    url(r'^idt/data_files/(?P<file_id>\d+)/delete', idt_views.delete_data_file),

    url(r'^data_files/(?P<file_id>\d+)/process_data', idt_views.process_data_file, name='process_data_file'),
    url(r'^idt/data_files/(?P<file_id>\d+)/process_data', idt_views.process_data_file),

    url(r'^validate_mapping/(?P<file_id>\d+)/', idt_views.validate_mapping_from_page, name='validate_mapping_from_page'),
    url(r'^idt/validate_mapping/(?P<file_id>\d+)/', idt_views.validate_mapping_from_page),

    url(r'^results/(?P<file_id>\d+)/$', idt_views.results, name='results'),
    url(r'^idt/results/(?P<file_id>\d+)/$', idt_views.results),

    url(r'^results/(?P<file_id>\d+)/download/$', idt_views.download_results, name='download_results'),
    url(r'^idt/results/(?P<file_id>\d+)/download/$', idt_views.download_results),

    url(r'^user_registration/finalise/(?P<token>.*)/$', idt_views.finalise_user_account, name='finalise_user_account'),
    url(r'^idt/user_registration/finalise/(?P<token>.*)/$', idt_views.finalise_user_account),

    url(r'^tests/set_selected_category/$', idt_views.set_selected_category, name='set_selected_category'),
    url(r'^idt/tests/set_selected_category/$', idt_views.set_selected_category),

    url(r'^mapping/get_test_category/$', idt_views.get_test_category, name='get_test_category'),
    url(r'^idt/mapping/get_test_category/$', idt_views.get_test_category),

    url(r'^idt/residual_risk/$', idt_views.residual_risk),
    url(r'^residual_risk/$', idt_views.residual_risk, name='residual_risk'),

    url(r'^idt/residual_risk/estimates/$', idt_views.residual_risk_estimates),
    url(r'^residual_risk/estimates/$', idt_views.residual_risk_estimates, name='residual_risk_estimates'),

    url(r'^idt/residual_risk/estimates/specify/$', idt_views.residual_risk_estimates_specify, {'form_selection': 'specify'}),
    url(r'^residual_risk/estimates/specify/$', idt_views.residual_risk_estimates_specify, {'form_selection': 'specify'}, name='residual_risk_estimates_specify'),

    url(r'^idt/residual_risk/estimates/calculate/$', idt_views.residual_risk_estimates_calculate, {'form_selection': 'calculate'}),
    url(r'^residual_risk/estimates/calculate/$', idt_views.residual_risk_estimates_calculate, {'form_selection': 'calculate'}, name='residual_risk_estimates_calculate'),

    url(r'^idt/residual_risk/calculate/data/$', idt_views.residual_risk_data),
    url(r'^residual_risk/calculate/data/$', idt_views.residual_risk_data, name='residual_risk_data'),

    url(r'^idt/residual_risk/calculate/supply/$', idt_views.residual_risk_supply),
    url(r'^residual_risk/calculate/supply/$', idt_views.residual_risk_supply, name='residual_risk_supply'),

    url(r'^idt/residual_risk_window/$', idt_views.residual_risk_window),
    url(r'^residual_risk_window/$', idt_views.residual_risk_window, name='residual_risk_window'),

    url(r'^idt/infectious_period/reset_defaults/$', idt_views.reset_defaults_infectious_period),
    url(r'^infectious_period/reset_defaults/$', idt_views.reset_defaults_infectious_period, name='reset_defaults_infectious_period'),

    url(r'^idt/calculation_params/reset_defaults/$', idt_views.reset_defaults_calculation_params),
    url(r'^calculation_params/reset_defaults/$', idt_views.reset_defaults_calculation_params, name='reset_defaults_calculation_params'),

]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
