import typing

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Librarian

# Register your models here.
# admin.site.register(Librarian)
# admin.site.register(Librarian, UserAdmin)


class CustomLibrarianAdmin(UserAdmin):
    # Campos de Leitura
    readonly_fields = ("date_joined", "last_login")

    # Campos na edição de informações do usuario
    fieldsets = (
        ("Credentials", {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("ssn", "shift", "birthdate")}),
        ("Permissions", {"fields": ("is_superuser", "is_active", "is_staff")}),
        ("Important Dates", {"fields": ("date_joined", "last_login")}),
    )

    # Colunas da tabela de filtro
    list_display = ("username", "ssn", "shift", "is_superuser")


admin.site.register(Librarian, CustomLibrarianAdmin)
