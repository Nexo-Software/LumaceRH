from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import PuestoSerializer
from .models import PuestoModel

class PuestoViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo PuestoModel"""
    queryset = PuestoModel.objects.all()
    serializer_class = PuestoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Sobrescribir el método perform_create para añadir el usuario que crea el puesto."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """Sobrescribir el método perform_update para actualizar el usuario que modifica el puesto."""
        serializer.save(updated_by=self.request.user)