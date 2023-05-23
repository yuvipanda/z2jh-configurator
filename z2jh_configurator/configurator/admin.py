from django.contrib import admin
from reversion.admin import VersionAdmin


from .models import Profile, Image, ProfileImage


class ProfileImageInline(admin.StackedInline):
    model = ProfileImage
    extra = 1


class ProfileAdmin(VersionAdmin):
    inlines = [ProfileImageInline]


class ImageAdmin(VersionAdmin):
    model = Image

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Image, ImageAdmin)

