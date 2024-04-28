from django.contrib import admin
from .models import DebtorExcelBase, ClaimerExcelBase, FieldPreset

class DebtorExcelBaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DebtorExcelBase._meta.fields]

class ClaimerExcelBaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ClaimerExcelBase._meta.fields]

class FieldPresetAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Add other fields you want to display in the admin list view

admin.site.register(DebtorExcelBase, DebtorExcelBaseAdmin)
admin.site.register(ClaimerExcelBase, ClaimerExcelBaseAdmin)
admin.site.register(FieldPreset, FieldPresetAdmin)
