from django.shortcuts import redirect
from django.conf import settings


def index(request):
    return redirect(settings.JUPYTERHUB_SERVICE_PREFIX + "login/jupyterhub")
