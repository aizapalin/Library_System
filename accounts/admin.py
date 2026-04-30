from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "library_id", "role", "is_librarian", "is_head_librarian", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "library_id")
    list_filter = ("role", "is_librarian", "is_head_librarian", "is_staff", "is_superuser", "is_active")
