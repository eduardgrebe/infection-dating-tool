from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings

class HttpOnlyCsrf(CsrfViewMiddleware):
    def process_response(self, request, response):
        response = super(HttpOnlyCsrf, self).process_response(request, response)
        if settings.CSRF_COOKIE_NAME in response.cookies:
            response.cookies[settings.CSRF_COOKIE_NAME]['httponly'] = True
        return response

