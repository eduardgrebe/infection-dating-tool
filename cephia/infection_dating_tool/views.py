from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from forms import (
    IDTUserCreationForm, TestHistoryFileUploadForm, TestPropertyMappingFormSet,
    DataFileTestPropertyMappingFormSet, TestPropertyEstimateFormSet,
    GlobalTestForm, UserTestForm, GroupedModelChoiceField, GroupedModelMultiChoiceField,
    TestPropertyMappingForm, UserTestPropertyDefaultForm
    )
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from user_management.views import _check_for_login_hack_attempt
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from user_management.models import AuthenticationToken
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.models import Group
from file_handlers.idt_test_history_file_handler import IDTFileHandler
from file_handlers.idt_test_and_properties_file_handler import TestsAndPropertiesFileHandler
from user_management.forms import UserPasswordForm
from models import (
    IDTDiagnosticTest, IDTTestPropertyEstimate,
    TestPropertyMapping, IDTFileInfo, IDTDiagnosticTestHistory,
    IDTSubject
    )
from cephia.models import CephiaUser
from diagnostics.models import DiagnosticTest, TestPropertyEstimate
from django.forms import modelformset_factory
import json
from json import dumps
from django.db.models import Q
from datetime import datetime
import datetime
from django.db import transaction
from dateutil.relativedelta import relativedelta
from django.db.models import Max
from result_factory import ResultDownload
from cephia.csv_helper import get_csv_response
import os
from django.core.mail import send_mail
from collections import OrderedDict

CATEGORIES = (
    ('western_blot', 'Western blot'),
    ('1st_gen_lab', '1st Gen Lab Assay (Viral Lysate IgG sensitive Antibody)'),
    ('2nd_gen_lab', '2nd Gen Lab Assay (Recombinant IgG sensitive Antibody)'),
    ('2nd_gen_rapid', '2nd Gen Rapid Test'),
    ('3rd_gen_lab', '3rd Gen Lab Assay (IgM sensitive Antibody)'),
    ('3rd_gen_rapid', '3rd Gen Rapid Test'),
    ('p24_antigen', 'p24 Antigen'),
    ('4th_gen_lab', '4th Gen Lab Assay (p24 Ag/Ab Combo)'),
    ('4th_gen_rapid', '4th Gen Rapid Test'),
    ('viral_load', 'Viral Load'),
    ('dpp', 'DPP'),
    ('immunofluorescence_assay', 'Immunofluorescence Assay'),
    ('No category', 'No category'),
)

def idt_login_required(login_url=None):
    return user_passes_test(
        lambda u: u.is_authenticated() and u.groups.filter(name='Infection Dating Tool Users').exists(),
        login_url=login_url,
    )


@idt_login_required(login_url='login')
def home(request, file_id=None, template="infection_dating_tool/home.html"):
    context = {}

    user = request.user.id

    context['infection_dating_tool'] = True
    
    return redirect("data_files")


@csrf_exempt
def idt_login(request, template='infection_dating_tool/login.html'):
    context = {}
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()

            if user.is_locked_out():
                msg = "User %s got their login correct but is locked out so has not been allowed in. " % user.username
                messages.add_message(request, messages.WARNING, msg)
            else:
                if user.groups.filter(name=u'Infection Dating Tool Users').exists():
                    auth_login(request, user)
                    user.login_ok()
                    token = AuthenticationToken.create_token(user)
                    return redirect("data_files")
                else:
                    msg = "User %s does not have the login credentials for this page so has not been allowed in. " % user.username
                    messages.add_message(request, messages.WARNING, msg)
        else:
            messages.add_message(request, messages.WARNING, "Invalid credentials")
            _check_for_login_hack_attempt(request, context)

    context['form'] = form
    return render(request, template, context)


def idt_logout(request, login_url=None, current_app=None, extra_context=None):
    if not login_url:
        login_url='login'
    return django_logout(request, login_url, current_app=current_app, extra_context=extra_context)


