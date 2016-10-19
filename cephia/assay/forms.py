from django import forms
from cephia.models import FileInfo, Panel, Laboratory, Assay
from models import AssayRun
import unicodecsv as csv
from cephia.excel_helper import ExcelHelper
import os
from assay_result_factory import get_result_model, ResultDownload
from cephia.csv_helper import get_csv_response
from assay.models import AssayResult
from datetime import datetime


class PanelCaptureForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['name','description', 'specimen_type', 'volume']

    def __init__(self, *args, **kwargs):
        super(PanelCaptureForm, self).__init__(*args, **kwargs)


class PanelFileForm(forms.ModelForm):
    class Meta:
        model = FileInfo
        fields = ['data_file','file_type', 'priority', 'panel']
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

class AssaysByVisitForm(forms.Form):
    visit_file = forms.FileField(required=True, label='Visit id file')
    assays = forms.ModelMultipleChoiceField(required=False, queryset=Assay.objects.all().order_by('name'), label='Which assays?')

    def clean_visit_file(self):
        visit_file = self.cleaned_data['visit_file']
        filename = visit_file.name
        extension = os.path.splitext(filename)[1][1:].lower()
        if extension == 'csv':
            rows = (z[0] for z in csv.reader(visit_file) if z)
        elif extension in ['xls', 'xlsx']:
            rows = (z[0] for z in ExcelHelper(visit_file).rows() if z)
        else:
            raise forms.ValidationError('Unsupported file uploaded: Only CSV and Excel are allowed.')
        self.cleaned_data['visit_ids'] = [r for r in rows if r.isdigit()]
        return visit_file

    def get_csv_response(self):
        assays = self.cleaned_data['assays']
        headers = []
        result_models = [get_result_model(assay.name) for assay in assays]
        results = AssayResult.objects.filter(assay_run__assay__in=assays)
        download = ResultDownload(headers, results, 'detailed', result_models)

        response, writer = get_csv_response('detailed_results_%s.csv' % (
            datetime.today().strftime('%d%b%Y_%H%M')))

        writer.writerow(download.get_headers())

        for row in download.get_content():
            writer.writerow(row)
        return response


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
            
