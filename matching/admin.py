from django.contrib import admin
from .models import ExcelBase

class ExcelBaseAdmin(admin.ModelAdmin):
    list_display = ['No', 'AN', 'HN', 'CID', 'name', 'nationality', 'admit_date']  # Customize the fields displayed in the admin list view

admin.site.register(ExcelBase, ExcelBaseAdmin)