@csrf_exempt
def idt_user_registration(request, template='infection_dating_tool/user_registration.html'):
    context = {}
    form = IDTUserCreationForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.send_registration_notification()

            return redirect("registration_info")
        else:
            messages.add_message(request, messages.WARNING, "Invalid credentials")
            _check_for_login_hack_attempt(request, context)

    context['form'] = form

    return render(request, template, context)


@csrf_exempt
def idt_user_registration_info(request, template='infection_dating_tool/user_registration_info.html'):
    context = {}

    return render(request, template, context)


@idt_login_required(login_url='login')
def data_files(request, file_id=None, template="infection_dating_tool/data_files.html"):
    context = {}

    user = request.user

    if request.method == 'POST':
        form = TestHistoryFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            name, file_ext = uploaded_file.filename().split('.')
            uploaded_file.file_name = name
            uploaded_file.save()

            errors = []
            errors = IDTFileHandler(uploaded_file).validate()
            if not errors:
                uploaded_file.user = user
                uploaded_file.save()
                with transaction.atomic():
                    saving_errors, uploaded_file = save_file_data(uploaded_file.pk, user)

                if saving_errors:
                    uploaded_file.delete()
                    for error in saving_errors:
                        messages.info(request, error)
                        messages.info(request, 'Your file was unable to save so it was not uploaded')
                    # messages.info(request, uploaded_file.message)
                    # uploaded_file.state = 'error'
                    # uploaded_file.save()
                elif uploaded_file.state == 'needs_mapping' or uploaded_file.state == 'mapped':
                    if uploaded_file.state == 'needs_mapping':
                        messages.info(request, 'Please provide mapping for your file')
                    messages.info(request, u"Your file was uploaded successfully" )
                
            else:
                uploaded_file.delete()
                for error in errors:
                    messages.info(request, error)
                messages.info(request, 'Your file was not uploaded')

            return redirect("data_files")

    else:
        form = TestHistoryFileUploadForm()

    context['data_files_page'] = True
    context['form'] = form
    context['file_info_data'] = IDTFileInfo.objects.filter(user=user, deleted=False).order_by("-created")

    return render(request, template, context)


@idt_login_required(login_url='login')
def tests(request, file_id=None, template="infection_dating_tool/tests.html"):
    context = {}
    user = request.user

    user_tests = IDTDiagnosticTest.objects.filter(user=user).order_by('name')
    global_tests = IDTDiagnosticTest.objects.filter(user__isnull=True).order_by('category', 'name')
    global_tests_dict = OrderedDict()

    for category in CATEGORIES:
        if category[0] != 'No category':
            tests = global_tests.filter(category=category[0])
        else:
            tests = global_tests.filter(category__isnull=True)
        global_tests_dict[category[1]] = tests
                
    context['user_tests'] = user_tests
    context['global_tests'] = global_tests_dict

    return render(request, template, context)


@idt_login_required(login_url='login')
def create_test(request, template='infection_dating_tool/create_test_form.html', context=None):
    context = {}
    user = request.user

    form = GlobalTestForm(request.POST or None)
    form.set_context_data({'user': request.user})

    user_estimates_formset = TestPropertyEstimateFormSet(
        request.POST or None,
        queryset=TestPropertyEstimate.objects.none()
    )

    if request.method == 'POST' and form.is_valid() and user_estimates_formset.is_valid():
        test_instance = form.save()
        test_instance.user = user
        test_instance.save()

        for instance in user_estimates_formset.save(commit=False):
            instance.user = request.user
            instance.test = test_instance
            instance.global_default = True
            instance.save()

        messages.info(request, 'Test added successfully')
        if request.is_ajax():
            return JsonResponse({'success': True, 'redirect_url': reverse("tests")})
        else:
            return redirect("tests")
    
    context['form'] = form
    context['user_estimates_formset'] = user_estimates_formset
    return render(request, template, context)


