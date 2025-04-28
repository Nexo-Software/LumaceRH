from rest_framework import serializers
from .models import SucursalModel

class SucursalSerializer(serializers.ModelSerializer):
    """Serializer para el modelo SucursalModel"""
    class Meta:
        model = SucursalModel
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')