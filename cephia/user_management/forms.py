from django.forms import *
#from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from api.forms import ApiPostForm


class LoginForm(Form):

    username = CharField(required=True, label="Username")
    password = CharField(widget=PasswordInput, required=True, label="Password")


class UserEditForm(ApiPostForm):
    username = CharField(required=False)
    password = CharField(widget=PasswordInput, required=False, label="Password (leave blank to keep previous password)")
    verify_password = CharField(widget=PasswordInput, required=False)
    force_unlock = BooleanField(required=False)
    is_superuser = BooleanField(required=False)
    is_active = BooleanField(required=False)
    lead_facilitator = ChoiceField(required=False, choices=[])


    def __init__(self, lead_facilitator, *args, **kwargs):
        kwargs.pop('extra_context')
        super(UserEditForm, self).__init__(*args, **kwargs)
        if self.initial and not self.initial['temporary_locked_out_at']:
            del self.fields['force_unlock']

        self.fields['lead_facilitator'].choices = [ (None, "") ] + [ ( x['id'], x['name'] ) for x in lead_facilitator ]
        
    def clean(self):
        data = super(UserEditForm, self).clean()

        if 'password' in data and ('verify_password' not in data or data['password'] != data['verify_password']):
            self._errors['password'] = self.error_class(["Passwords don't match"])
            self._errors['verify_password'] = self.error_class(["Passwords don't match"])
            raise ValidationError("Passwords don't match")

        if 'password' in data and not data['password']:
            del data['password']

        return data

    def save(self):
        user = super(UserEditForm, self).save()
        if self.cleaned_data.get('force_unlock'):
            user.login_ok()
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user

class HRUserEditForm(UserEditForm):
    is_superuser = None

class UserProfileForm(ApiPostForm):

    first_name = CharField(required=False)
    last_name = CharField(required=False)
    email = CharField(required=False)
    password = CharField(widget=PasswordInput, required=False, label="Password (leave blank to keep previous password)")
    verify_password = CharField(widget=PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(UserProfileForm, self).clean()

        if 'password' in data and ('verify_password' not in data or data['password'] != data['verify_password']):
            self._errors['password'] = self.error_class(["Passwords don't match"])
            self._errors['verify_password'] = self.error_class(["Passwords don't match"])
            raise ValidationError("Passwords don't match")

        if 'password' in data and not data['password']:
            del data['password']

        return data

class GroupEditForm(ApiPostForm):
    # class Meta:
    #     model = Group

    #allowed_statuses = ModelMultipleChoiceField(queryset=LoanApplicationStatus.objects.all(), required=False)
    allowed_statuses = MultipleChoiceField(required=False)
    #allowed_landing_pages = ModelMultipleChoiceField(queryset=LandingPage.objects.all(), required=False)
    allowed_landing_pages = MultipleChoiceField(required=False)
    permissions = MultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        kwargs.pop('extra_context')
        if 'permissions' in kwargs:
            permissions = kwargs.pop('permissions')
            
        if 'allowed_statuses' in kwargs:
            allowed_statuses = kwargs.pop('allowed_statuses')

        if 'allowed_landing_pages' in kwargs:
            allowed_landing_pages = kwargs.pop('allowed_landing_pages')

        super(GroupEditForm, self).__init__(*args, **kwargs)

#        permissions = Permission.objects.all().exclude(name__contains="Can add").exclude(name__contains="Can delete").exclude(name__contains="Can change").order_by("name")

        # TODO why do we need to set the choices on the widget and the field?
        permission_choices = [ (p['id'], p['name']) for p in permissions ]
        self.fields['permissions'].widget = CheckboxSelectMultiple( choices=permission_choices )
        self.fields['permissions'].choices = permission_choices

        allowed_status_choices = [ (s['id'], s['name']) for s in allowed_statuses ]
        self.fields['allowed_statuses'].widget = CheckboxSelectMultiple( choices=allowed_status_choices )
        self.fields['allowed_statuses'].choices = allowed_status_choices

        allowed_landing_page_choices = [ (l['id'], l['name']) for l in allowed_landing_pages ]
        self.fields['allowed_landing_pages'].widget = CheckboxSelectMultiple( choices=allowed_landing_page_choices )
        self.fields['allowed_landing_pages'].choices = allowed_landing_page_choices

        # allowed_statuses = LoanApplicationStatus.objects.all().order_by("name")
        # self.fields['allowed_statuses'].initial = self.instance.allowed_statuses.all()
        # self.fields['allowed_statuses'].widget = CheckboxSelectMultiple( choices=[ (x.id, x.name) for x in allowed_statuses ] )
        # self.fields['allowed_statuses'].help_text = ""

        # allowed_landing_pages = LandingPage.objects.all().order_by("name")
        # self.fields['allowed_landing_pages'].initial = self.instance.allowed_landing_pages.all()
        # self.fields['allowed_landing_pages'].widget = CheckboxSelectMultiple( choices=[ (x.id, x.name) for x in allowed_landing_pages ] )
        # self.fields['allowed_landing_pages'].help_text = ""

    def save(self, *args, **kwargs):
        group = super(GroupEditForm, self).save(*args, **kwargs)

        for allowed_status in group.allowed_statuses.all():
            if allowed_status not in self.cleaned_data['allowed_statuses']:
                instance.allowed_statuses.remove(allowed_status)
        for allowed_status in self.cleaned_data['allowed_statuses']:
            if allowed_status not in group.allowed_statuses.all():
                group.allowed_statuses.add(allowed_status)

        for allowed_landing_page in group.allowed_landing_pages.all():
            if allowed_landing_page not in self.cleaned_data['allowed_landing_pages']:
                instance.allowed_landing_pages.remove(allowed_landing_page)
        for allowed_landing_page in self.cleaned_data['allowed_landing_pages']:
            if allowed_landing_page not in group.allowed_landing_pages.all():
                group.allowed_landing_pages.add(allowed_landing_page)

        if kwargs.get('commit', True):
           group.save()

        return group

class ActivateUserForm(ApiPostForm):
    password1 = CharField(required=True, label='Enter your password', widget=PasswordInput())
    password2 = CharField(required=True, label='Re-Enter your password', widget=PasswordInput())

    
        
