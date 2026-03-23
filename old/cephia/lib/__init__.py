import traceback
import logging

def log_exception(e, logger=None):
    if logger is None:
        logger = logging.getLogger()
    logger.exception(e)
    return traceback.format_exception(type(e), e, None)[0]
    
