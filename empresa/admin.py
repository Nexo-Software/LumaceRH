from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import EmpresaModel

admin.site.register(EmpresaModel, ModelAdmin)