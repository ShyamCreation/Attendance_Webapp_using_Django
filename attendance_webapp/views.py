from django.http import HttpResponse

from django.shortcuts import render

def base(request):
      # Example context data
    return render(request, 'base.html')  # Render child template


# views.py
from django.shortcuts import render

def session_expired_view(request):
    return render(request, 'session_expired.html', {'message': 'Your session has expired. Please login again.'})
