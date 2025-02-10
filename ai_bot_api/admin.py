from django.contrib import admin
from .models import CustomUser,AddCompanies
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(AddCompanies)