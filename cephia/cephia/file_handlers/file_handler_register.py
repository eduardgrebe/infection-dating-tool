import logging
from subject_file_handler import SubjectFileHandler
from visit_file_handler import VisitFileHandler
from transfer_in_file_handler import TransferInFileHandler
from aliquot_file_handler import AliquotFileHandler
from transfer_out_file_handler import TransferOutFileHandler
from protocol_lookup_file_handler import ProtocolLookupFileHandler
from test_history_file_handler import TestHistoryFileHandler
from diagnostic_test_file_handler import DiagnosticTestFileHandler
from test_properties_file_handler import TestPropertyFileHandler

logger = logging.getLogger(__name__)


registered_file_handlers = []


def register_file_handler(file_type, cls):
    registered_file_handlers.append((file_type, cls))


def get_file_handler_for_type(file_type):
    for registered_file_type, registered_file_handler in registered_file_handlers:
        if file_type == registered_file_type:
            return registered_file_handler
    raise Exception("Unknown file type: %s" % file_type)

register_file_handler("subject", SubjectFileHandler)
register_file_handler("visit", VisitFileHandler)
register_file_handler("aliquot", AliquotFileHandler)
register_file_handler("transfer_out", TransferOutFileHandler)
register_file_handler("transfer_in", TransferInFileHandler)
register_file_handler("diagnostic_test", DiagnosticTestFileHandler)
register_file_handler("test_history", TestHistoryFileHandler)
register_file_handler("protocol_lookup", ProtocolLookupFileHandler)
register_file_handler("test_property", TestPropertyFileHandler)
