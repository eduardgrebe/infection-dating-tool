import logging
from subject_file_handler import SubjectFileHandler
from visit_file_handler import VisitFileHandler
from transfer_in_file_handler import TransferInFileHandler
from aliquot_file_handler import AliquotFileHandler
from transfer_out_file_handler import TransferOutFileHandler
from panel_membership_file_handler import PanelMembershipFileHandler
from panel_shipment_file_handler import PanelShipmentFileHandler
from lag_file_handler import LagFileHandler
from architect_file_handler import ArchitectFileHandler
from biorad_cdc_file_handler import BioradCDCFileHandler
from biorad_jhu_file_handler import BioradJHUFileHandler
from vitros_file_handler import VitrosFileHandler
from ls_vitros_file_handler import LSVitrosFileHandler
from geenius_file_handler import GeeniusFileHandler
from bed_file_handler import BEDFileHandler
from biorad_glasgow_file_handler import BioradGlasgowFileHandler
from luminex_file_handler import LuminexFileHandler
from ide_file_handler import IDEFileHandler
from duke_file_handler import DukeFileHandler

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
register_file_handler("panel_shipment", PanelShipmentFileHandler, None)
register_file_handler("panel_membership", PanelMembershipFileHandler, None)
register_file_handler("assay", LagFileHandler, 'LAg')
register_file_handler("assay", ArchitectFileHandler, 'Architect')
register_file_handler("assay", BioradCDCFileHandler, 'BioRad-Avidity-CDC')
register_file_handler("assay", BioradJHUFileHandler, 'BioRad-Avidity-JHU')
register_file_handler("assay", VitrosFileHandler, 'Vitros')
register_file_handler("assay", LSVitrosFileHandler, 'LS-Vitros')
register_file_handler("assay", GeeniusFileHandler, 'Geenius')
register_file_handler("assay", BEDFileHandler, 'BED')
register_file_handler("assay", BioradGlasgowFileHandler, 'BioRad-Avidity-Glasgow')
register_file_handler("assay", LuminexFileHandler, 'Luminex')
register_file_handler("assay", IDEFileHandler, 'IDE-V3')
register_file_handler("assay", DukeFileHandler, 'Duke-BioPlex')
