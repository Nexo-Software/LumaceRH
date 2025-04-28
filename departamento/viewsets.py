from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import DepartamentoSerializer
from .models import DepartamentoModel

class DepartamentoViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo DepartamentoModel"""
    queryset = DepartamentoModel.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Sobrescribir el método perform_create para añadir el usuario que crea el departamento."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """Sobrescribir el método perform_update para actualizar el usuario que modifica el departamento."""
        serializer.save(updated_by=self.request.user)
