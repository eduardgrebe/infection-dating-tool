from django import forms
from cephia.models import FileInfo, Panel, Laboratory, Assay, Visit, Specimen
from models import AssayRun
import unicodecsv as csv
from cephia.excel_helper import ExcelHelper
import os
from assay_result_factory import get_result_model, ResultDownload
from cephia.csv_helper import get_csv_response
from assay.models import AssayResult
from datetime import datetime
from django.conf import settings
from django.db.models import Q
from django.db.models import Prefetch
from django.db.models.functions import Concat


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
    visit_file = forms.FileField(required=False, label='Upload a list of visit IDs')
    visit_ids = forms.CharField(required=False, widget=forms.Textarea(), label='Or enter a newline-separated list of visit IDs')
    specimen_file = forms.FileField(required=False, label='Upload a list of specimen labels')
    specimen_labels = forms.CharField(required=False, widget=forms.Textarea(), label='Or enter a newline-separated list of specimen labels')
    by_visit_assays = forms.ModelMultipleChoiceField(required=False, queryset=Assay.objects.all().order_by('name'), label='Which assays?')
    panels = forms.ModelMultipleChoiceField(required=False, queryset=Panel.objects.all().order_by('name'), label='Restrict export to panels:')
    result_output = forms.ChoiceField(required=True, choices=((1, 'detailed'), (2, 'generic')), initial='detailed', label='Select generic or detailed')

    def clean_specimen_file(self):
        specimen_file = self.cleaned_data.get('specimen_file')
        if not specimen_file:
            return specimen_file
        filename = specimen_file.name
        extension = os.path.splitext(filename)[1][1:].lower()
        if extension == 'csv':
            rows = [z[0] for z in csv.reader(specimen_file) if z]
        elif extension in ['xls', 'xlsx']:
            rows = list(z[0] for z in ExcelHelper(specimen_file).rows() if z)
        else:
            raise forms.ValidationError('Unsupported file uploaded: Only CSV and Excel are allowed.')

        self.cleaned_data['imported_specimen_labels'] = rows
        return rows


    def clean_specimen_labels(self):
        value = self.cleaned_data.get('specimen_labels')
        if not value:
            return value
        rows = [z.strip() for z in value.split(u'\n')]
        self.cleaned_data['imported_specimen_labels'] = rows
        return value


    def clean_visit_file(self):
        visit_file = self.cleaned_data.get('visit_file')
        if not visit_file:
            return visit_file
        filename = visit_file.name
        extension = os.path.splitext(filename)[1][1:].lower()
        if extension == 'csv':
            rows = (int(z[0]) for z in csv.reader(visit_file) if z)
        elif extension in ['xls', 'xlsx']:
            rows = (int(z[0]) for z in ExcelHelper(visit_file).rows() if z)
        else:
            raise forms.ValidationError('Unsupported file uploaded: Only CSV and Excel are allowed.')
        self.cleaned_data['imported_visit_ids'] = [r for r in rows if r.isdigit()]
        return visit_file


    def clean_visit_ids(self):
        value = self.cleaned_data.get('visit_ids')
        if not value:
            return value
        rows = [int(z.strip()) for z in value.split(u'\n')]
        self.cleaned_data['imported_visit_ids'] = rows
        return value


    def clean(self):
        if self.cleaned_data.get('specimen_file') and self.cleaned_data.get('specimen_labels'):
            raise forms.ValidationError('Options are bexclusive, please complete only one.')
        if self.cleaned_data.get('visit_file') and self.cleaned_data.get('visit_ids'):
            raise forms.ValidationError('Options are bexclusive, please complete only one.')

        return self.cleaned_data


    def get_csv_response(self):
        headers = []
        assays = self.cleaned_data['by_visit_assays']
        specimen_labels = self.cleaned_data.get('imported_specimen_labels')
        visit_ids = self.cleaned_data.get('imported_visit_ids')
        panels = self.cleaned_data.get('panels')
        result_models = None
        results = AssayResult.objects.all()

        if visit_ids and specimen_labels:
            specimen_visit_ids = Visit.objects.filter(specimens__specimen_label__in=specimen_labels)
            specimen_visit_ids = list(specimen_visit_ids.values_list('pk', flat=True).distinct())

            results = results.filter(
                specimen__visit__pk__in=visit_ids + specimen_visit_ids,
            ).distinct()
        elif visit_ids:
            results = results.filter(specimen__visit__pk__in=visit_ids).distinct()
        elif specimen_labels:
            results = results.filter(specimen__visit__specimens__specimen_label__in=specimen_labels).distinct()

        # visits_left_joined_to_results = Visit.objects.prefetch_related(Prefetch('assay_results'))
        # visits = visits.extra("VR = concat(visit.id, results.id)")
        # visits = visits.extra(select={'VR' : Concat('visit.id', 'specimen.assay_results.id')})
        # visits_left_joined_to_results = visits_left_joined_to_results.distinct('VR')
        
        # ### gtp
 
        # Select visit.id, visit.name, results.id, results.date
        #      from visit
        #      LEFT JOIN specimen as specimen_alias where speciman.visit_id=visit.id
        #      LEFT JOIN results where results.visit_id = visit.id
        #      where (visit.id IN [1,2,3]) OR (speciman_alias.specimen_label IN [3,2,1])

        #      where (visit.id IN [1,2,3]) OR (visit.id IN (select visit_id from specimen where label in [3,2,1])

        # select * from visit
        # left join results

        # specimen_visits = Visit.objects.filter(specimens__specimen_label__in=specimen_labels))
                                             
        # visits = Visit.objects.filter( Q(pk__in=visit_ids) | Q(pk_in=specimen_visits))

        # #  Q(specimens__specimen_label__in=specimen_labels) )
        # visits_left_joined_to_results = prefetch_related('results')
        # visits = visits.extra("VR = concat(visit.id, results.id)")
        # visits_left_joined_to_results = visits_left_joined_to_results.distinct('VR')
        # print visits_left_joined_to_results.queryset.sql()

        # for visit_result in visits_left_joined_to_results:
        #     print(visit_result)
        #

        # CSV
        # Visit.objects.all().values_list('id', 'name', 'date', 'specimen__type', flat=True)
        # [ {'id':1, 'name':'bob'}, {}, {} ]

        # select count('id') from cephia_results;
        
        # ### end gtp
        
        

        # if specimen_labels:
        #     specimen_visits = Visit.objects.filter(specimens__specimen_label__in=specimen_labels)
        #     results = results.filter(specimen__in=specimens)

        if assays:
            results = results.filter(assay_run__assay__in=assays)

        if panels:
            results = results.filter(specimen__visit__panels__in=panels)

        if self.cleaned_data['result_output'] == '1':
            if not assays:
                assays = results.values('assay').distinct()
                assays = Assay.objects.filter(pk__in=assays)

            result_models = [ get_result_model(assay.name) for assay in assays if get_result_model(assay.name) ]
            download = ResultDownload(headers, results, False, result_models, filter_by_visit=True)

            response, writer = get_csv_response('detailed_results_%s.csv' % (
            datetime.today().strftime('%d%b%Y_%H%M')))
        else:
            download = ResultDownload(headers, results, True, result_models, filter_by_visit=True)

            response, writer = get_csv_response('generic_results_%s.csv' % (
            datetime.today().strftime('%d%b%Y_%H%M')))

        if visit_ids:
            download.add_extra_visits(visit_ids)

        if specimen_labels:
            download.add_extra_specimens(specimen_labels)

        writer.writerow(download.get_headers())

        for row in download.get_content():
            writer.writerow(row)
        return response

    def preview_filter(self):
        headers = []
        assays = self.cleaned_data['by_visit_assays']
        specimen_labels = self.cleaned_data.get('imported_specimen_labels')
        visit_ids = self.cleaned_data.get('imported_visit_ids')
        panels = self.cleaned_data.get('panels')
        result_models = None
        results = AssayResult.objects.all()

        if visit_ids and specimen_labels:
            specimen_visit_ids = Visit.objects.filter(specimens__specimen_label__in=specimen_labels)
            specimen_visit_ids = list(specimen_visit_ids.values_list('pk', flat=True).distinct())

            results = results.filter(
                specimen__visit__pk__in=visit_ids + specimen_visit_ids,
            ).distinct()
        elif visit_ids:
            results = results.filter(specimen__visit__pk__in=visit_ids).distinct()
        elif specimen_labels:
            results = results.filter(specimen__visit__specimens__specimen_label__in=specimen_labels).distinct()

        if assays:
            results = results.filter(assay_run__assay__in=assays)

        if panels:
            results = results.filter(specimen__visit__panels__in=panels)

        if self.cleaned_data['result_output'] == '1':
            if not assays:
                assays = results.values('assay').distinct()
                assays = Assay.objects.filter(pk__in=assays)

            result_models = [ get_result_model(assay.name) for assay in assays if get_result_model(assay.name) ]
            download = ResultDownload(headers, results, False, result_models, 25, filter_by_visit=True)
        else:
            download = ResultDownload(headers, results, True, result_models, 25, filter_by_visit=True)

        if visit_ids:
            download.add_extra_visits(visit_ids)

        if specimen_labels:
            download.add_extra_specimens(specimen_labels)

        download.get_headers()
        return download


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


class CreateCustomAssayForm(forms.ModelForm):
    class Meta:
        model = Assay
        fields = ['name','long_name', 'developer', 'description']

    def __init__(self, *args, **kwargs):
        super(CreateCustomAssayForm, self).__init__(*args, **kwargs)
