from django.contrib import admin

from .models import Profile, Image, ProfileImage

admin.site.register(Image)


class ProfileImageInline(admin.StackedInline):
    model = ProfileImage
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProfileImageInline]


admin.site.register(Profile, ProfileAdmin)