@idt_login_required(login_url='login')
def edit_test(request, test_id=None, template='infection_dating_tool/edit_test.html', context=None):
    context = context or {}
    user = request.user
    test = IDTDiagnosticTest.objects.get(pk=test_id)
    user_default_property_form = UserTestPropertyDefaultForm(request.POST or None)

    if test.user:
        form = UserTestForm(request.POST or None, instance=test)
        default_property = test.properties.filter(global_default=True).first()
        if default_property:
            context['default_property'] = default_property.pk
    else:
        form = GlobalTestForm(request.POST or None, instance=test)
        form.fields['category'].initial = test.category
        properties = IDTDiagnosticTest.objects.get(pk=test_id).properties.for_user(user=None)
        context['properties'] = properties

    user_estimates_formset = TestPropertyEstimateFormSet(
        request.POST or None,
        queryset=test.properties.filter(user=request.user)
    )

    if request.method == 'POST' and form.is_valid() and user_estimates_formset.is_valid():
        if test.user:
            test_instance = form.save()
        else:
            test_instance = test

        for instance in user_estimates_formset.save(commit=False):
            instance.user = request.user
            instance.test = test
            instance.save()

        if test.user:
            default_property_pk = request.POST['default_property']
            user_test_properties = test_instance.properties.all().global_default = False
            if default_property_pk:
                default_property = IDTTestPropertyEstimate.objects.get(pk=default_property_pk)
            else:
                default_property = test_instance.properties.all().order_by('-pk').first()
            default_property.global_default = True
            default_property.save()

        messages.info(request, 'Test edited successfully')
        if request.is_ajax():
            return JsonResponse({'success': True, 'redirect_url': reverse("tests")})
        else:
            return redirect("tests")

    context['test'] = test
    context['form'] = form
    context['user_estimates_formset'] = user_estimates_formset
    context['user_default_property_form'] = user_default_property_form
    
    return render(request, template, context)


@idt_login_required(login_url='login')
def results(request, file_id=None, template="infection_dating_tool/results.html"):
    context = {}

    data_file = IDTFileInfo.objects.get(pk=file_id)
    test_history = IDTDiagnosticTestHistory.objects.filter(data_file=data_file)

    test_history_subjects = list(test_history.all().values_list('subject', flat=True).distinct())
    subjects = IDTSubject.objects.filter(pk__in=test_history_subjects)

    context['file'] = data_file
    context['subjects'] = subjects

    return render(request, template, context)


@idt_login_required(login_url='login')
def download_results(request, file_id=None, context=None):
    data_file = IDTFileInfo.objects.get(pk=file_id)
    test_history = IDTDiagnosticTestHistory.objects.filter(data_file=data_file)

    test_history_subjects = list(test_history.all().values_list('subject', flat=True).distinct())
    subjects = IDTSubject.objects.filter(pk__in=test_history_subjects)

    download = ResultDownload(subjects)

    response, writer = get_csv_response('infection_dates_%s_%s.csv' % (
        data_file.file_name, datetime.datetime.today().strftime('%d%b%Y_%H%M')))
    
    writer.writerow(download.get_headers())

    for row in download.get_content():
        writer.writerow(row)

    return response


@idt_login_required(login_url='login')
def test_mapping(request, file_id=None, template="infection_dating_tool/test_mapping.html"):
    context = {}
    user = request.user
    is_file = False
    js_is_file = 'false'

    if file_id:
        data_file = IDTFileInfo.objects.get(pk=file_id)
        is_file = True
        js_is_file = 'true'
        
        codes = list(data_file.test_history.all().values_list('test_code', flat=True).distinct())
        mapping = TestPropertyMapping.objects.filter(code__in=codes, user=user).order_by('-pk')

        if data_file.state == 'mapped' or data_file.state == 'processed':
            completed_mapping = True
        else:
            completed_mapping = False

        context['completed_mapping'] = completed_mapping
        context['data_file'] = data_file
        context['file_name'] = os.path.basename(data_file.data_file.name)
    else:
        mapping = TestPropertyMapping.objects.filter(user=user).order_by('-pk')
        
    context['mapping'] = mapping
    context['is_file'] = is_file
    context['js_is_file'] = js_is_file
    
    return render(request, template, context)


