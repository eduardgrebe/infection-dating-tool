from itertools import chain
from django.conf import settings


class SpecimenDownload(object):

    def __init__(self, specimens, limit=None):
        self.headers = []
        self.content = []
        self.limit = limit
        self.specimens = specimens

        self.columns = [
            "id",
            "specimen_label",
            "parent_label",
            'subject.id',
            'subject.subject_label_blinded',
            'subject.subject_label',
            'visit.id',
            "visit.visit_date",
            "specimen_type.name",
            "shipped_to.name",
            "source_study.name",
            "reported_draw_date",
            "visit.subject.cohort_entry_date",
            "visit.subject.cohort_entry_hiv_status",
            "visit.visit_hivstatus",
            "visit.subject.subtype.name",
            "visit.subject.subtype_confirmed",
            "visit.subject.country.name",
            "visit.subject.sex",
            "visit.subject.date_of_birth",
            "visit.subject.population_group.name",
            "visit.subject.risk_sex_with_men",
            "visit.subject.risk_sex_with_women",
            "visit.subject.risk_idu",
            "visit.subject.last_negative_date",
            "visit.subject.first_positive_date",
            "visit.subject.fiebig_stage_at_firstpos",
            "visit.subject.edsc_reported",
            "visit.subject.ars_onset_date",
            "visit.subject.art_initiation_date",
            "visit.subject.aids_diagnosis_date",
            "visit.subject.art_interruption_date",
            "visit.subject.art_resumption_date",
            "visit.treatment_naive",
            "visit.on_treatment",
            "visit.first_treatment",
            "visit.pregnant",
            "visit.cd4_count",
            "visit.viral_load",
            "visit.viral_load_offset",
            "visit.vl_type",
            "visit.vl_detectable",
            "visit.subject.subject_eddi.eddi",
            "visit.subject.subject_eddi.ep_ddi",
            "visit.subject.subject_eddi.lp_ddi",
            "visit.subject.subject_eddi.eddi_interval_size",
            "visit.visit_eddi.days_since_eddi",
            "visit.visit_eddi.days_since_ep_ddi",
            "visit.visit_eddi.days_since_lp_ddi",
            "visit.visitdetail.age_in_years",
            "visit.visitdetail.earliest_visit_date",
            "visit.scopevisit_ec",
            "visit.visitdetail.ever_scope_ec",
            "visit.visitdetail.is_after_aids_diagnosis",
            "visit.visitdetail.ever_aids_diagnosis",
            "visit.visitdetail.days_since_cohort_entry",
            "visit.visitdetail.days_since_first_draw",
            "visit.visitdetail.days_since_first_art",
            "visit.visitdetail.days_since_current_art",
            "visit.visitdetail.days_from_eddi_to_first_art",
            "visit.visitdetail.days_from_eddi_to_current_art",
        ]


        self.prepare_headers()
        self.prepare_content()

    def getattr_or_none(self, obj, attr):
        value = obj
        for key in attr.split('.'):
            value = getattr(value, key, None)
            if value is None:
                break
        return value

    def get_content(self):
        return self.content

    def get_headers(self):
        return self.headers

    def prepare_content(self):
        limited_specimens = self.specimens
        if self.limit:
            limited_specimens = self.specimens[0:self.limit]

        batch_size = 5000
        batch = limited_specimens[:batch_size]
        current_index = 0

        try:
            batch[0]
            has_specimens =  True
        except IndexError:
            has_specimens = False

        while has_specimens:
            
            for specimen in batch:
                row = [ self.getattr_or_none(specimen, c) for c in self.columns ]
                self.content.append(row)
                if self.limit and len(self.content) >= self.limit:
                    break

            current_index += batch_size
            batch = limited_specimens[current_index: current_index + batch_size]
            try:
                batch[0]
                has_specimens =  True
            except IndexError:
                has_specimens = False
            
            if self.limit and len(self.content) >= self.limit:
                break

            
    def prepare_headers(self):
        for column in self.columns:
            column_split = column.split('.')
            if column_split[-1] in ['id']:
                if column == 'id':
                    header = 'specimen_id'
                else:
                    header = column_split[-2] + '_'  + column_split[-1]
            elif column_split[-1] in ['name']:
                header = column_split[-2]
                if header == 'panel':
                    header = 'panel_name'
            elif column_split[-1] in ['short_name']:
                header = column_split[-2]
            else:
                header = column_split[-1]
            self.headers.append(header)


    def add_extra_specimens(self, specimen_labels):
        existing_specimen_labels = self.specimens.values_list('specimen_label', flat=True).distinct()
        missing_specimen_labels = sorted(set(specimen_labels).difference(existing_specimen_labels))

        self.prepare_empty_content(missing_specimens=missing_specimen_labels)


    def prepare_empty_content(self, missing_specimens=None):
        if missing_specimens:
            for specimen_label in missing_specimens:
                row = [ specimen_label if col == 'specimen_label' else None for col in self.columns  ]
                self.content.append(row)
