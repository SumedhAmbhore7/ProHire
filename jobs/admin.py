from django.contrib import admin
from .models import Job, Application

@admin.action(description='Approve selected jobs')
def approve_jobs(modeladmin, request, queryset):
    queryset.update(status='active')

@admin.action(description='Reject selected jobs')
def reject_jobs(modeladmin, request, queryset):
    queryset.update(status='rejected')

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'posted_by', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    actions = [approve_jobs, reject_jobs]

admin.site.register(Job, JobAdmin)
admin.site.register(Application)
