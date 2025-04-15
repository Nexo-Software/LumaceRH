from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.

from .models import ContratoModel

admin.site.register(ContratoModel, ModelAdmin)