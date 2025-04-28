from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ContratoSerializer
from .models import ContratoModel

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = ContratoModel.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Sobrescribir el método perform_create para añadir el usuario que crea el contrato."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)
    def perform_update(self, serializer):
        """Sobrescribir el método perform_update para actualizar el usuario que modifica el contrato."""
        serializer.save(updated_by=self.request.user)