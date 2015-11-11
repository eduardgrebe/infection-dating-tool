from django.forms import *
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple

class UserEditForm(ModelForm):

    password = CharField(widget=PasswordInput, required=False, label="Password (leave blank to keep previous password)")
    verify_password = CharField(widget=PasswordInput, required=False)
    force_unlock = BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields=["username", "first_name", "last_name", "email", "password", "verify_password", "is_superuser",
                "is_active", 'force_unlock', 'groups']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        if self.instance and not self.instance.temporary_locked_out_at:
            del self.fields['force_unlock']

        self.fields['is_superuser'].help_text = ""
        self.fields['is_active'].help_text = ""

        self.fields['groups'].widget = CheckboxSelectMultiple( choices=[ (x.id, x.name) for x in Group.objects.all().order_by("name") ] )
        self.fields['groups'].help_text = ""

        self.fields['username'].help_text = ""

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

class UserProfileForm(ModelForm):

    password = CharField(widget=PasswordInput, required=False, label="Password (leave blank to keep previous password)")
    verify_password = CharField(widget=PasswordInput, required=False)

    class Meta:
        model = get_user_model()
        fields=["first_name", "last_name", "email", "password", "verify_password"]

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

    def save(self):
        user = super(UserProfileForm, self).save()
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user

class GroupEditForm(ModelForm):
    class Meta:
        model = Group
        exclude = ['name']

    def __init__(self, *args, **kwargs):
        super(GroupEditForm, self).__init__(*args, **kwargs)

        permissions = Permission.objects.all().exclude(name__contains="Can add").exclude(name__contains="Can delete").exclude(name__contains="Can change").order_by("name")

        self.fields['permissions'].widget = CheckboxSelectMultiple( choices=[ (x.id, x.name) for x in permissions ] )
        self.fields['permissions'].help_text = ""

    def save(self, *args, **kwargs):
        group = super(GroupEditForm, self).save(*args, **kwargs)

        if kwargs.get('commit', True):
           group.save()

        return group


class ActivateUserForm(Form):
    password1 = CharField(required=True)
    password2 = CharField(required=True)

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise ValidationError("The passwords entered do not match")
        return self.cleaned_data

    def save(self, user):
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.activation_key = None
        user.activation_key_expires_at = None
        user.save()
        return user
