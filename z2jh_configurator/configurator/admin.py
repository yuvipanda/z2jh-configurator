from django.contrib import admin
from reversion.admin import VersionAdmin


from .models import Profile, Image, ProfileImage, ProfileNodeGroup


class ProfileImageInline(admin.StackedInline):
    model = ProfileImage
    extra = 0


class ProfileNodeGroupInline(admin.StackedInline):
    model = ProfileNodeGroup
    extra = 0


class ProfileAdmin(VersionAdmin):
    prepopulated_fields = {
        "slug": ["display_name"]
    }
    inlines = [ProfileImageInline, ProfileNodeGroupInline]


class ImageAdmin(VersionAdmin):
    prepopulated_fields = {
        "slug": ["display_name"]
    }
    model = Image

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Image, ImageAdmin)
