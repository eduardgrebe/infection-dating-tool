from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from forms import EddiUserCreationForm, TestHistoryFileUploadForm, StudyForm, TestPropertyMappingForm, TestPropertyForm
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
from file_handlers.outside_eddi_test_history_file_handler import TestHistoryFileHandler
from cephia.models import FileInfo, CephiaUser
from models import Study, OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate, TestPropertyMapping
from diagnostics.models import DiagnosticTest, TestPropertyEstimate
from django.forms import modelformset_factory

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
            if tests:
                test_properties = _copy_test_properties(user)
            else:
                add_tests = _copy_diagnostic_tests()
                test_properties = _copy_test_properties(user)

            return redirect("outside_eddi:home")
        else:
            messages.add_message(request, messages.WARNING, "Invalid credentials")
            _check_for_login_hack_attempt(request, context)

    context['form'] = form

    return render(request, template, context)


@outside_eddi_login_required(login_url='outside_eddi:login')
def diagnostic_tests(request, file_id=None, template="outside_eddi/diagnostic_tests.html"):
    context = {}

    if request.method == 'POST':
        form = TestHistoryFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            messages.info(request, u"Your file was uploaded successfully" )
            latest_file = FileInfo.objects.filter(data_file=uploaded_file).last()
            
            TestHistoryFileHandler(uploaded_file).parse()
            messages.info(request, u"Your file was parsed successfully" )
            TestHistoryFileHandler(uploaded_file).validate()
            messages.info(request, u"Your file was validated successfully" )
            TestHistoryFileHandler(uploaded_file).process()
            messages.info(request, u"Your file was processed successfully" )
            
            return redirect("outside_eddi:diagnostic_tests")

    else:
        form = TestHistoryFileUploadForm()

    context['form'] = form

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

    tests = OutsideEddiDiagnosticTest.objects.all()
    context['tests'] = tests

    return render(request, template, context)

@outside_eddi_login_required(login_url='outside_eddi:login')
def test_mapping(request, file_id=None, template="outside_eddi/test_mapping.html"):
    context = {}

    user = request.user
    
    TestPropertyMappingFormSet = modelformset_factory(TestPropertyMapping, exclude=('user',))
    formset = TestPropertyMappingFormSet(request.POST or None,
                                         queryset=TestPropertyMapping.objects.filter(user=user))


    if request.method == 'POST':
        if formset.is_valid():
            for form in formset.forms:
                if form.cleaned_data:
                    f = form.save(commit=False)
                    f.user = user
                    code = f.code
                    set_property = TestPropertyMapping.objects.filter(code=code, user=user).first()
                    if set_property:
                        f.test_property = set_property.test_property
                    f.save()

            return redirect("outside_eddi:test_mapping")
        else:
            messages.add_message(request, messages.WARNING, "Invalid mapping")
    
    context['formset'] = formset
    
    return render(request, template, context)

@outside_eddi_login_required(login_url='outside_eddi:login')
def test_properties(request, code=None, test_id=None, file_id=None, template="outside_eddi/test_properties.html", context=None):
    context = context or {}

    user = request.user
    test = OutsideEddiDiagnosticTest.objects.get(pk=test_id)

    TestPropertyEstimateFormSet = modelformset_factory(OutsideEddiTestPropertyEstimate,
                                                       fields=('active_property', 'estimate_label', 'mean_diagnostic_delay_days', 'foursigma_diagnostic_delay_days', 'diagnostic_delay_median', 'comment', 'reference'),
                                                       exclude=('user', 'history', 'test', 'name', 'estimate_type', 'variance', 'time0_ref', 'description', 'is_default'))
    formset = TestPropertyEstimateFormSet(request.POST or None,
                                         queryset=OutsideEddiTestPropertyEstimate.objects.filter(user=user, test__pk=test_id))

    if request.method == 'POST':
        if formset.is_valid():
            for form in formset.forms:
                if form.cleaned_data:
                    f = form.save(commit=False)
                    f.user = user
                    f.test = test
                    f.save()
                    if f.active_property==True:
                        active = f

            set_code_property = TestPropertyMapping.objects.filter(code=code, user=user).first()
            if set_code_property:
                set_code_property.test_property=active
                set_code_property.save()
            return redirect("outside_eddi:test_mapping")
        else:
            messages.add_message(request, messages.WARNING, "Invalid properties")
            return redirect("outside_eddi:test_mapping")

    context['formset'] = formset
    context['test'] = test
    context['code'] = code
    
    return render(request, template, context)

def _copy_diagnostic_tests():
    
    tests = DiagnosticTest.objects.all()

    for test in tests:
        outside_eddi_test = OutsideEddiDiagnosticTest.objects.create(id = test.id,
                                                                     name = test.name,
                                                                     description = test.description)

def _copy_test_properties(user):

    test_properties = TestPropertyEstimate.objects.all()

    for prop in test_properties:
        test_name = prop.test.name
        test = OutsideEddiDiagnosticTest.objects.filter(name=test_name).first()

        outside_eddi_test_property = OutsideEddiTestPropertyEstimate.objects.create(user=user,
                                                                                    test = test,
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
