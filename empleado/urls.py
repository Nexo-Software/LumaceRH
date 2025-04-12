from django.urls import path
from .views import PostulanteListView, PostulanteWizardView

urlpatterns = [
    path('', PostulanteListView.as_view(), name='postulante_list'),  # Listar postulantes
    path('create/', PostulanteWizardView.as_view(), name='postulante_create'),

]
