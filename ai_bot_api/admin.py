from django.contrib import admin
from .models import CustomUser,AddCompanies,AddJob
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(AddCompanies)
admin.site.register(AddJob)
