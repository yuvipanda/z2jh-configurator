import os
from social_core.backends.oauth import BaseOAuth2


class JupyterHubOAuth(BaseOAuth2):
    """JupyterHub OAuth Backend"""

    name = "jupyterhub"
    hub_api = os.environ["JUPYTERHUB_API_URL"]
    AUTHORIZATION_URL = f"{hub_api}/oauth2/authorize"
    ACCESS_TOKEN_URL = f"{hub_api}/oauth2/token"
    ACCESS_TOKEN_METHOD = "POST"
    REDIRECT_STATE = False
    SCOPE_SEPARATOR = ","

    ID_KEY = "name"

    def auth_headers(self):
        headers = super().auth_headers()
        client_id, client_secret = self.get_key_and_secret()
        headers["Authorization"] = f"bearer {client_secret}"
        return headers

    def get_user_details(self, user_data):
        """Return user details from GitHub account"""
        details = {
            "username": user_data["name"],
            "email": "",
            "admin": user_data["admin"],
        }
        print(details)
        return details

    def user_data(self, access_token, response, *args, **kwargs):
        """Loads user data from service"""
        print(response)
        url = f"{self.hub_api}/user"
        user_data = self.get_json(
            url, headers={"Authorization": f"bearer {access_token}"}
        )
        print(user_data)
        return user_data


def make_jh_admins_superusers(strategy, details, backend, user=None, *args, **kwargs):
    """
    Make JupyterHub admins be django superusers & staff.

    This allows them to access the admin interface
    """
    if not user:
        return

    if details["admin"] != user.is_superuser:
        # Mark them as django superusers so they can access the admin interface,
        # if they are jupyterhub admins.
        user.is_superuser = details["admin"]
        user.is_staff = details["admin"]

        strategy.storage.user.changed(user)
