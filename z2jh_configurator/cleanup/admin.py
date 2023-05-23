# Unregister models we do not want the user to see in the admin

from django.contrib import admin
from django.contrib.auth.models import User, Group
from social_django.models import Association, Nonce, UserSocialAuth

to_unregister = [
    User,
    Group,
    Association,
    Nonce,
    UserSocialAuth
]

for model in to_unregister:
    admin.site.unregister(model)
