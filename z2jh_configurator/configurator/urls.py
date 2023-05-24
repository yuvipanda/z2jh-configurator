from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile-list", views.profile_list, name="profile-list"),
]
