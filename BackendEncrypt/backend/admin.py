from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, PasswordEntry

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('email',)
    readonly_fields = ('created_at',)

@admin.register(PasswordEntry)
class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'username', 'service_url', 'created_at', 'updated_at')
    search_fields = ('title', 'username', 'user__email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
