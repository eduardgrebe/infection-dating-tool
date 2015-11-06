from functools import wraps
import logging
logger = logging.getLogger(__name__)
from models import AuthenticationToken
from api_data_interface import ApiDataInterface

class ApiDataInterface(object):
    def __init__(self, request):
        self.data = request.POST

    def error_response(http_code, error_code, msg):
        return { 'http_code': http_code, 
                 'error_code': error_code,
                 'msg': msg }

