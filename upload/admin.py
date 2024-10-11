from django.contrib import admin
from upload.models import ExcelFile, Debtor, Claimer

class ExcelFileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ExcelFile._meta.fields]

class DebtorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Debtor._meta.fields]

class ClaimerAdmin(admin.ModelAdmin):  
    list_display = [field.name for field in Claimer._meta.fields]

admin.site.register(ExcelFile, ExcelFileAdmin)
admin.site.register(Debtor, DebtorAdmin)
admin.site.register(Claimer, ClaimerAdmin)
