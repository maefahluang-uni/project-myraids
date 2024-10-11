from django.contrib import admin
from matching.models import MatchingResult, MatchingPreset, MatchingHistory


@admin.register(MatchingResult)
class MatchingResultAdmin(admin.ModelAdmin):
    list_display = ('debtor_file', 'claimer_file', 'main_column_value', 'created_at')
    search_fields = ('main_column_value', 'debtor_file__file', 'claimer_file__file')
    list_filter = ('created_at',)


@admin.register(MatchingPreset)
class MatchingPresetAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


@admin.register(MatchingHistory)
class MatchingHistoryAdmin(admin.ModelAdmin):
    list_display = ('debtor_file', 'claimer_file', 'main_column_value', 'created_at')
    search_fields = ('main_column_value', 'debtor_file__file', 'claimer_file__file')
    list_filter = ('created_at', 'preset')

