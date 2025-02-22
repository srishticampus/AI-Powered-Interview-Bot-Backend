from django.contrib import admin
from .models import CustomUser,AddCompanies,AddJob,JobApplication
# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'skills')
    search_fields = ('email', 'username')

class AddJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'company_name', 'job_description', 'application_deadline', 'created_at')

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(AddCompanies)
admin.site.register(AddJob, AddJobAdmin)
admin.site.register(JobApplication)
