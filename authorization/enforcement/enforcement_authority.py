from ..decision import DecisionAuthority
from ..utilities.reflection import assert_subclass

# Django
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest


class EnforcementAuthority:
    @classmethod
    def authorize(cls, request):
        return DecisionAuthority.authorize(request)
    
    @classmethod
    def authorize_http(cls, http_request, action, resource, redirect_403=True):
        # Make sure http_request is a subclass of Django's HttpRequest class.
        assert_subclass(http_request, HttpRequest)
        
        # Create the authorization request.
        from .authorization_request import AuthorizationRequest
        request = AuthorizationRequest(
            subject=http_request.user,
            action=action,
            resource=resource,
            context=http_request
        )
        
        if request.permitted:
            # If the authorization request is permitted, return True.
            return True
        else:
            # If the authorization request is denied, return False or raise 403.
            if redirect_403:
                raise PermissionDenied
            else:
                return False