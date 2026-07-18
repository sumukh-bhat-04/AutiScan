from django.contrib import admin
from .models import ScreeningResult

@admin.register(ScreeningResult)
class ScreeningResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'risk_level', 'probability', 'created_at')
    search_fields = ('user__username', 'risk_level')
    list_filter = ('risk_level', 'created_at')
