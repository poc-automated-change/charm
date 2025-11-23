from django.db import models


class ChangeRequest(models.Model):
    """Links to ServiceNow change requests and related integrations"""

    # ServiceNow fields
    servicenow_sys_id = models.CharField(
        max_length=32,
        unique=True,
        help_text="ServiceNow system ID"
    )
    number = models.CharField(
        max_length=40,
        help_text="Change request number (e.g., CHG0030001)"
    )
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    state = models.CharField(max_length=20)
    priority = models.CharField(max_length=10)

    # Integration links
    jira_issue_key = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Linked Jira issue key"
    )
    github_repo = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="GitHub repository name"
    )
    github_pr_number = models.IntegerField(
        null=True,
        blank=True,
        help_text="GitHub pull request number"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Change Request'
        verbose_name_plural = 'Change Requests'
        indexes = [
            models.Index(fields=['servicenow_sys_id']),
            models.Index(fields=['number']),
            models.Index(fields=['jira_issue_key']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.number} - {self.short_description}"
