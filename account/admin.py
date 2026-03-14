from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ( "","bio"),
        }),
    )
    model = User
    list_display = ('username', 'email',  'is_staff')
    list_filter= [ 'is_staff']