@idt_login_required(login_url='login')
def create_test_mapping_properties(request, test_id=None, template='infection_dating_tool/create_mapping_form.html', context=None):
    return create_test_mapping(request, map_code, test_id, template)


@idt_login_required(login_url='login')
def create_test_mapping(request, map_code=None, test_id=None, template='infection_dating_tool/create_mapping_form.html', context=None):
    context = {}
    user = request.user
    map_code = request.GET.get('map_code')
    
    if test_id:
        test_active_property = IDTDiagnosticTest.objects.get(pk=test_id).properties.filter(global_default=True).first()
        form = TestPropertyMappingForm(request.POST or None,
                                       initial={'test': test_id,
                                                'code': map_code,
                                                'test_property': test_active_property}
        )
        properties = IDTDiagnosticTest.objects.get(pk=test_id).properties.for_user(user=None)
        test = IDTDiagnosticTest.objects.get(pk=test_id)

        user_estimates_formset = TestPropertyEstimateFormSet(
            request.POST or None,
            queryset=test.properties.filter(user=request.user)
        )
        context['test'] = test
        context['properties'] = properties
        context['map_code'] = map_code
    
    else:
        form = TestPropertyMappingForm(request.POST or None)
        user_estimates_formset = TestPropertyEstimateFormSet(
            request.POST or None
        )

    form.set_context_data({'user': request.user})

    choices = GroupedModelChoiceField(queryset=IDTDiagnosticTest.objects.filter(Q(user=user) | Q(user=None)), group_by_field='category')

    form.fields['test'] = choices

    if request.method == 'POST' and form.is_valid() and user_estimates_formset.is_valid():
        mapping_instance = form.save()

        selected_property = None
        for instance in user_estimates_formset.save(commit=False):
            instance.user = request.user
            instance.test = mapping_instance.test
            if instance.pk is None and mapping_instance.test_property is None:
                selected_property = instance
            instance.save()

        if mapping_instance.test_property is None:
            mapping_instance.test_property = selected_property
            mapping_instance.save()

        messages.info(request, 'Mapping added successfully')
        if request.is_ajax():
            return JsonResponse({'success': True, 'redirect_url': reverse("test_mapping")})
        else:
            return redirect("test_mapping")
    
    context['form'] = form
    context['user_estimates_formset'] = user_estimates_formset
    return render(request, template, context)


@idt_login_required(login_url='login')
def edit_test_mapping_properties(request, map_id=None, test_id=None, is_file=False, template='infection_dating_tool/edit_mapping_form.html', context=None):
    return edit_test_mapping(request, map_id, test_id, is_file, template)

@idt_login_required(login_url='login')
def edit_test_mapping_file_properties(request, map_id=None, test_id=None, is_file=True, template='infection_dating_tool/edit_mapping_form.html', context=None):
    return edit_test_mapping(request, map_id, test_id, is_file, template)


