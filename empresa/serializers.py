from rest_framework import serializers
from .models import EmpresaModel

class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo EmpresaModel"""
    class Meta:
        model = EmpresaModel
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')