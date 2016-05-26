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
                                  "specimen.visit.subject.art_initiation_date",
                                  "specimen.visit.subject.aids_diagnosis_date",
                                  "specimen.visit.subject.art_interruption_date",
                                  "specimen.visit.subject.art_resumption_date",
                                  "specimen.visit.treatment_naive",
                                  "specimen.visit.on_treatment",
                                  "specimen.visit.cd4_count",
                                  "specimen.visit.viral_load",
                                  "specimen.visit.subject.subject_eddi.eddi",
                                  "specimen.visit.subject.subject_eddi.ep_ddi",
                                  "specimen.visit.subject.subject_eddi.lp_ddi",
                                  "specimen.visit.visit_eddi.days_since_eddi",
                                  "specimen.visit.visit_eddi.days_since_ep_ddi",
                                  "specimen.visit.visit_eddi.days_since_lp_ddi" ]

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
            if column_split[-1] in ['id','name']:
                header = column_split[-2] + '_'  + column_split[-1]
            else:
                header = column_split[-1]
            self.headers.append(header)
