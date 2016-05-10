from assay.models import *
import logging


logger = logging.getLogger(__name__)

registered_results = []

def register_result(assay_name, cls):
    registered_results.append((cls, assay_name))

def get_results_for_assay(assay_name):
    for registered_assay_name, registered_result in registered_results:
        import pdb; pdb.set_trace()
        if registered_assay_name == assay_name:
            return registered_result
    raise Exception("Unknown assay: %s" % assay_name)


register_result(ArchitectAvidityResult, 'ArchitectAvidity')
register_result(ArchitectUnmodifiedResult, 'ArchitectUnmodified')
register_result(BEDResult, 'BED')
register_result(BioRadAvidityCDCResult, 'BioRadAvidity-CDC')
register_result(BioRadAvidityGlasgowResult, 'BioRadAvidity-Glasgow')
register_result(BioRadAvidityJHUResult, 'BioRadAvidity-JHU')
register_result(GeeniusResult, 'Geenius')
register_result(IDEV3Result, 'IDE-V3')
register_result(LagMaximResult, 'LAg-Maxim')
register_result(LagSediaResult, 'LAg-Sedia')
register_result(LSVitrosDiluentResult, 'LSVitros-Diluent')
register_result(LSVitrosPlasmaResult, 'LSVitros-Plasma')
register_result(LuminexCDCResult, 'BioPlex-CDC')
register_result(VitrosAvidityResult, 'Vitros')
