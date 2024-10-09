from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.utils import timezone

class SessionLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Get the current session key
            current_session_key = request.session.session_key

            # Get all active sessions for the current user
            user_sessions = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_data__contains=f"_auth_user_id:{request.user.pk}"
            ).exclude(session_key=current_session_key)

            # Limit the number of active sessions
            max_sessions = 1  # Set the desired maximum number of sessions
            if user_sessions.count() >= max_sessions:
                # Logout all other sessions
                for session in user_sessions:
                    session_data = session.get_decoded()
                    if request.user.pk == int(session_data.get('_auth_user_id')):
                        session.delete()

                # Logout the current session as well
                logout(request)

        response = self.get_response(request)
        return response