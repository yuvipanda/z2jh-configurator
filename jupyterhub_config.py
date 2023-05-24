import sys

c.JupyterHub.authenticator_class = "dummy"

c.Authenticator.admin_users = ["admin"]

c.JupyterHub.services = [
    {
        "name": "configurator",
        "url": "http://127.0.0.1:9000",
        "oauth_redirect_uri": "http://127.0.0.1:8000/services/configurator/complete/jupyterhub/",
        "command": [
            sys.executable,
            "-m",
            "gunicorn",
            "z2jh_configurator.wsgi:application",
            "--bind",
            "127.0.0.1:9000",
            "--reload",
        ],
    }
]
