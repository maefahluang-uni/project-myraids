# matching/admin.py

from django.contrib import admin
from .models import Comparison, ColumnSelection, ComparisonResult

@admin.register(Comparison)
class ComparisonAdmin(admin.ModelAdmin):
    """Admin view for managing file comparisons."""
    list_display = ('id', 'user', 'file1', 'file2', 'common_column', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('file1__file', 'file2__file', 'common_column')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def file1(self, obj):
        return obj.file1.file.name.split('/')[-1]

    def file2(self, obj):
        return obj.file2.file.name.split('/')[-1]

@admin.register(ColumnSelection)
class ColumnSelectionAdmin(admin.ModelAdmin):
    """Admin view for managing column selections in comparisons."""
    list_display = ('id', 'comparison', 'column_file1', 'column_file2', 'combined_column_name')
    list_filter = ('comparison',)
    search_fields = ('column_file1', 'column_file2', 'combined_column_name')
    ordering = ('comparison',)

    def comparison(self, obj):
        return f"Comparison {obj.comparison.id} - {obj.comparison.user}"

@admin.register(ComparisonResult)
class ComparisonResultAdmin(admin.ModelAdmin):
    """Admin view for managing comparison results."""
    list_display = ('id', 'comparison', 'common_column_value', 'status', 'description')
    list_filter = ('status', 'comparison__user')
    search_fields = ('common_column_value', 'description')
    ordering = ('comparison', 'status')
    readonly_fields = ('data_file1', 'data_file2', 'status', 'description')

    def comparison(self, obj):
        return f"Comparison {obj.comparison.id} - {obj.comparison.user}"
