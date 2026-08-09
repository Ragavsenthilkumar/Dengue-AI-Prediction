from django.contrib import admin
from .models import Report, ActionAlert


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'risk_level', 'status', 'reported_by', 'created_at')
    list_filter = ('risk_level', 'status')
    search_fields = ('title', 'description')


@admin.register(ActionAlert)
class ActionAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'issued_by', 'report', 'created_at')
    list_filter = ('priority',)

