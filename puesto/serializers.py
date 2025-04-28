from rest_framework import serializers
from .models import PuestoModel

class PuestoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo PuestoModel"""
    class Meta:
        model = PuestoModel
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')