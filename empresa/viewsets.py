from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import EmpresaSerializer
from .models import EmpresaModel

class EmpresaViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo EmpresaModel"""
    queryset = EmpresaModel.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Sobrescribir el método perform_create para añadir el usuario que crea la empresa."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """Sobrescribir el método perform_update para actualizar el usuario que modifica la empresa."""
        serializer.save(updated_by=self.request.user)