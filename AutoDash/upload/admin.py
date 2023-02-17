from django.contrib import admin
from upload.models import Data

# Register your models here.

class DataAdmin(admin.ModelAdmin):
    pass
admin.site.register(Data,DataAdmin)