@idt_login_required(login_url='login')
def edit_test_mapping(request, map_id, test_id=None, is_file=False, template='infection_dating_tool/edit_mapping_form.html', context=None):
    context = context or {}

    user = request.user
    mapping = TestPropertyMapping.objects.get(pk=map_id)
    if test_id:
        map_code = request.GET.get('map_code')
        test = IDTDiagnosticTest.objects.get(pk=test_id)
        if mapping.test == test and mapping.test_property:
            test_active_property = mapping.test_property
        else:
            test_active_property = test.properties.filter(global_default=True).first()

        form = TestPropertyMappingForm(request.POST or None,
                                       instance=mapping,
                                       initial={'test': test_id,
                                                'code': map_code,
                                                'test_property': test_active_property}
        )
        properties = IDTDiagnosticTest.objects.get(pk=test_id).properties.for_user(user=None)
        
        context['test'] = test

        user_estimates_formset = TestPropertyEstimateFormSet(
            request.POST or None,
            queryset=test.properties.filter(user=request.user)
        )
        context['user_estimates_formset'] = user_estimates_formset
    else:
        form = TestPropertyMappingForm(request.POST or None, instance=mapping)
        if mapping.test:
            properties = mapping.test.properties.for_user(user=None)
            user_estimates_formset = TestPropertyEstimateFormSet(
                request.POST or None,
                queryset=mapping.test.properties.filter(user=request.user)
            )
            context['user_estimates_formset'] = user_estimates_formset
        else:
            user_estimates_formset = TestPropertyEstimateFormSet(
                request.POST or None
            )
            properties = IDTTestPropertyEstimate.objects.none()

    
    form.set_context_data({'user': request.user})
    choices = GroupedModelChoiceField(queryset=IDTDiagnosticTest.objects.filter(Q(user=user) | Q(user=None)), group_by_field='category')
    form.fields['test'] = choices
    if is_file:
        form.fields['code'].widget.attrs['readonly'] = True
    
    if request.method == 'POST' and form.is_valid() and user_estimates_formset.is_valid():
        mapping_instance = form.save()

        selected_property = None
        for instance in user_estimates_formset.save(commit=False):
            instance.user = request.user
            instance.test = mapping_instance.test
            if instance.pk is None and mapping_instance.test_property is None:
                selected_property = instance
            instance.save()

        if mapping_instance.test_property is None:
            mapping_instance.test_property = selected_property
            mapping_instance.save()
        
                
        messages.info(request, 'Mapping edited successfully')
        if request.is_ajax():
            return JsonResponse({'success': True, 'redirect_url': reverse("test_mapping")})
        else:
            return redirect("test_mapping")

    context['form'] = form
    context['properties'] = properties
    context['map'] = mapping
    context['is_file'] = is_file
    
    return render(request, template, context)



def help_page(request, file_id=None, template="infection_dating_tool/help.html"):
    context = {}

    return render(request, template, context)


@idt_login_required(login_url='login')
def delete_data_file(request, file_id, context=None):
    context = context or {}

    data_file = IDTFileInfo.objects.get(pk=file_id)
    data_file_test_history = IDTDiagnosticTestHistory.objects.filter(data_file=data_file).delete()
    data_file.deleted = True
    data_file.save()
    
    messages.info(request, "Your file and all it's data has been deleted")
    return redirect(reverse('data_files'))


@idt_login_required(login_url='login')
def process_data_file(request, file_id, context=None):
    context = context or {}

    user = request.user
    data_file = validate_mapping(file_id, user)

    if data_file.state == 'mapped':
        subject_pks = list(data_file.test_history.all().values_list('subject', flat=True).distinct())
        subjects = IDTSubject.objects.filter(pk__in=subject_pks)
        update_adjusted_dates(user, data_file)
        
        lp_ddis = IDTDiagnosticTestHistory.objects.filter(test_result='Positive')
        lp_ddis = lp_ddis.values('subject')
        lp_ddis = lp_ddis.annotate(earliest_positive=Max('adjusted_date'))
        lp_ddis = dict((v['subject'], v['earliest_positive']) for v in lp_ddis)

        ep_ddis = IDTDiagnosticTestHistory.objects.filter(test_result='Negative')
        ep_ddis = ep_ddis.values('subject')
        ep_ddis = ep_ddis.annotate(latest_negative=Max('adjusted_date'))
        ep_ddis = dict((v['subject'], v['latest_negative']) for v in ep_ddis)
        
        with transaction.atomic():
            for subject in subjects:
                subject.calculate_eddi(user, data_file, lp_ddis.get(subject.pk), ep_ddis.get(subject.pk))
        data_file.state = 'processed'
        data_file.save()
        messages.info(request, 'Data Processed')
    elif data_file.state == 'needs_mapping':
        messages.info(request, 'Incomplete Mapping. Cannot process data')

    return redirect(reverse('data_files'))


