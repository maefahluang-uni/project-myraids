from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ExcelFile, Debtor, Claimer

# Debtor Inline for ExcelFile Admin
class DebtorInline(admin.TabularInline):
    model = Debtor
    extra = 0
    fields = ('PatientName', 'HN', 'VN', 'debt', 'DoctorName')
    readonly_fields = ('PatientName', 'HN', 'VN', 'debt', 'DoctorName')

# Claimer Inline for ExcelFile Admin
class ClaimerInline(admin.TabularInline):
    model = Claimer
    extra = 0
    fields = ('VN', 'HN', 'Stat', 'Amount', 'NetTotal')
    readonly_fields = ('VN', 'HN', 'Stat', 'Amount', 'NetTotal')

# ExcelFile Admin
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ('file_link', 'user', 'location', 'patient_type', 'uploaded_at')

    def file_link(self, obj):
        """Provide a link to the admin detail view instead of downloading the file."""
        url = reverse('admin:upload_excelfile_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.file.name)
    
    file_link.short_description = 'File'

    inlines = [DebtorInline, ClaimerInline]

# Debtor Admin
class DebtorAdmin(admin.ModelAdmin):
    list_display = ('PatientName', 'HN', 'VN', 'excelfile', 'location', 'debt', 'DoctorName')
    search_fields = ('PatientName', 'HN', 'VN')
    list_filter = ('location', 'patient_type')

# Claimer Admin
class ClaimerAdmin(admin.ModelAdmin):
    list_display = ('VN', 'HN', 'excelfile', 'Stat', 'Line', 'ClaimAcc', 'NetTotal', 'bill')
    search_fields = ('VN', 'HN')
    list_filter = ('location', 'patient_type')

# Registering models with admin site
admin.site.register(ExcelFile, ExcelFileAdmin)
admin.site.register(Debtor, DebtorAdmin)
admin.site.register(Claimer, ClaimerAdmin)
