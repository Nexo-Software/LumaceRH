from rest_framework import serializers
from .models import ContratoModel

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoModel
        fields = '__all__'  # O especifica los campos que deseas incluir
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')