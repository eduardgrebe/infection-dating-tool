from django import forms
from cephia.models import FileInfo, Panel, Laboratory, Assay
from models import AssayRun

class PanelCaptureForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['name','description', 'specimen_type', 'volume']

    def __init__(self, *args, **kwargs):
        super(PanelCaptureForm, self).__init__(*args, **kwargs)


class PanelFileForm(forms.ModelForm):
    class Meta:
        model = FileInfo
        fields = ['data_file','file_type', 'priority', 'panel', 'specimen_label_type']
        widgets = {
            'data_file': forms.FileInput(attrs={'accept':'.xls, .xlsx, .csv'}),
            'priority':forms.HiddenInput(),
            'file_type':forms.HiddenInput(),
            'panel':forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PanelFileForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

class AssayRunFilterForm(forms.Form):

    panel = forms.ChoiceField(required=False)
    assay = forms.ChoiceField(required=False)
    laboratory = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(AssayRunFilterForm, self).__init__(*args, **kwargs)

        lab_choices = [('','---------')]
        [ lab_choices.append((x.id, x.name)) for x in Laboratory.objects.all() ]
        self.fields['laboratory'].choices = lab_choices

        assay_choices = [('','---------')]
        [ assay_choices.append((x.id, x.name)) for x in Assay.objects.all() ]
        self.fields['assay'].choices = assay_choices

        panel_choices = [('','---------')]
        [ panel_choices.append((x.id, x.name)) for x in Panel.objects.all() ]
        self.fields['panel'].choices = panel_choices

    def filter(self):
        qs = AssayRun.objects.all()
        panel = self.cleaned_data['panel']
        assay = self.cleaned_data['assay']
        laboratory = self.cleaned_data['laboratory']

        if panel:
            qs = qs.filter(panel__id=panel)
        if assay:
            qs = qs.filter(assay__id=assay)
        if laboratory:
            qs = qs.filter(laboratory__id=laboratory)

        return qs

class AssayRunResultsFilterForm(forms.Form):
    specimen_label = forms.CharField(required=False)

    def filter(self, qs):
        if self.cleaned_data.get('specimen_label'):
            qs = qs.filter(specimen__specimen_label__icontains=self.cleaned_data.get('specimen_label')).distinct()
        return qs
            
