import logging

#CLINICAL
from subject_file_handler import SubjectFileHandler
from visit_file_handler import VisitFileHandler
from transfer_in_file_handler import TransferInFileHandler
from aliquot_file_handler import AliquotFileHandler
from transfer_out_file_handler import TransferOutFileHandler

#DIAGNOSTIC TESTS
from panel_membership_file_handler import PanelMembershipFileHandler
from panel_shipment_file_handler import PanelShipmentFileHandler
from protocol_lookup_file_handler import ProtocolLookupFileHandler
from test_history_file_handler import TestHistoryFileHandler
from diagnostic_test_file_handler import DiagnosticTestFileHandler
from test_properties_file_handler import TestPropertyFileHandler

#ASSAY
from architect_avidity_file_handler import ArchitectAvidityFileHandler
from architect_unmodified_file_handler import ArchitectUnmodifiedFileHandler
from bed_file_handler import BEDFileHandler
from biorad_cdc_file_handler import BioRadAvidityCDCFileHandler
from biorad_glasgow_file_handler import BioRadAvidityGlasgowFileHandler
from biorad_jhu_file_handler import BioRadAvidityJHUFileHandler
from geenius_file_handler import GeeniusFileHandler
from ide_v3_file_handler import IDEV3FileHandler
from lag_maxim_file_handler import LagMaximFileHandler
from lag_sedia_file_handler import LagSediaFileHandler
from lsvitros_diluent_file_handler import LSVitrosDiluentFileHandler
from lsvitros_plasma_file_handler import LSVitrosPlasmaFileHandler
from luminex_file_handler import LuminexFileHandler
from vitros_file_handler import VitrosAvidityFileHandler

logger = logging.getLogger(__name__)

registered_file_handlers = []

def register_file_handler(file_type, assay, cls):
    registered_file_handlers.append((file_type, cls, assay))

def get_file_handler_for_type(file_type, assay):
    for registered_file_type, registered_file_assay, registered_file_handler in registered_file_handlers:
        if (file_type == registered_file_type) and (assay == registered_file_assay):
            return registered_file_handler
    raise Exception("Unknown file type: %s" % file_type)

register_file_handler("subject", SubjectFileHandler, None)
register_file_handler("visit", VisitFileHandler, None)
register_file_handler("aliquot", AliquotFileHandler, None)
register_file_handler("transfer_out", TransferOutFileHandler, None)
register_file_handler("transfer_in", TransferInFileHandler, None)

register_file_handler("diagnostic_test", DiagnosticTestFileHandler, None)
register_file_handler("test_history", TestHistoryFileHandler, None)
register_file_handler("protocol_lookup", ProtocolLookupFileHandler, None)
register_file_handler("test_property", TestPropertyFileHandler, None)

register_file_handler("panel_shipment", PanelShipmentFileHandler, None)
register_file_handler("panel_membership", PanelMembershipFileHandler, None)

# register_file_handler("assay", ArchitectAvidityFileHandler
# register_file_handler("assay", ArchitectUnmodifiedFileHandler
# register_file_handler("assay", BEDFileHandler
register_file_handler("assay", BioRadAvidityCDCFileHandler, 'BioRadAvidity-CDC')
register_file_handler("assay", BioRadAvidityGlasgowFileHandler, 'BioRadAvidity-Glasgow')
register_file_handler("assay", BioRadAvidityJHUFileHandler, 'BioRadAvidity-JHU')
# register_file_handler("assay", GeeniusFileHandler
# register_file_handler("assay", IDEV3FileHandler
# register_file_handler("assay", LagMaximFileHandler
register_file_handler("assay", LagSediaFileHandler, 'LAg-Sedia')
# register_file_handler("assay", LSVitrosDiluentFileHandler
# register_file_handler("assay", LSVitrosPlasmaFileHandler
# register_file_handler("assay", LuminexFileHandler
# register_file_handler("assay", VitrosAvidityFileHandler
'''
LAg-Maxim
ArchitectUnmodified
ArchitectAvidity
BioRadAvidity-JHU
Vitros
LSVitros-Diluent
LSVitros-Plasma
Geenius
BED
BioRadAvidity-Glasgow
Luminex-CDC
IDE-V3
BioPlex-Duke
Immuneticks-MixL
Immuneticks-NewMix
Immuneticks-NewMixPeptide
'''
