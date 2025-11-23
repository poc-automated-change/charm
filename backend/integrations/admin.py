from django.contrib import admin
from .models import ChangeRequest


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = [
        'number',
        'short_description',
        'state',
        'priority',
        'jira_issue_key',
        'created_at'
    ]
    list_filter = ['state', 'priority', 'created_at']
    search_fields = [
        'number',
        'short_description',
        'description',
        'servicenow_sys_id',
        'jira_issue_key'
    ]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('ServiceNow Information', {
            'fields': ('servicenow_sys_id', 'number', 'short_description', 'description', 'state', 'priority')
        }),
        ('Integrations', {
            'fields': ('jira_issue_key', 'github_repo', 'github_pr_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
