from itertools import chain

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

    def __init__(self, specific_columns, results):

        self.headers = []
        self.content = []
        self.specific_columns = specific_columns
        self.results = results
        self.common_columns = [ "specimen.specimen_label",
                                "specimen.id",
                                "specimen.parent_label",
                                "specimen.specimen_type.name",
                                "assay_run.assay.name",
                                "assay_run.panel.name",
                                "laboratory.name",
                                "test_date",
                                "operator",
                                "assay_kit_lot",
                                "plate_identifier",
                                "specimen_purpose",
                                "test_mode",
                                "exclusion",
                                "warning_msg" ]

        self.clinical_columns = [ 'specimen.visit.subject.subject_label',
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
                                  "specimen.visit.cd4_count",
                                  "specimen.visit.viral_load",
                                  "specimen.visit.vl_type",
                                  "specimen.visit.vl_detectable",
                                  "specimen.visit.scopevisit_ec",
                                  "specimen.visit.subject.subject_eddi.eddi",
                                  "specimen.visit.subject.subject_eddi.ep_ddi",
                                  "specimen.visit.subject.subject_eddi.lp_ddi",
                                  "specimen.visit.visit_eddi.days_since_eddi",
                                  "specimen.visit.visit_eddi.days_since_ep_ddi",
                                  "specimen.visit.visit_eddi.days_since_lp_ddi",

                                  "specimen.visit.visitdetail.age_in_years",
                                  "specimen.visit.visitdetail.earliest_visit_date",
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

        for result in self.results:
            row = [ self.getattr_or_none(result, c) for c in combined_columns ]
            self.content.append(row)

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
