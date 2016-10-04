from user_management.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from cephia.models import FileInfo
from models import UserStudies

class EddiUserCreationForm(UserCreationForm):
    
    def save(self, commit=True):
        
        user = super(EddiUserCreationForm, self).save(True)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.save()
        outside_eddi_group = Group.objects.get(name='Outside Eddi Users')
        outside_eddi_group.user_set.add(user)
        return user

class TestHistoryFileUploadForm(ModelForm):
    class Meta:
        model = FileInfo
        fields = ['data_file']

class UserStudiesForm(ModelForm):
    class Meta:
        model = UserStudies
        fields = ['name']
