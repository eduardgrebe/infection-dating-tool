registered_results = []

def register_result(assay_name, cls):
    registered_results.append((cls, assay_name))

def get_results_for_assay(assay_name):
    for registered_assay_name, registered_result in registered_results:
        if registered_assay_name == assay_name:
            return registered_result
    raise Exception("Unknown assay: %s" % assay_name)
