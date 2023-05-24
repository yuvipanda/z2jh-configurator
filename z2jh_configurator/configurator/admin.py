from django.contrib import admin
from reversion.admin import VersionAdmin


from .models import Profile, Image, ProfileImage


class ProfileImageInline(admin.StackedInline):
    model = ProfileImage
    extra = 1


class ProfileAdmin(VersionAdmin):
    prepopulated_fields = {
        "slug": ["display_name"]
    }
    inlines = [ProfileImageInline]


class ImageAdmin(VersionAdmin):
    prepopulated_fields = {
        "slug": ["display_name"]
    }
    model = Image

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Image, ImageAdmin)

