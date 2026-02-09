from ProHire.wsgi import application
from functions_framework import http

@http
def prohire_app(request):
    """
    HTTP Cloud Function that wraps the Django WSGI application.
    """
    return application(request)
