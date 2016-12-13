from itertools import chain
from django.conf import settings
import gc

registered_result_models = []
registered_result_row_models = []

def register_result_model(assay_name, cls):
    registered_result_models.append((cls, assay_name))

def register_result_row_model(assay_name, cls):
    registered_result_row_models.append((cls, assay_name))

def get_result_model(assay_name):
    for registered_assay_name, registered_result_model in registered_result_models:
        if registered_assay_name == assay_name:
            return registered_result_model
            raise Exception("Unknown assay: %s" % assay_name)

def get_result_row_model(assay_name):
    for registered_assay_name, registered_result_row_model in registered_result_row_models:
        if registered_assay_name == assay_name:
            return registered_result_row_model
            raise Exception("Unknown assay: %s" % assay_name)


class ResultDownload(object):

    def __init__(self, specific_columns, results, generic=False, result_models=None, limit=None, filter_by_visit=False):

        self.headers = []
        self.content = []
        self.specific_columns = specific_columns
        self.result_models = result_models
        self.detailed = bool(self.result_models)
        self.results = results.select_related(
            'assay', 'specimen', 'assay_run', 'specimen__visit__visitdetail', 'specimen__source_study',
            'specimen__visit', 'specimen__visit__subject', 'specimen__visit__subject__subject_eddi',
            'assay_run__panel', 'assay_run__laboratory', 'specimen__specimen_type', 'specimen__visit__visit_eddi',
            'specimen__visit__subject__population_group', 'specimen__visit__subject__subtype',
            'specimen__visit__subject__country', 'assay_run__assay'
        )
        self.limit = limit

        if self.result_models:
            for model in self.result_models:
                self.results = self.results.prefetch_related(model.__name__.lower() + '_set')

        specific_columns = [
            "operator",
            "assay_kit_lot",
            "plate_identifier",
            "specimen_purpose",
            "test_mode",
        ]

        if not filter_by_visit:
            self.common_columns = [ "specimen.specimen_label",
                                    "specimen.id",
                                    "specimen.parent_label",
                                    "specimen.specimen_type.name",
                                    "assay_run.id",
                                    "assay_run.assay.name",
                                    "assay_run.panel.name",
                                    "assay_run.laboratory.name",
                                    "test_date",
            ]

        elif filter_by_visit:
            self.common_columns = [ 'specimen.visit.subject.id',
                                    'specimen.visit.id',
                                    "specimen.id",
                                    "specimen.specimen_label",
                                    "specimen.parent_label",
                                    "specimen.specimen_type.name",
                                    "assay_run.id",
                                    "assay_run.assay.name",
                                    "assay_run.panel.name",
                                    "assay_run.laboratory.name",
                                    "test_date",
            ]

        if not (generic or self.detailed):
            self.common_columns += ['test_mode'] + specific_columns

        if self.detailed:
            self.common_columns += ['result_field', 'result_value']
            if not filter_by_visit:
                self.common_columns = ['generic_id', 'specific_id', 'test_mode'] + self.common_columns
            elif filter_by_visit:
                self.common_columns.insert(3, 'generic_id')
                self.common_columns.insert(4, 'specific_id')
                self.common_columns.insert(5, 'test_mode')

        self.common_columns += [
            "warning_msg",
            "method",
            "exclusion"
        ]

        self.clinical_columns = [
            'specimen.visit.id',
            'specimen.visit.subject.subject_label',
            'specimen.visit.subject.id',
            "specimen.source_study.name",
            "specimen.visit.visit_date",
            "specimen.reported_draw_date",
            "specimen.visit.subject.cohort_entry_date",
            "specimen.visit.subject.cohort_entry_hiv_status",
            "specimen.visit.visit_hivstatus",
            "specimen.visit.subject.subtype.name",
            "specimen.visit.subject.subtype_confirmed",
            "specimen.visit.subject.country.name",
            "specimen.visit.subject.sex",
            "specimen.visit.subject.date_of_birth",
            "specimen.visit.subject.population_group.name",
            "specimen.visit.subject.risk_sex_with_men",
            "specimen.visit.subject.risk_sex_with_women",
            "specimen.visit.subject.risk_idu",
            "specimen.visit.subject.last_negative_date",
            "specimen.visit.subject.first_positive_date",
            "specimen.visit.subject.fiebig_stage_at_firstpos",
            "specimen.visit.subject.edsc_reported",
            "specimen.visit.subject.ars_onset_date",
            "specimen.visit.subject.art_initiation_date",
            "specimen.visit.subject.aids_diagnosis_date",
            "specimen.visit.subject.art_interruption_date",
            "specimen.visit.subject.art_resumption_date",
            "specimen.visit.treatment_naive",
            "specimen.visit.on_treatment",
            "specimen.visit.first_treatment",
            "specimen.visit.pregnant",
            "specimen.visit.cd4_count",
            "specimen.visit.viral_load",
            "specimen.visit.viral_load_offset",
            "specimen.visit.vl_type",
            "specimen.visit.vl_detectable",
            "specimen.visit.subject.subject_eddi.eddi",
            "specimen.visit.subject.subject_eddi.ep_ddi",
            "specimen.visit.subject.subject_eddi.lp_ddi",
            "specimen.visit.subject.subject_eddi.eddi_interval_size",
            "specimen.visit.visit_eddi.days_since_eddi",
            "specimen.visit.visit_eddi.days_since_ep_ddi",
            "specimen.visit.visit_eddi.days_since_lp_ddi",

            "specimen.visit.visitdetail.age_in_years",
            "specimen.visit.visitdetail.earliest_visit_date",
            "specimen.visit.scopevisit_ec",
            "specimen.visit.visitdetail.ever_scope_ec",
            "specimen.visit.visitdetail.is_after_aids_diagnosis",
            "specimen.visit.visitdetail.ever_aids_diagnosis",
            "specimen.visit.visitdetail.days_since_cohort_entry",
            "specimen.visit.visitdetail.days_since_first_draw",
            "specimen.visit.visitdetail.days_since_first_art",
            "specimen.visit.visitdetail.days_since_current_art",
            "specimen.visit.visitdetail.days_from_eddi_to_first_art",
            "specimen.visit.visitdetail.days_from_eddi_to_current_art",
        ]

        if filter_by_visit:
            self.clinical_columns.remove('specimen.visit.id')
            self.clinical_columns.remove('specimen.visit.subject.id')

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
        combined_columns = list(chain(self.common_columns,
                                      self.specific_columns,
                                      self.clinical_columns))

        try:
            result_field_index = combined_columns.index('result_field')
            result_value_index = combined_columns.index('result_value')
            specific_id_index = combined_columns.index('specific_id')
            generic_id_index = combined_columns.index('generic_id')
            test_mode_field_index = combined_columns.index('test_mode')
            method_field_index = combined_columns.index('method')
            exclusion_field_index = combined_columns.index('exclusion')

        except (IndexError, ValueError):
            pass


        limited_results = self.results
        if self.limit:
            limited_results = self.results[0:self.limit]

        batch_size = 5000
        batch = limited_results[:batch_size]
        current_index = 0

        try:
            batch[0]
            has_results =  True
        except IndexError:
            has_results = False

        while has_results:
            
            for result in batch:
                row = [ self.getattr_or_none(result, c) for c in combined_columns ]

                if self.detailed:
                    for model in self.result_models:
                        row[generic_id_index] = result.pk
                        related_name = model.__name__.lower() + '_set'
                        for specific_result in getattr(result, related_name).all():
                            row[specific_id_index] = specific_result.pk
                            row[test_mode_field_index] = specific_result.test_mode
                            for field in model.result_detail_fields:
                                import pdb;pdb.set_trace()
                                row[result_field_index] = field
                                row[result_value_index] = getattr(specific_result, field, None)
                                row[method_field_index] = ''
                                if exclusion_field_index > -1:
                                    row[exclusion_field_index] = getattr(specific_result, 'exclusion', None)

                                self.content.append(list(row))
                                if self.limit and len(self.content) >= self.limit:
                                    break
                        row[result_field_index] = 'final_result'
                        row[test_mode_field_index] = ''
                        row[result_value_index] = result.result
                        row[method_field_index] = result.method
                        self.content.append(list(row))
                        if self.limit and len(self.content) >= self.limit:
                            break
                else:
                    self.content.append(row)

            gc.collect()

            current_index += batch_size
            batch = limited_results[current_index: current_index + batch_size]
            try:
                batch[0]
                has_results =  True
            except IndexError:
                has_results = False
            
            if self.limit and len(self.content) >= self.limit:
                break

            
    def prepare_headers(self):
        combined_columns = list(chain(self.common_columns,
                                      self.specific_columns,
                                      self.clinical_columns))
        for column in combined_columns:
            column_split = column.split('.')
            if column_split[-1] in ['id']:
                header = column_split[-2] + '_'  + column_split[-1]
            elif column_split[-1] in ['name']:
                header = column_split[-2]
            else:
                header = column_split[-1]
            self.headers.append(header)


    def add_extra_visits(self, visit_ids):
        result_visit_ids = self.results.values_list('specimen__visit__pk', flat=True).distinct()
        missing_visits = sorted(set(visit_ids).difference(result_visit_ids))

        self.prepare_empty_content(missing_visits=missing_visits)


    def add_extra_specimens(self, specimen_labels):
        result_specimen_labels = self.results.values_list('specimen__specimen_label', flat=True).distinct()
        missing_specimen_labels = sorted(set(specimen_labels).difference(result_specimen_labels))

        self.prepare_empty_content(missing_specimens=missing_specimen_labels)


    def prepare_empty_content(self, missing_visits=None, missing_specimens=None):
        combined_columns = list(chain(self.common_columns,
                                      self.specific_columns,
                                      self.clinical_columns))

        try:
            result_field_index = combined_columns.index('result_field')
            result_value_index = combined_columns.index('result_value')
            specific_id_index = combined_columns.index('specific_id')
            generic_id_index = combined_columns.index('generic_id')
            test_mode_field_index = combined_columns.index('test_mode')
            method_field_index = combined_columns.index('method')
            exclusion_field_index = combined_columns.index('exclusion')

        except (IndexError, ValueError):
            pass

        if missing_visits:
            for visit_id in missing_visits:
                row = [ visit_id if col == 'specimen.visit.id' else None for col in combined_columns  ]
                self.content.append(row)

        if missing_specimens:
            for specimen_label in missing_specimens:
                row = [ specimen_label if col == 'specimen.specimen_label' else None for col in combined_columns  ]
                self.content.append(row)
