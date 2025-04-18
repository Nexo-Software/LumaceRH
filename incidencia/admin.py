from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import CategoriaIncidenciasModel, TablaCalculosIncidenciasModel, TipoIncidenciaModel, IncidenciasEmpleadoModel

admin.site.register(CategoriaIncidenciasModel, ModelAdmin)
admin.site.register(TablaCalculosIncidenciasModel, ModelAdmin)
admin.site.register(TipoIncidenciaModel, ModelAdmin)