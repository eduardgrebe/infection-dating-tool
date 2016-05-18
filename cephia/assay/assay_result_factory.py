registered_result_models = []
registered_result_row_models = []

download_common_headers = ['specimen_label'
                           'specimen_id',
                           'specimen_common (first 4 digits of specimen_label if is a panel specimen)',
                           'root_specimen_label',
                           'specimen_type',
                           'assay',
                           'panel',
                           'laboratory',
                           'test_date',
                           'operator',
                           'assay_kit_lot',
                           'plate_identifier',
                           'specimen_purpose',
                           'test_mode',
                           'exclusion',
                           'warning_msg']

download_clinical_headers = ['subject_label',
                             'subject_id',
                             'source_study',
                             'visit.visit_date',
                             'specimen.reported_draw_date',
                             'cohort_entry_date',
                             'cohort_entry_hiv_status',
                             'visit.visit_hiv_status',
                             'subtype',
                             'subtype_confirmed',
                             'country',
                             'sex',
                             'age(vist_date-date_of_birth).years',
                             'population_group',
                             'risk_sex_with_men',
                             'risk_sex_with_women',
                             'risk_idu',
                             'art_initiation_date',
                             'aids_diagnosis_date',
                             'art_interruption_date',
                             'art_resumption_date',
                             'visit.treatment_naive',
                             'visit.on_treatment',
                             'visit.cd4_count',
                             'visit.viral_load',
                             'subject_eddi.eddi',
                             'subject_eddi.ep_ddi',
                             'subject_eddi.lp_ddi',
                             'visit_eddi.days_since_eddi',
                             'visit_eddi.days_since_ep_ddi',
                             'visit_eddi.days_since_lp_ddi']

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
