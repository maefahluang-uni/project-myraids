# admin.py

from django.contrib import admin
from .models import SelectedColumns, MatchedResult

@admin.register(SelectedColumns)
class SelectedColumnsAdmin(admin.ModelAdmin):
    """
    Admin configuration for SelectedColumns model.
    """
    list_display = ('id', 'user', 'excel_file_1', 'excel_file_2', 'common_column', 'created_at')
    search_fields = ('user__username', 'excel_file_1__file', 'excel_file_2__file', 'common_column')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'excel_file_1', 'excel_file_2')

@admin.register(MatchedResult)
class MatchedResultAdmin(admin.ModelAdmin):
    """
    Admin configuration for MatchedResult model.
    """
    list_display = ('id', 'user', 'session', 'common_value', 'file_source')
    search_fields = ('user__username', 'session__id', 'common_value')
    list_filter = ('file_source', 'session__created_at')
    ordering = ('-session__created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'session')
