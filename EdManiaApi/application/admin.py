from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, UserChild, ChildActivity, ChildDayActivity, Activities
from .forms import UserChangeForm, UserCreationForm

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["emailAddress", "is_admin"]
    list_filter = ("is_admin",)

    fieldsets = (
        ("Authentication", {"fields": ("emailAddress",)}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("emailAddress", "password1", "password2"),
            },
        ),
    )

    search_fields = ("emailAddress",)
    ordering = ("emailAddress",)
    filter_horizontal = ()


@admin.register(UserChild)
class UserChildAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "userID", "dateOfBirth"]


@admin.register(ChildActivity)
class ChildActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "childID", "activityID", "enabled"]


@admin.register(ChildDayActivity)
class ChildDayActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "childActivityID", "points", "hrs", "mins", "date"]


@admin.register(Activities)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
