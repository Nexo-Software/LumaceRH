from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import DepartamentoModel

admin.site.register(DepartamentoModel, ModelAdmin)