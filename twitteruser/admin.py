from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from twitteruser.models import TwitterUser


class TwitterUserAdmin(UserAdmin):
    list_display = (
        "username",
        "display_name",
    )
    prepopulated_fields = {"slug": ("username",)}
    list_filter = (
        "username",
        "display_name",
    )
    fieldsets = (
        (None, {"fields": ("username", "display_name", "following", "slug")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )


admin.site.register(TwitterUser, TwitterUserAdmin)
