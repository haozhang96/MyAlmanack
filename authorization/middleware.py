from .decision import AuthorizationRequest

# Django
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process request?
        return self.get_response(request)
    
    def process_view(self, request, view, *view_args, **view_kwargs):
        pass
        """
        # Get the view's authorization action.
        action = getattr(view, "_authorization_action", None)
        
        # If the view has defined an action, check its authorization.
        if action is not None:
            resource = getattr(view, "_authorization_resource", None)
            
            # Make sure that the 
            if resource is None:
                raise ValueError()
            
            # Create an authorization request using the defined action.
            authorization_request = AuthorizationRequest(
                subject=request.user,
                action=action,
                resource=resource,
                context=request
            )
            
            # If the user is unauthorized to view the page, raise an exception.
            if not authorization_request.is_permitted:
                raise PermissionDenied
        """