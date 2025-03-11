from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# ثبت مدل User در پنل ادمین
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number','username','is_verified', 'is_staff', 'is_superuser','verification_code_expiry','verification_code')
    search_fields = ('phone_number',)
    ordering = ('phone_number',)

    # اضافه کردن فیلدهای سفارشی به فرم ادمین
    fieldsets = (
        (None, {'fields': ('username','phone_number', 'password')}),
        ('Permissions', {'fields': ('is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number','username', 'password1', 'password2', 'is_verified', 'is_staff', 'is_superuser'),
        }),
    )
