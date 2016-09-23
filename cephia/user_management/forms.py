from django.forms import *
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission, User
from django.contrib.admin.widgets import FilteredSelectMultiple

class PermissionChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, instance):
        return instance.name


class UserEditForm(ModelForm):

    password = CharField(widget=PasswordInput, required=False, label="Password (leave blank to keep previous password)")
    verify_password = CharField(widget=PasswordInput, required=False)
    force_unlock = BooleanField(required=False)
    user_permissions = PermissionChoiceField(
        widget=CheckboxSelectMultiple(),
        required=False,
        queryset=Permission.objects.filter(content_type__app_label='cephia', content_type__model='CephiaUser', name__icontains='upload'), label='Permissions')

    class Meta:
        model = get_user_model()
        fields=["username", "first_name", "last_name", "email", "password", "verify_password", "is_superuser",
                "is_active", 'is_staff', 'force_unlock', 'user_permissions']

    def label_from_instance(self, instance):
        return instance.name

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        if self.instance and not self.instance.temporary_locked_out_at:
            del self.fields['force_unlock']

        self.fields['is_superuser'].help_text = ""
        self.fields['is_active'].help_text = ""

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

class UserCreationForm(ModelForm):
    username = CharField(widget=TextInput(attrs={'placeholder': 'Username'}), label=None)
    email = CharField(widget=TextInput(attrs={'placeholder': 'Email'}), label=None)
    
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password = CharField(label=("Password"),
                                widget=PasswordInput(attrs={'placeholder': 'Password'}))
    verify_password = CharField(label=("Password confirmation"),
                                widget=PasswordInput(attrs={'placeholder': 'Confirm Password'}),
                                help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password", "verify_password", "is_active", 'user_permissions']

    def clean_verify_password(self):
        password = self.cleaned_data.get("password")
        verify_password = self.cleaned_data.get("verify_password")
        if password and verify_password and password != verify_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return verify_password

class EddiUserCreationForm(UserCreationForm):
    
    def save(self, commit=True):
        
        user = super(EddiUserCreationForm, self).save(True)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.save()
        outside_eddi_group = Group.objects.get(name='Outside Eddi Users')
        outside_eddi_group.user_set.add(user)
        return user
