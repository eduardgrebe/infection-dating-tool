from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from forms import EddiUserCreationForm, TestHistoryFileUploadForm, StudyForm, TestPropertyMappingFormSet, DataFileTestPropertyMappingFormSet, TestPropertyEstimateFormSet, GlobalTestFormSet, UserTestFormSet
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
from models import Study, OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate, TestPropertyMapping, OutsideEddiFileInfo
from diagnostics.models import DiagnosticTest, TestPropertyEstimate
from django.forms import modelformset_factory
import json
from json import dumps
from django.db.models import Q
import datetime

def outside_eddi_login_required(login_url=None):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='Outside Eddi Users').exists(),
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
                    return redirect("outside_eddi:home")
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
                uploaded_file.state = 'validated'
                uploaded_file.save()
                messages.info(request, u"Your file was uploaded successfully" )
            else:
                uploaded_file.delete()
                for error in errors:
                    messages.info(request, error)

            return redirect("outside_eddi:data_files")

    else:
        form = TestHistoryFileUploadForm()

    context['form'] = form
    context['file_info_data'] = OutsideEddiFileInfo.objects.filter(user=user).order_by("-created")

    return render(request, template, context)

@outside_eddi_login_required(login_url='outside_eddi:login')
def delete_data_file(request, file_id, context=None):
    context = context or {}

    f = OutsideEddiFileInfo.objects.get(pk=file_id)
    subjects = f.subjects.all().delete()
    import pdb;pdb.set_trace()
    
    f.delete()
    messages.info(request, 'File deleted')
    return redirect(reverse('outside_eddi:data_files'))

@outside_eddi_login_required(login_url='outside_eddi:login')
def save_data_file(request, file_id, context=None):
    context = context or {}

    user = request.user
    
    f = OutsideEddiFileInfo.objects.get(pk=file_id)
    mapping_needed = OutsideEddiFileHandler(f).save_data(user)

    if f.message:
        messages.info(request, f.message)
        f.state = 'error'
        f.save()
    elif mapping_needed:
        f.state = 'needs_mapping'
        f.save()
        for mapping in mapping_needed:
            messages.info(request, mapping)
    else:
        messages.info(request, 'Data Saved')
        f.state = 'mapped'
        f.save()
    return redirect(reverse('outside_eddi:data_files'))

@outside_eddi_login_required(login_url='outside_eddi:login')
def process_data_file(request, file_id, context=None):
    context = context or {}

    return redirect(reverse('outside_eddi:data_files'))

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


    global_formset = GlobalTestFormSet(
        request.POST or None,
        queryset=OutsideEddiDiagnosticTest.objects.filter(user=None),
        prefix='global'
    )
    user_formset = UserTestFormSet(
        request.POST or None,
        queryset=OutsideEddiDiagnosticTest.objects.filter(user=user),
        prefix='user'
    )

    test_ids_by_name = {}
    all_tests = OutsideEddiDiagnosticTest.objects.filter(Q(user=user) | Q(user=None))
    for test in all_tests:
        test_ids_by_name[str(test.name)] = test.id

    test_names = []
    for test in all_tests:
        test_names.append(test.name)

    names = json.dumps(test_ids_by_name)

    tests = OutsideEddiDiagnosticTest.objects.all()

    if request.method == 'POST':
        if user_formset.is_valid():
            for form in user_formset.forms:
                if form.cleaned_data:
                    if form.instance.pk:
                        f = form.save(commit=False)
                        f.user = user
                        f.save()
                    else:
                        if OutsideEddiDiagnosticTest.objects.filter(name=form.cleaned_data['name'],
                                                              user=user).exists():
                            messages.add_message(request, messages.WARNING, "You already have a test with the name: " + form.cleaned_data['name'])
                        else:
                            f = form.save(commit=False)
                            f.user = user
                            f.save()

            return redirect("outside_eddi:tests")

        else:
            messages.add_message(request, messages.WARNING, "Invalid test details")
            return redirect("outside_eddi:tests")

    context['user_formset'] = user_formset
    context['global_formset'] = global_formset
    context['tests'] = tests
    context['test_ids_by_name'] = names

    return render(request, template, context)

@outside_eddi_login_required(login_url='outside_eddi:login')
def test_mapping(request, file_id=None, template="outside_eddi/test_mapping.html"):
    context = {}

    user = request.user

    data_file = None
    if file_id != 'None':
        data_file = OutsideEddiFileInfo.objects.get(pk=file_id)
        codes = [x.test_code for x in data_file.subjects.all()]
        formset = DataFileTestPropertyMappingFormSet(request.POST or None,
                                             queryset=TestPropertyMapping.objects.filter(code__in=codes, user=user))
    else:
        formset = TestPropertyMappingFormSet(request.POST or None,
                                             queryset=TestPropertyMapping.objects.filter(user=user))

    for form in formset:
        form.fields['test'].queryset = OutsideEddiDiagnosticTest.objects.filter(Q(user=user) | Q(user=None)).order_by('-user')

    tooltips_for_tests = {}
    tests = OutsideEddiDiagnosticTest.objects.all()
    for test in tests:
        tooltips_for_tests[str(test.pk)] = test.description

    tips = json.dumps(tooltips_for_tests)

    if request.method == 'POST':
        if formset.is_valid():
            for form in formset.forms:
                if form.cleaned_data:
                    if form.instance.pk:
                        f = form.save(commit=False)
                        f.user = user
                        code = f.code
                        set_property = TestPropertyMapping.objects.filter(code=code, user=user).first()
                        if set_property:
                            f.test_property = set_property.test_property
                        f.save()
                    else:
                        if TestPropertyMapping.objects.filter(code=form.cleaned_data['code'],
                                                              user=user).exists():
                            messages.add_message(request, messages.WARNING, "You already have a mapping with code: " + form.cleaned_data['code'])
                        else:
                            f = form.save(commit=False)
                            f.user = user
                            code = f.code
                            set_property = TestPropertyMapping.objects.filter(code=code, user=user).first()
                            if set_property:
                                f.test_property = set_property.test_property
                            f.save()
            if file_id == 'None':
                return redirect("outside_eddi:test_mapping", file_id)
            else:
                mappings = TestPropertyMapping.objects.filter(code__in=codes, user=user)
                redirect_page = True
                for mapping in mappings:
                    if mapping.test_property:
                        continue
                    else:
                        redirect_page = False
                        messages.add_message(request, messages.WARNING, "Please provide a property for " + mapping.code)
                if redirect_page == True:
                    data_file.state = 'mapped'
                    data_file.save()
                    return redirect("outside_eddi:data_files")
                else:
                    return redirect("outside_eddi:test_mapping", file_id)    

        else:
            messages.add_message(request, messages.WARNING, "Invalid mapping")

    context['formset'] = formset
    context['tooltips_for_tests'] = tips
    context['file'] = data_file

    return render(request, template, context)

