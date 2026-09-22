from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_suspended', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (('ข้อมูลเพิ่มเติม', {'fields': ('role', 'phone', 'is_suspended')}),)

admin.site.register(CustomUser, CustomUserAdmin)
