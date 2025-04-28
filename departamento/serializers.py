from rest_framework import serializers
from .models import DepartamentoModel

class DepartamentoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo DepartamentoModel"""
    class Meta:
        model = DepartamentoModel
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')