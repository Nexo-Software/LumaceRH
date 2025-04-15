from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here.
from .models import EmpleadoModel, PostulanteModel

admin.site.register(PostulanteModel, ModelAdmin)
admin.site.register(EmpleadoModel, ModelAdmin)