@outside_eddi_login_required(login_url='outside_eddi:login')
def test_properties(request, code=None, details=None, test_id=None, file_id=None, template="outside_eddi/test_properties.html", context=None):
    context = context or {}

    user = request.user

    if code == 'new_user_test':
        test = OutsideEddiDiagnosticTest.objects.create(name=test_id, user=user)
        if details != 'no_user_details':
            test.description = details
            test.save()
        test_id = test.pk
        code = 'user'
    else:
        test = OutsideEddiDiagnosticTest.objects.get(pk=test_id)
        if code == 'user' and test.description != details and details != 'no_user_details':
            test.description = details
            test.save()

    active_property = None

    if code != 'None' and code != 'user' and code != 'global':
        if TestPropertyMapping.objects.filter(code=code, user=user, test=test).exists():
            user_map = TestPropertyMapping.objects.filter(code=code, user=user, test=test).first()
        elif TestPropertyMapping.objects.filter(code=code, user=user).exists():
            user_map = TestPropertyMapping.objects.filter(code=code, user=user).first()
            user_map.test = test
            user_map.test_property = None
            user_map.save()
        else:
            user_map = TestPropertyMapping.objects.create(code=code, user=user, test=test)

        if user_map.test_property:
            active_property = user_map.test_property
        else:
            test_properties = user_map.test.properties.all()
            for prop in test_properties:
                if prop.is_default == True:
                    active_property = prop

        properties = OutsideEddiTestPropertyEstimate.objects.filter(test=test)

        for prop in properties:
            prop.active_property = False
            prop.save()

        if active_property != None:
            active_property.active_property = True
            active_property.save()

    else:
        properties = OutsideEddiTestPropertyEstimate.objects.filter(test=test)
        for prop in properties:
            prop.active_property = False
            if prop.is_default == True:
                prop.active_property = True
            prop.save()

    formset = TestPropertyEstimateFormSet(
        request.POST or None,
        queryset=OutsideEddiTestPropertyEstimate.objects.filter(Q(user=user) | Q(user=None),
        test__pk=test_id))

    if code == 'global':
        for form in formset:
            form.fields['active_property'].widget.attrs['disabled'] = True

    if request.method == 'POST':
        if formset.is_valid():
            active_exists = False
            for form in formset.forms:
                if form.cleaned_data:
                    if form.cleaned_data['active_property'] == True:
                        active_exists = True

            for form in formset.forms:
                if form.cleaned_data:
                    i = str(form.instance)
                    if i == 'None':
                        f = form.save(commit=False)
                        f.test = test
                        f.user = user
                        if active_exists == False:
                            f.active_property=True
                            if code == 'user':
                                f.is_default = True
                        f.save()
                        if f.active_property==True:
                            active = f
                    elif form.instance.user == user:
                        f = form.save(commit=False)
                        f.test = test
                        f.user = user
                        f.save()
                        if f.active_property==True:
                            active = f
                            if code == 'user':
                                f.is_default = True
                    else:
                        f = form.save()
                        if f.active_property==True:
                            active = f

            if code != 'None' or code != 'user' or code != 'global':
                user_map = TestPropertyMapping.objects.filter(code=code, user=user, test=test).first()
                if user_map:
                    user_map.test_property = active
                    user_map.save()
                else:
                    user_map_code_only = TestPropertyMapping.objects.filter(code=code, user=user).first()
                    if user_map_code_only:
                        user_map_code_only.test = test
                        user_map_code_only.test_property = active
                        user_map_code_only.save()
                    else:
                        new_map = TestPropertyMapping.objects.create(code=code, user=user, test=test, test_property=active)

                if request.is_ajax():
                    return JsonResponse({"success": True})
                else:
                    return redirect("outside_eddi:test_mapping", file_id)

            else:
                if request.is_ajax():
                    return JsonResponse({"success": True})
                else:
                    return redirect("outside_eddi:tests")
        else:

            if request.is_ajax():
                context['formset'] = formset
                context['test'] = test
                context['code'] = code
                context['details'] = details
                context['file'] = file_id
                return render(request, 'outside_eddi/test_properties.html', context)
            else:
                messages.add_message(request, messages.WARNING, "Invalid properties")
                return redirect("outside_eddi:test_mapping")

    context['formset'] = formset
    context['test'] = test
    context['code'] = code
    context['details'] = details
    context['file'] = file_id

    return render(request, template, context)

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
