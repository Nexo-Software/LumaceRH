from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import SucursalSerializer
from .models import SucursalModel

class SucursalViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo SucursalModel"""
    queryset = SucursalModel.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Sobrescribir el método perform_create para añadir el usuario que crea la sucursal."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """Sobrescribir el método perform_update para actualizar el usuario que modifica la sucursal."""
        serializer.save(updated_by=self.request.user)