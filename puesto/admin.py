from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import PuestoModel

admin.site.register(PuestoModel, ModelAdmin)