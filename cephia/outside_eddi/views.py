from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from forms import (
    EddiUserCreationForm, TestHistoryFileUploadForm, StudyForm, TestPropertyMappingFormSet,
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
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.models import Group
from file_handlers.outside_eddi_test_history_file_handler import OutsideEddiFileHandler
from cephia.models import CephiaUser
from user_management.forms import UserPasswordForm
from models import (
    Study, OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate,
    TestPropertyMapping, OutsideEddiFileInfo, OutsideEddiDiagnosticTestHistory,
    OutsideEddiSubject
    )
from diagnostics.models import DiagnosticTest, TestPropertyEstimate
from django.forms import modelformset_factory
import json
from json import dumps
from django.db.models import Q
import datetime
from django.db import transaction
from dateutil.relativedelta import relativedelta
from django.db.models import Max


def outside_eddi_login_required(login_url=None):
    return user_passes_test(
        lambda u: u.is_authenticated() and u.groups.filter(name='Outside Eddi Users').exists(),
        login_url=login_url,
    )


@outside_eddi_login_required(login_url='outside_eddi:login')
def home(request, file_id=None, template="outside_eddi/home.html"):
    context = {}

    user = request.user.id
    studies = Study.objects.filter(user__id=request.user.id)

    context['studies'] = studies
    context['outside_eddi'] = True

    return render(request, template, context)


@csrf_exempt
def outside_eddi_login(request, template='outside_eddi/login.html'):
    context = {}
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()

            if user.is_locked_out():
                msg = "User %s got their login correct but is locked out so has not been allowed in. " % user.username
                messages.add_message(request, messages.WARNING, msg)
            else:
                if user.groups.filter(name=u'Outside Eddi Users').exists():
                    auth_login(request, user)
                    user.login_ok()
                    token = AuthenticationToken.create_token(user)
                    return redirect("outside_eddi:data_files")
                else:
                    msg = "User %s does not have the login credentials for this page so has not been allowed in. " % user.username
                    messages.add_message(request, messages.WARNING, msg)
        else:
            messages.add_message(request, messages.WARNING, "Invalid credentials")
            _check_for_login_hack_attempt(request, context)

    context['form'] = form
    return render(request, template, context)


def outside_eddi_logout(request, login_url=None, current_app=None, extra_context=None):
    if not login_url:
        login_url='outside_eddi:login'
    return django_logout(request, login_url, current_app=current_app, extra_context=extra_context)


@csrf_exempt
def outside_eddi_user_registration(request, template='outside_eddi/user_registration.html'):
    context = {}
    form = EddiUserCreationForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.send_registration_notification()

            tests = OutsideEddiDiagnosticTest.objects.all()

            if not tests:
                add_tests = _copy_diagnostic_tests()
                test_properties = _copy_test_properties()

            return redirect("outside_eddi:home")
        else:
            messages.add_message(request, messages.WARNING, "Invalid credentials")
            _check_for_login_hack_attempt(request, context)

    context['form'] = form

    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def data_files(request, file_id=None, template="outside_eddi/data_files.html"):
    context = {}

    user = request.user

    if request.method == 'POST':
        form = TestHistoryFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            errors = []
            errors = OutsideEddiFileHandler(uploaded_file).validate()
            if not errors:
                uploaded_file.user = user
                uploaded_file.save()
                uploaded_file = save_file_data(uploaded_file.pk, user)

                if uploaded_file.message:
                    messages.info(request, uploaded_file.message)
                    uploaded_file.state = 'error'
                    uploaded_file.save()
                elif uploaded_file.state == 'needs_mapping':
                    messages.info(request, 'Please provide mapping for your file')
                
                messages.info(request, u"Your file was uploaded successfully" )
            else:
                uploaded_file.delete()
                for error in errors:
                    messages.info(request, error)
                messages.info(request, 'Your file was not uploaded')

            return redirect("outside_eddi:data_files")

    else:
        form = TestHistoryFileUploadForm()

    context['form'] = form
    context['file_info_data'] = OutsideEddiFileInfo.objects.filter(user=user, deleted=False).order_by("-created")

    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def edit_study(request, study_id=None, template="outside_eddi/manage_studies.html"):
    context = {}

    if study_id is not None:
        study = get_object_or_404(Study, pk=study_id)
        form = StudyForm(request.user, request.POST or None, instance=study)
    else:
        study = None
        form = StudyForm(request.user, request.POST or None)

    if request.method == 'POST' and form.is_valid():
        study = form.save(request.user)
        if study_id:
            messages.info(request, u"Your study, %s was updated successfully" % study.name )
        else:
            messages.info(request, u"Your study, %s was created successfully" % study.name )
        return redirect('outside_eddi:edit_study', study_id=study.pk)

    context['form'] = form
    context['study'] = study

    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def tests(request, file_id=None, template="outside_eddi/tests.html"):
    context = {}
    user = request.user

    user_tests = OutsideEddiDiagnosticTest.objects.filter(user=user).order_by('name')
    global_tests = OutsideEddiDiagnosticTest.objects.filter(user__isnull=True).order_by('name')

    context['user_tests'] = user_tests
    context['global_tests'] = global_tests

    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def create_test(request, template='outside_eddi/create_test_form.html', context=None):
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
            instance.is_default = True
            instance.save()

        messages.info(request, 'Test added successfully')
        if request.is_ajax():
            return JsonResponse({'success': True, 'redirect_url': reverse("outside_eddi:tests")})
        else:
            return redirect("outside_eddi:tests")
    
    context['form'] = form
    context['user_estimates_formset'] = user_estimates_formset
    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def edit_test(request, test_id=None, template='outside_eddi/edit_test.html', context=None):
    context = context or {}
    user = request.user
    test = OutsideEddiDiagnosticTest.objects.get(pk=test_id)
    user_default_property_form = UserTestPropertyDefaultForm(request.POST or None)

    if test.user:
        form = UserTestForm(request.POST or None, instance=test)
        default_property = test.properties.filter(is_default=True).first()
        if default_property:
            context['default_property'] = default_property.pk
    else:
        form = GlobalTestForm(request.POST or None, instance=test)
        properties = OutsideEddiDiagnosticTest.objects.get(pk=test_id).properties.for_user(user=None)
        context['properties'] = properties

    user_estimates_formset = TestPropertyEstimateFormSet(
        request.POST or None,
        queryset=test.properties.filter(user=request.user)
    )

    if request.method == 'POST' and form.is_valid() and user_estimates_formset.is_valid():
        test_instance = form.save()

        for instance in user_estimates_formset.save(commit=False):
            instance.user = request.user
            instance.test = test
            instance.save()

        if test.user:
            default_property_pk = request.POST['default_property']
            if default_property_pk:
                user_test_properties = test_instance.properties.all().is_default = False
                default_property = OutsideEddiTestPropertyEstimate.objects.get(pk=default_property_pk)
                default_property.is_default = True
                default_property.save()

        messages.info(request, 'Test edited successfully')
        if request.is_ajax():
            return JsonResponse({'success': True, 'redirect_url': reverse("outside_eddi:tests")})
        else:
            return redirect("outside_eddi:tests")

    context['test'] = test
    context['form'] = form
    context['user_estimates_formset'] = user_estimates_formset
    context['user_default_property_form'] = user_default_property_form
    
    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def results(request, file_id=None, template="outside_eddi/results.html"):
    context = {}

    data_file = OutsideEddiFileInfo.objects.get(pk=file_id)
    test_history = OutsideEddiDiagnosticTestHistory.objects.filter(data_file=data_file)

    test_history_subjects = list(test_history.all().values_list('subject', flat=True).distinct())
    subjects = OutsideEddiSubject.objects.filter(pk__in=test_history_subjects)

    context['file'] = data_file
    context['subjects'] = subjects

    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def test_mapping(request, file_id=None, template="outside_eddi/test_mapping.html"):
    context = {}
    user = request.user
    is_file = False
    js_is_file = 'false'

    if file_id:
        data_file = OutsideEddiFileInfo.objects.get(pk=file_id)
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
    else:
        mapping = TestPropertyMapping.objects.filter(user=user).order_by('-pk')
        
    context['mapping'] = mapping
    context['is_file'] = is_file
    context['js_is_file'] = js_is_file
    
    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def create_test_mapping_properties(request, test_id=None, template='outside_eddi/create_mapping_form.html', context=None):
    return create_test_mapping(request, map_code, test_id, template)


@outside_eddi_login_required(login_url='outside_eddi:login')
def create_test_mapping(request, map_code=None, test_id=None, template='outside_eddi/create_mapping_form.html', context=None):
    context = {}
    user = request.user
    map_code = request.GET.get('map_code')
    
    if test_id:
        test_active_property = OutsideEddiDiagnosticTest.objects.get(pk=test_id).properties.filter(is_default=True).first()
        form = TestPropertyMappingForm(request.POST or None,
                                       initial={'test': test_id,
                                                'code': map_code,
                                                'test_property': test_active_property}
        )
        properties = OutsideEddiDiagnosticTest.objects.get(pk=test_id).properties.for_user(user=None)
        test = OutsideEddiDiagnosticTest.objects.get(pk=test_id)

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
    choices = GroupedModelChoiceField(queryset=OutsideEddiDiagnosticTest.objects.filter(Q(user=user) | Q(user=None)), group_by_field='user')
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
            return JsonResponse({'success': True, 'redirect_url': reverse("outside_eddi:test_mapping")})
        else:
            return redirect("outside_eddi:test_mapping")
    
    context['form'] = form
    context['user_estimates_formset'] = user_estimates_formset
    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def edit_test_mapping_properties(request, map_id=None, test_id=None, is_file=False, template='outside_eddi/edit_mapping_form.html', context=None):
    return edit_test_mapping(request, map_id, test_id, is_file, template)

@outside_eddi_login_required(login_url='outside_eddi:login')
def edit_test_mapping_file_properties(request, map_id=None, test_id=None, is_file=True, template='outside_eddi/edit_mapping_form.html', context=None):
    return edit_test_mapping(request, map_id, test_id, is_file, template)


@outside_eddi_login_required(login_url='outside_eddi:login')
def edit_test_mapping(request, map_id, test_id=None, is_file=False, template='outside_eddi/edit_mapping_form.html', context=None):
    context = context or {}

    user = request.user
    mapping = TestPropertyMapping.objects.get(pk=map_id)
    if test_id:
        map_code = request.GET.get('map_code')
        test = OutsideEddiDiagnosticTest.objects.get(pk=test_id)
        if mapping.test == test and mapping.test_property:
            test_active_property = mapping.test_property
        else:
            test_active_property = test.properties.filter(is_default=True).first()

        form = TestPropertyMappingForm(request.POST or None,
                                       instance=mapping,
                                       initial={'test': test_id,
                                                'code': map_code,
                                                'test_property': test_active_property}
        )
        properties = OutsideEddiDiagnosticTest.objects.get(pk=test_id).properties.for_user(user=None)
        
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
            properties = OutsideEddiTestPropertyEstimate.objects.none()

    
    form.set_context_data({'user': request.user})
    choices = GroupedModelChoiceField(queryset=OutsideEddiDiagnosticTest.objects.filter(Q(user=user) | Q(user=None)), group_by_field='user')
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
            return JsonResponse({'success': True, 'redirect_url': reverse("outside_eddi:test_mapping")})
        else:
            return redirect("outside_eddi:test_mapping")

    context['form'] = form
    context['properties'] = properties
    context['map'] = mapping
    context['is_file'] = is_file
    
    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def help_page(request, file_id=None, template="outside_eddi/help.html"):
    context = {}

    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def delete_data_file(request, file_id, context=None):
    context = context or {}

    data_file = OutsideEddiFileInfo.objects.get(pk=file_id)
    data_file_test_history = OutsideEddiDiagnosticTestHistory.objects.filter(data_file=data_file).delete()
    data_file.deleted = True
    data_file.save()
    
    messages.info(request, "Your file and all it's data has been deleted")
    return redirect(reverse('outside_eddi:data_files'))


@outside_eddi_login_required(login_url='outside_eddi:login')
def process_data_file(request, file_id, context=None):
    context = context or {}

    user = request.user
    data_file = validate_mapping(file_id, user)

    if data_file.state == 'mapped':
        subject_pks = list(data_file.test_history.all().values_list('subject', flat=True).distinct())
        subjects = OutsideEddiSubject.objects.filter(pk__in=subject_pks)
        update_adjusted_dates(user, data_file)
        
        lp_ddis = OutsideEddiDiagnosticTestHistory.objects.filter(test_result='Positive')
        lp_ddis = lp_ddis.values('subject')
        lp_ddis = lp_ddis.annotate(earliest_positive=Max('adjusted_date'))
        lp_ddis = dict((v['subject'], v['earliest_positive']) for v in lp_ddis)

        ep_ddis = OutsideEddiDiagnosticTestHistory.objects.filter(test_result='Negative')
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

    return redirect(reverse('outside_eddi:data_files'))


@outside_eddi_login_required(login_url='outside_eddi:login')
def validate_mapping_from_page(request, file_id, context=None):
    context = context or {}
    user = request.user
    validate_mapping(file_id, user)

    return test_mapping(request, file_id)


def finalise_user_account(request, token, template='outside_eddi/complete_signup.html', hide_error_message=None):
    context = {}

    user = CephiaUser.objects.get(password_reset_token=token)
    form = UserPasswordForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            user.set_password(self.cleaned_data['password'])
            user.is_active = True
            user.password_reset_token = None
            user.save()
            outside_eddi_group = Group.objects.get(name='Outside Eddi Users')
            outside_eddi_group.user_set.add(user)
            
            # user = form.save(user)
            return redirect("outside_eddi:home")
        else:
            messages.add_message(request, messages.WARNING, "Invalid credentials")
            _check_for_login_hack_attempt(request, context)



    context['token'] = token
    context['form'] = form
    return render_to_response(template, context, context_instance=RequestContext(request))


def _copy_diagnostic_tests():

    tests = DiagnosticTest.objects.all()

    for test in tests:
        outside_eddi_test = OutsideEddiDiagnosticTest.objects.create(name = test.name,
                                                                     description = test.description)

def _copy_test_properties():

    test_properties = TestPropertyEstimate.objects.all()

    for prop in test_properties:
        test_name = prop.test.name
        test = OutsideEddiDiagnosticTest.objects.filter(name=test_name).first()

        outside_eddi_test_property = OutsideEddiTestPropertyEstimate.objects.create(test = test,
                                                                                    estimate_label=prop.estimate_label,
                                                                                    estimate_type=prop.estimate_type,
                                                                                    mean_diagnostic_delay_days=prop.mean_diagnostic_delay_days,
                                                                                    diagnostic_delay_median=prop.diagnostic_delay_median,
                                                                                    foursigma_diagnostic_delay_days=prop.foursigma_diagnostic_delay_days,
                                                                                    time0_ref=prop.time0_ref,
                                                                                    comment=prop.comment,
                                                                                    reference=prop.reference)

        if prop.is_default == True:
            outside_eddi_test_property.is_default = True
            outside_eddi_test_property.active_property = True

        outside_eddi_test_property.save()


def test_properties_mapping(request, test):
    user = request.user

    formset = TestPropertyEstimateFormSet(
        request.POST or None,
        queryset=OutsideEddiTestPropertyEstimate.objects.filter(
            Q(user=user) | Q(user=None),
            test__pk=test.pk
        ),
        prefix='properties'
    )

    return formset


def set_active_property(test):
    properties = OutsideEddiTestPropertyEstimate.objects.filter(test=test)
    for prop in properties:
        prop.active_property = False
        if prop.is_default == True:
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
    data_file = OutsideEddiFileInfo.objects.get(pk=file_id)
    OutsideEddiFileHandler(data_file).save_data(user)
    mapping = data_file.create_mapping(user)
    check_mapping_details(mapping, user, data_file)

    return data_file


def validate_mapping(file_id, user):
    data_file = OutsideEddiFileInfo.objects.get(pk=file_id)
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
        file_test_history = OutsideEddiDiagnosticTestHistory.objects.filter(data_file=data_file)
        codes = list( file_test_history.all().values_list('test_code', flat=True).distinct() )
        mapping = TestPropertyMapping.objects.filter(code__in=codes, user=user)

        map_property_means = list( mapping.values_list(
            'code', 'test_property__mean_diagnostic_delay_days'
        ).distinct() )
        
        map_property_means = dict( (v[0], v[1]) for v in map_property_means )
        test_history_dates = list( file_test_history.values_list('test_code', 'test_date') )
        dates_means = dict( (v[0], (v[1], int(map_property_means[v[0]]))) for v in test_history_dates )
        
        for test_history in file_test_history:
            test_code = test_history.test_code
            test_date = dates_means[test_code][0]
            mean_diagnostic_delay_days = dates_means[test_code][1]
            test_history.adjusted_date = test_date - relativedelta(days=mean_diagnostic_delay_days)
            test_history.save()
