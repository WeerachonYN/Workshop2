
from rest_framework.views import exception_handler
def custom_exception_handler(exc, context):

    handlers = {
        'MethodNotAllowed':_exception_notAllowed,
        'NotAuthenticated':_exception_notAuthenticated,
        'PermissionDenied':_exception_permissionDenied,
        'ParseError':_exception_ParseError,
        'NotFound':_exception_pageNotfound,
        'NotAcceptable':_exception_notAccept,
        'UnsupportedMediaType':_exception_unsupportMD_type,
        'Throttled':_exception_throttled,
        'ValidationError':_exception_validatError,
        'AuthenticationFailed':_exception_AuthenticationFailed
    }

    response =  exception_handler(exc, context)
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc,context,response)
    return response

def _exception_notAuthenticated(exc,context,response):

    response.data = {
        'error':'Unauthenticated'
    }
    if response is not None:
        response.data['status_code'] = response.status_code
  
    return response

def _exception_notAllowed(exc,context,response):
    response.data = {
        'error':'Method Not Allowed'
    }
    if response is not None:
        response.data['status_code'] = response.status_code  
    return response

def _exception_permissionDenied(exc,context,response):
    response.data = {
        'error':'Forbidden'
    }
    if response is not None:
        response.data['status_code'] = response.status_code  
    return response

def _exception_ParseError(exc,context,response):
    response.data = {
        'error':'Bad Request'
    }
    if response is not None:
        response.data['status_code'] = response.status_code  
    return response

def _exception_pageNotfound(exc,context,response):
    response.data = {
        'error':'Not Found'
    }
    if response is not None:
        response.data['status_code'] = response.status_code  
    return response

def _exception_notAccept(exc,context,response):
    response.data = {
        'error':'Not Acceptable'
    }
    if response is not None:
        response.data['status_code'] = response.status_code  
    return response   


def _exception_unsupportMD_type(exc,context,response):
    response.data = {
        'error':'Unsupported Media Type'
    }
    if response is not None:
        response.data['status_code'] = response.status_code  
    return response   

def _exception_throttled(exc,context,response):
    response.data = {
        'error':'Too Many Requests'
    }
    if response is not None:
        response.data['status_code'] = response.status_code  
    return response   

def _exception_validatError(exc,context,response):
    response.data = {
        'error':'Validation Error'
    }
    if response is not None:
        response.data['status_code'] = response.status_code  
    return response   
def _exception_AuthenticationFailed(exc,context,response):

    response.data = {
        'error':'Unauthenticated'
    }