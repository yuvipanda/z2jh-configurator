from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse

from .models import Profile

def index(request):
    # FIXME: Use a reverse() here instead?
    return redirect(settings.JUPYTERHUB_SERVICE_PREFIX + "login/jupyterhub")


def profile_list(request):
    profiles = Profile.objects.all()
    return JsonResponse({
        'profile_list': [p.to_dict() for p in profiles]
    })