@idt_login_required(login_url='login')
def validate_mapping_from_page(request, file_id, context=None):
    context = context or {}
    user = request.user
    validate_mapping(file_id, user)

    return test_mapping(request, file_id)


def finalise_user_account(request, token, template='infection_dating_tool/complete_signup.html', hide_error_message=None):
    context = {}

    user = CephiaUser.objects.get(password_reset_token=token)
    form = UserPasswordForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            user_instance = form.save(user)
            password = form.cleaned_data['password']
            auth_user = authenticate(username=user_instance.username, password=password)
            
            if auth_user:
                auth_login(request, auth_user)
                auth_user.login_ok()
                token = AuthenticationToken.create_token(auth_user)
                return redirect("data_files")

    context['token'] = token
    context['form'] = form

    return render_to_response(template, context, context_instance=RequestContext(request))


def test_properties_mapping(request, test):
    user = request.user

    formset = TestPropertyEstimateFormSet(
        request.POST or None,
        queryset=IDTTestPropertyEstimate.objects.filter(
            Q(user=user) | Q(user=None),
            test__pk=test.pk
        ),
        prefix='properties'
    )

    return formset


def set_active_property(test):
    properties = IDTTestPropertyEstimate.objects.filter(test=test)
    for prop in properties:
        prop.active_property = False
        if prop.global_default == True:
            prop.active_property = True
        prop.save()


def check_mapping_details(mapping, user, data_file):
    completed_mapping = True
    for m in mapping:
        if not m.code or not  m.test or not m.test_property:
            completed_mapping = False
        elif m.code and m.test and m.test_property:
            if m.test_property not in m.test.properties.all():
                completed_mapping = False

        if completed_mapping == False:
            break

    if completed_mapping:
        data_file.state = 'mapped'
    elif not completed_mapping:
        data_file.state = 'needs_mapping'
    data_file.save()

    return completed_mapping


def save_file_data(file_id, user):
    data_file = IDTFileInfo.objects.get(pk=file_id)
    errors = IDTFileHandler(data_file).save_data(user)
    if not errors:
        mapping = data_file.create_mapping(user)
        check_mapping_details(mapping, user, data_file)

    return errors, data_file


def validate_mapping(file_id, user):
    data_file = IDTFileInfo.objects.get(pk=file_id)
    codes = list(data_file.test_history.all().values_list('test_code', flat=True).distinct())
    mapping = TestPropertyMapping.objects.filter(code__in=codes, user=user)

    if len(codes) > mapping.count():
        codes_with_map = list(mapping.filter(code__in=codes).values_list('code', flat=True))
        codes_without_map = list(set(codes) - set(codes_with_map))

        for code in codes_without_map:
            new_map = TestPropertyMapping.objects.create(
                code=code,
                user=user
            )
        mapping = TestPropertyMapping.objects.filter(code__in=codes, user=user)

    check_mapping_details(mapping, user, data_file)

    return data_file


def update_adjusted_dates(user, data_file):
    with transaction.atomic():
        file_test_history = IDTDiagnosticTestHistory.objects.filter(data_file=data_file)
        codes = list( file_test_history.all().values_list('test_code', flat=True).distinct() )
        mapping = TestPropertyMapping.objects.filter(code__in=codes, user=user)

        map_property_means = list( mapping.values_list(
            'code', 'test_property__diagnostic_delay'
        ).distinct() )
        
        map_property_means = dict( (v[0], v[1]) for v in map_property_means )
        test_history_dates = list( file_test_history.values_list('test_code', 'test_date', 'id') )

        dates_means = dict( (v[2], (v[1], int(map_property_means[v[0]]))) for v in test_history_dates )
        
        for test_history in file_test_history:
            dict_values = dates_means[test_history.id]
            # test_code = test_history.test_code
            test_date = dict_values[0]
            diagnostic_delay = dict_values[1]
            test_history.adjusted_date = test_date - relativedelta(days=diagnostic_delay)
            test_history.save()
