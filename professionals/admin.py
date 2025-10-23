from django.contrib import admin
from .models import Professional


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ("id", "name_social", "profession", "contact")
    search_fields = ("name_social", "profession", "contact")
