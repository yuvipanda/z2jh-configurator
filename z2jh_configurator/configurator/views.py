from django.shortcuts import redirect
from django.conf import settings


def index(request):
    # FIXME: Use a reverse() here instead?
    return redirect(settings.JUPYTERHUB_SERVICE_PREFIX + "login/jupyterhub")
