from user_management.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from cephia.models import FileInfo

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
    
# class TestHistoryForm(forms.Form):
#     subject_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Subject ID'}), label=None)
#     test_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Test Code'}), label=None)
#     test_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class':'datepicker', 'placeholder': 'Test Date'}))
#     test_result = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Test Result'}), label=None)
#     test_source = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Test Source'}), label=None)
#     protocol = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Protocol'}), label=None)

#     # def __init__(self, *args, **kwargs):
#     #     super(TestHistoryForm, self).__init__(self, *args, **kwargs)
#     #     self.fields['test_date'].widget = forms.DateInput()
#     #     self.fields['test_date'].widget.attrs.update({'class':'datepicker'})

#     def save(self, commit=True):
#         import pdb;pdb.set_trace()
