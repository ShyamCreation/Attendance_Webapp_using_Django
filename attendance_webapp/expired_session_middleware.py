from django.contrib.auth.views import redirect_to_login
from django.utils import timezone

class ExpiredSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and the session has expired
        if request.user.is_authenticated and request.session.get_expiry_age() <= 0:
            # If the session has expired, redirect the user to the login page
            return redirect_to_login(request.get_full_path())

        response = self.get_response(request)
        return response